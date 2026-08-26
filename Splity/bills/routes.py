from flask import Blueprint, render_template, redirect, flash, url_for, request
from flask_login import login_required, current_user
from Splity.forms.forms import CreateBillForm, RepaymentForm
from Splity.services import bill_services, groups_services

bills_blueprint=Blueprint("bills",__name__)

def _prepare_form(form,group_id):
    members=groups_services.get_group_members(group_id)
    choices=[(member.id,member.name) for member in members]
    form.payer_id.choices=choices
    form.names.choices=choices
    return members

def _custom_amounts(form):
    return {member_id:request.form.get(f"custom_amount_{member_id}") for member_id in form.names.data}

@bills_blueprint.route("/group/<int:group_id>/create_bill",methods=["GET","POST"],strict_slashes=False)
@login_required
def create_bill(group_id):
    try:
        group,_=groups_services.get_group_details(group_id,current_user.id)
    except groups_services.GroupServiceException as error:
        flash(str(error),"danger"); return redirect(url_for("home.home"))
    form=CreateBillForm()
    members=_prepare_form(form,group_id)
    if request.method=="GET":
        form.payer_id.data=current_user.id
        form.names.data=[member.id for member in members]
    if form.validate_on_submit():
        try:
            bill_services.add_bill_service(
                user_id=current_user.id,description=form.description.data,amount=form.amount.data,
                owe_members=form.names.data,group_id=group_id,payer_id=form.payer_id.data,
                split_mode=form.split_mode.data,custom_amounts=_custom_amounts(form))
            flash("Expense added.","success")
            return redirect(url_for("home.group_details",group_id=group_id))
        except bill_services.BillServiceException as error: flash(str(error),"danger")
    return render_template("bills/create_bill.html",form=form,currency=group.currency,group_id=group_id,members=members)

@bills_blueprint.route("/group/<int:group_id>/bill/<int:bill_id>/edit",methods=["GET","POST"])
@login_required
def edit_bill(group_id,bill_id):
    try:
        groups_services.get_group_details(group_id,current_user.id)
        bill=groups_services.get_bill(bill_id)
        if not bill or bill.group_id!=group_id: raise bill_services.BillServiceException("Expense not found.")
    except (groups_services.GroupServiceException,bill_services.BillServiceException) as error:
        flash(str(error),"danger"); return redirect(url_for("home.home"))
    form=CreateBillForm()
    members=_prepare_form(form,group_id)
    participant_repo=groups_services.get_bill_participants(bill_id)
    existing={p.user_id:p.amount_owed for p in participant_repo}
    if request.method=="GET":
        form.description.data=bill.description; form.amount.data=bill.amount
        form.payer_id.data=bill.user_id; form.names.data=list(existing)
    if form.validate_on_submit():
        try:
            bill_services.edit_bill_service(
                bill_id,current_user.id,form.description.data,form.amount.data,form.names.data,
                form.payer_id.data,form.split_mode.data,_custom_amounts(form))
            flash("Expense updated.","success")
            return redirect(url_for("home.group_details",group_id=group_id))
        except bill_services.BillServiceException as error: flash(str(error),"danger")
    return render_template("bills/create_bill.html",form=form,currency=groups_services.get_group(group_id).currency,
        group_id=group_id,members=members,editing=True,bill=bill,existing_shares=existing)

@bills_blueprint.post("/group/<int:group_id>/delete_bill/<int:bill_id>")
@login_required
def delete_bill(bill_id,group_id):
    try:
        bill_services.delete_bill_service(bill_id,current_user.id,group_id)
        flash("Expense deleted.","success")
    except bill_services.BillServiceException as error: flash(str(error),"danger")
    return redirect(url_for("home.group_details",group_id=group_id))

@bills_blueprint.post("/group/<int:group_id>/repay")
@login_required
def repay(group_id):
    form=RepaymentForm()
    settlements,_=bill_services.settling_algorithm(group_id)
    form.payee_id.choices=[(s[4],s[2]) for s in settlements if s[3]==current_user.id]
    if form.validate_on_submit():
        try:
            bill_services.record_repayment(group_id,current_user.id,form.payee_id.data,form.amount.data)
            flash("Repayment recorded. The receiver must confirm it.","success")
        except bill_services.BillServiceException as error: flash(str(error),"danger")
    else: flash("Enter a valid repayment.","danger")
    return redirect(url_for("home.group_details",group_id=group_id))

@bills_blueprint.post("/repayment/<int:repayment_id>/confirm")
@login_required
def confirm_repayment(repayment_id):
    repayment=bill_services.confirm_repayment(repayment_id,current_user.id)
    flash("Repayment confirmed and balances updated.","success")
    return redirect(url_for("home.group_details",group_id=repayment.group_id))
