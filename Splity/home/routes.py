from flask import Blueprint, render_template, redirect, flash, url_for
from flask_login import login_required, current_user
from Splity.forms.forms import GroupCreationForm, JoinGroupForm, GroupEditForm, RepaymentForm
from Splity.services import groups_services, currency_service, bill_services

home_blueprint=Blueprint("home",__name__)

@home_blueprint.route("/",strict_slashes=False)
def home():
    if not current_user.is_authenticated:
        return redirect(url_for("authentication.login"))
    return render_template("home.html",groups=groups_services.get_user_groups(current_user.id))

@home_blueprint.route("/create_group",methods=["GET","POST"],strict_slashes=False)
@login_required
def create_group():
    form=GroupCreationForm(); form.currency.choices=currency_service.get_currency()
    if form.validate_on_submit():
        try:
            group=groups_services.create_group(form.name.data,form.description.data,form.currency.data,current_user.id)
            flash(f"Group '{group.name}' created.","success")
            return redirect(url_for("home.group_details",group_id=group.id))
        except groups_services.GroupServiceException as error: flash(str(error),"danger")
    return render_template("group/group_creation.html",form=form)

@home_blueprint.route("/join_group",methods=["GET","POST"],strict_slashes=False)
@login_required
def join_group():
    form=JoinGroupForm()
    if form.validate_on_submit():
        try:
            group=groups_services.join_group(form.invite_code.data,current_user.id)
            flash(f"You joined '{group.name}'.","success")
            return redirect(url_for("home.group_details",group_id=group.id))
        except groups_services.GroupServiceException as error: flash(str(error),"danger")
    return render_template("group/join_group.html",form=form)

@home_blueprint.route("/group/<int:group_id>",strict_slashes=False)
@login_required
def group_details(group_id):
    try:
        group,members=groups_services.get_group_details(group_id,current_user.id)
        bills=bill_services.get_bills_and_creators_service(group_id)
        settlements,balances=bill_services.settling_algorithm(group_id)
        repayments=bill_services.get_repayments(group_id)
        repayment_form=RepaymentForm()
        repayment_form.payee_id.choices=[(s[4],s[2]) for s in settlements if s[3]==current_user.id]
        return render_template("group/group_details.html",group=group,members=members,bill_data=bills,
            total_group_spending=bill_services.total_group_spending(group_id),
            user_net_balance=round(balances.get(current_user.id,["",0])[1],2),
            settle_payments=settlements,repayments=repayments,repayment_form=repayment_form)
    except groups_services.GroupServiceException as error:
        flash(str(error),"danger"); return redirect(url_for("home.home"))

@home_blueprint.route("/group/<int:group_id>/edit",methods=["GET","POST"],strict_slashes=False)
@login_required
def edit_group(group_id):
    try: group,members=groups_services.get_group_details(group_id,current_user.id)
    except groups_services.GroupServiceException as error:
        flash(str(error),"danger"); return redirect(url_for("home.home"))
    if current_user.id!=group.creator_id:
        flash("Only the group owner can change group settings.","danger")
        return redirect(url_for("home.group_details",group_id=group_id))
    form=GroupEditForm(obj=None)
    if form.validate_on_submit():
        try:
            groups_services.edit_group(form.name.data,form.description.data,group_id,current_user.id)
            flash("Group details updated.","success")
            return redirect(url_for("home.group_details",group_id=group_id))
        except groups_services.GroupServiceException as error: flash(str(error),"danger")
    elif not form.is_submitted():
        form.name.data=group.name; form.description.data=group.description
    return render_template("group/edit_group.html",form=form,members=members,group=group)

@home_blueprint.post("/group/<int:group_id>/remove_user/<int:user_id>")
@login_required
def remove_user(group_id,user_id):
    try:
        member=groups_services.remove_user(group_id,user_id,current_user.id)
        flash(f"{member.name} was removed. Their expense history remains in the group.","success")
    except groups_services.GroupServiceException as error: flash(str(error),"danger")
    return redirect(url_for("home.edit_group",group_id=group_id))

@home_blueprint.post("/group/<int:group_id>/leave")
@login_required
def leave_group(group_id):
    try:
        _,group=groups_services.leave_from_group(group_id,current_user.id)
        flash(f"You left '{group.name}'. Its existing history has been preserved.","success")
        return redirect(url_for("home.home"))
    except groups_services.GroupServiceException as error:
        flash(str(error),"danger"); return redirect(url_for("home.group_details",group_id=group_id))

@home_blueprint.post("/group/<int:group_id>/delete")
@login_required
def delete_group(group_id):
    try:
        group=groups_services.delete_group(group_id,current_user.id)
        flash(f"Group '{group.name}' deleted.","success")
        return redirect(url_for("home.home"))
    except groups_services.GroupServiceException as error:
        flash(str(error),"danger"); return redirect(url_for("home.group_details",group_id=group_id))
