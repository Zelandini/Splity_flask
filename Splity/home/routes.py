# /Splity_flask/Splity/home/routes.py


from flask import Blueprint, render_template, redirect, flash, url_for
from flask_login import login_required, current_user

from Splity.adapters.repository import GroupRepository
from Splity.forms.forms import GroupCreationForm, JoinGroupForm
from Splity.services import groups_services, currency_service

home_blueprint = Blueprint("home", __name__)

@home_blueprint.route('/')
def home():
    groups = []
    if current_user.is_authenticated:
        group = GroupRepository()
        groups = group.get_user_groups(current_user.id)
    return render_template('home.html', groups=groups)

@login_required
def my_groups():
    groups = current_user.groups
    return render_template('group_details.html', groups=groups)


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

    return render_template('group_creation.html', form=form)

@home_blueprint.route('/join_group', methods=['GET', 'POST'])
@login_required
def join_group():
    form = JoinGroupForm()
    if form.validate_on_submit():
        try:
            group = groups_services.join_group(form.invite_code.data.upper(), current_user.id)
            flash(f"Successfully joined Group '{group.name}'", "success")
            return redirect(url_for('home.home'))
        except groups_services.GroupServiceException as e:
            flash(str(e), "danger")
        except Exception as e:
            flash(f"An unexpected error occurred: {str(e)}", "danger")
    return render_template('join_group.html', form=form)

@home_blueprint.route('/group/<int:group_id>', methods=['GET', 'POST'])
@login_required
def group_details(group_id):
    group_repo = GroupRepository()
    group = group_repo.get_by_id(group_id)
    if not group:
        flash("Group not found", "danger")
        return redirect(url_for('home.home'))

    user_groups = group_repo.get_user_groups(current_user.id)
    user_group_ids = [g.id for g in user_groups]
    if group_id not in user_group_ids:
        flash(f"You are not in Group {group.name}", "danger")
        return redirect(url_for('home.home'))

    member_groups = group_repo.get_group_members(group_id)
    for member in member_groups:
        print(member)

    return render_template('group_details.html', group=group, members=member_groups)