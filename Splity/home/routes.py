# /Splity_flask/Splity/home/routes.py

from flask import Blueprint, render_template, redirect, flash, url_for
from flask_login import login_required, current_user

from Splity.adapters.repository import GroupRepository
from Splity.forms.forms import GroupCreationForm, JoinGroupForm, GroupEditForm
from Splity.services import groups_services, currency_service

home_blueprint = Blueprint("home", __name__)


@home_blueprint.route('/')
def home():
    """Home page - shows user's groups"""
    groups = []
    if current_user.is_authenticated:
        group_repo = GroupRepository()
        groups = group_repo.get_user_groups(current_user.id)
    return render_template('home.html', groups=groups)


@home_blueprint.route('/create_group', methods=['GET', 'POST'])
@login_required
def create_group():
    """Create a new group"""
    form = GroupCreationForm()

    # Populate the dropdown dynamically from the API
    form.currency.choices = currency_service.get_currency()

    if form.validate_on_submit():
        try:
            # Call the service to create group
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
    """Join an existing group using invite code"""
    form = JoinGroupForm()

    if form.validate_on_submit():
        try:
            # FIX: Correct parameter order - (user_id, invite_code)
            group = groups_services.join_group(
                user_id=current_user.id,
                invite_code=form.invite_code.data.strip().upper()
            )
            flash(f"Successfully joined Group '{group.name}'", "success")
            return redirect(url_for('home.home'))
        except groups_services.GroupServiceException as e:
            flash(str(e), "danger")
        except Exception as e:
            flash(f"An unexpected error occurred: {str(e)}", "danger")

    return render_template('join_group.html', form=form)


@home_blueprint.route('/group/<int:group_id>')
@login_required
def group_details(group_id):
    try:
        group, members = groups_services.get_group_details(group_id, current_user.id)
        return render_template('group_details.html', group=group, members=members)
    except groups_services.GroupServiceException as e:
        flash(str(e), "danger")
        return redirect(url_for('home.home'))


@home_blueprint.route('/group/<int:group_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_group(group_id):
    group, members = groups_services.get_group_details(group_id, current_user.id)
    form = GroupEditForm(name=group.name, description=group.description)
    if current_user.id != group.creator_id:
        flash("You cannot edit this group", "danger")
        return redirect(url_for('home.group_details', group_id=group.id))
    if form.validate_on_submit():
        try:
            group = groups_services.edit_group(name=form.name.data, description=form.description.data, group_id=group_id, creator_id=current_user.id)
            flash(f"Successfully edited Group '{group.name}'", "success")
            return redirect(url_for('home.group_details', group_id=group.id))
        except groups_services.GroupServiceException as e:
            flash(str(e), "danger")
    return render_template('edit_group.html', form=form, members=members, group=group)
