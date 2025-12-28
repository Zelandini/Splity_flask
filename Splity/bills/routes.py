# /Splity_flask/Splity/bills/routes.py


from flask import Blueprint, render_template, redirect, flash, url_for
from flask_login import login_required, current_user

from Splity.forms.forms import CreateBillForm
from Splity.services import bill_services, groups_services



bills_blueprint = Blueprint('bills', __name__)

@bills_blueprint.route('/group/<int:group_id>/create_bill', methods=['GET', 'POST'])
@login_required
def create_bill(group_id):
    form = CreateBillForm()
    owe_members = groups_services.get_group_members(group_id)
    form.owe_members.choices = [f"{member.name} | @{member.username}" for member in owe_members]
    # if form.validate_on_submit():
    #     try:
    #         bill = groups_services.ad
    return render_template("bills/create_bill.html", form=form)