# /Splity_flask/Splity/bills/routes.py


from flask import Blueprint, render_template, redirect, flash, url_for, request
from flask_login import login_required, current_user

from Splity.forms.forms import CreateBillForm
from Splity.services import bill_services, groups_services



bills_blueprint = Blueprint('bills', __name__)

@bills_blueprint.route('/group/<int:group_id>/create_bill', methods=['GET', 'POST'], strict_slashes=False)
@login_required
def create_bill(group_id):
    form = CreateBillForm()
    currency = groups_services.get_group(group_id).currency
    owe_members = groups_services.get_group_members(group_id)
    form.names.choices = [f"{member.name} | @{member.username}" for member in owe_members]
    if request.method == 'GET':
        form.names.data = form.names.choices
    if form.validate_on_submit():
        try:
            bill = bill_services.add_bill_service(user_id=current_user.id,
                                          description=form.description.data.rstrip(),
                                          amount=form.amount.data,
                                          owe_members=[member.id for member in owe_members],
                                          group_id=group_id)
            flash(f"Bill '{bill.description}' Added", 'success')
            return redirect(url_for('home.group_details', group_id=group_id))
        except bill_services.BillServiceException as e:
            flash(str(e), 'danger')
    return render_template("bills/create_bill.html", form=form, currency=currency)


@bills_blueprint.route('/group/<int:group_id>/delete_bill/<int:bill_id>', methods=['GET', 'POST'], strict_slashes=False)
@login_required
def delete_bill(bill_id, group_id):
    try:
        bill = bill_services.delete_bill_service(bill_id=bill_id, current_user_id=current_user.id, group_id=group_id)
        flash(f"Bill '{bill.description}' Deleted", 'success')
        return redirect(url_for('home.group_details', group_id=group_id))
    except bill_services.BillServiceException as e:
        flash(str(e), 'danger')
        return redirect(url_for('home.group_details', group_id=group_id))
