from flask import Blueprint, render_template, redirect, flash, url_for
from flask_login import login_required, current_user

from Splity.forms.forms import GroupCreationForm
from Splity.services import groups_services, currency_service

home_blueprint = Blueprint("home", __name__)

@home_blueprint.route('/')
def home():
    return render_template('home.html')

@home_blueprint.route('/create_group', methods=['GET', 'POST'])
@login_required
def create_group():
    form = GroupCreationForm()

    # Populate the dropdown dynamically from the API
    form.currency.choices = currency_service.get_currency()

    if form.validate_on_submit():
        try:
            # CALL THE SERVICE, NOT THE FORM
            group = groups_services.create_group(
                name=form.name.data,
                description=form.description.data,
                currency=form.currency.data,
                creator_id=current_user.id
            )
            flash(f"Group '{group.name}' created! Invite code: {group.invite_code}", "success")
            return redirect(url_for('home.home'))
        except groups_services.GroupServiceException as e:
            flash(str(e), "danger")
        except Exception as e:
            flash(f"An unexpected error occurred: {str(e)}", "danger")

    return render_template('groupcreation.html', form=form)