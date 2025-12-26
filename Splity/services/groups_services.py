# /Splity_flask/Splity/services/groups_services.py


from Splity.adapters.repository import GroupRepository
from Splity.domainmodel.models import Group

class GroupServiceException(Exception):
    pass


def create_group(name: str, description: str, currency: str, creator_id: int) -> Group:
    repo = GroupRepository()
    existing_group = repo.get_by_and_membership(name, creator_id)
    print(existing_group)
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

