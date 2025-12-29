# /Splity_flask/Splity/services/groups_services.py
from typing import List

from Splity.adapters.repository import GroupRepository, UserRepository, BillRepository
from Splity.domainmodel.models import Group, User, Bill


class GroupServiceException(Exception):
    pass


def create_group(name: str, description: str, currency: str, creator_id: int) -> Group:
    repo = GroupRepository()
    existing_group = repo.get_by_name_and_membership(name, creator_id)
    if existing_group:
        raise GroupServiceException(f"You already have a group named '{name}'.")
    if not name or not name.strip():
        raise GroupServiceException("Group name cannot be empty.")
    try:
        new_group = Group(name=name, description=description, currency=currency, creator_id=creator_id)
        repo.add(new_group)
        return new_group
    except Exception as e:
        raise GroupServiceException(f"Failed to create group: {str(e)}")


def get_group_details(group_id: int, user_id: int):
    repo = GroupRepository()
    group = repo.get_by_id(group_id)
    if not group:
        raise GroupServiceException("Group not found.")
    user_groups = repo.get_group_members(group_id)
    user_groups_ids = [user.id for user in user_groups]
    if user_id not in user_groups_ids:
        raise GroupServiceException(f"You are not in Group {group.name}")
    members = repo.get_group_members(group_id)
    return group, members


def join_group(invite_code: str, user_id: int) -> Group:
    repo = GroupRepository()
    invite_code = invite_code.strip().upper()
    if len(invite_code) != 6:
        raise GroupServiceException("Invalid invite code format.")
    try:
        success = repo.join_by_code(user_id, invite_code)
        if not success:
            raise GroupServiceException("Invalid invite code or you're already in this group.")
        group = repo.get_by_invite_code(invite_code)
        return group
    except Exception as e:
        raise GroupServiceException(f"Failed to join group: {str(e)}")


def leave_from_group(group_id, user_id: int):
    repo = GroupRepository()
    group = repo.get_by_id(group_id)
    existing_group = repo.get_by_name_and_membership(group.name, user_id)
    if not existing_group:
        raise GroupServiceException("You are not in group.")
    if user_id == existing_group.creator_id:
        raise GroupServiceException("You are not allowed to leave the group.")
    try:
        member_removed = repo.remove_member(group_id, user_id)
        return member_removed, existing_group
    except Exception as e:
        raise GroupServiceException(f"Failed to leave group: {str(e)}")


def remove_user(group_id: int, user_id: int, requester_id: int):
    repo = GroupRepository()
    user = UserRepository()
    group = repo.get_by_id(group_id)
    user_to_remove = user.get_by_id(user_id)  # Ensure your repo has this
    if not group or not user_to_remove:
        raise GroupServiceException("Group or User not found.")
    if group.creator_id != requester_id:
        raise GroupServiceException("Only the creator can remove members.")
    if user_id == group.creator_id:
        raise GroupServiceException("You cannot remove yourself from the group.")
    success = repo.remove_member(group_id, user_id)
    if not success:
        raise GroupServiceException("User is not a member of this group.")
    return user_to_remove  # Return the user so we can flash their name

def delete_group(group_id: int, user_id: int):
    repo = GroupRepository()
    group = repo.get_by_id(group_id)
    if not group:
        raise GroupServiceException("Group not found.")
    if user_id != group.creator_id:
        raise GroupServiceException("Not authorised to delete this group.")
    try:
        success = repo.delete_group(group_id)
        if not success:
            raise GroupServiceException("Group was not deleted.")
        return group
    except Exception as e:
        raise GroupServiceException(f"Failed to delete group: {str(e)}")


def edit_group(name: str, description: str, group_id: int, creator_id: int) -> Group:
    repo = GroupRepository()
    current_group = repo.get_by_id(group_id)
    existing_group = repo.get_by_name_and_membership(name, creator_id)
    if current_group.creator_id != creator_id:
        raise GroupServiceException("You are not allowed to edit this group.")
    if not name or not name.strip():
        raise GroupServiceException("Group name cannot be empty.")
    if not description or not description.strip():
        raise GroupServiceException("Group description cannot be empty.")
    if existing_group:
        raise GroupServiceException("Group name already exists.")
    try:
        current_group.name = name
        current_group.description = description
        repo.edit_group_name(group_id, name)
        repo.edit_group_description(group_id, description)
        return current_group
    except Exception as e:
        raise GroupServiceException(f"Failed to edit group: {str(e)}")


def get_group(group_id: int) -> Group:
    repo = GroupRepository()
    group = repo.get_by_id(group_id)
    return group

def get_user_groups(user_id: int) -> List[Group]:
    repo = GroupRepository()
    groups = repo.get_user_groups(user_id)
    return groups

def get_group_members(group_id: int) -> List[User]:
    repo = GroupRepository()
    members = repo.get_group_members(group_id)
    return members

def get_all_bills(group_id: int) -> List[Bill]:
    repo = BillRepository()
    bills = repo.get_all_bills(group_id)
    return bills





