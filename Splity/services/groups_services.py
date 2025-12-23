from Splity.adapters.repository import GroupRepository
from Splity.domainmodel.models import Group


class GroupServiceException(Exception):
    pass


def create_group(name: str, description: str, currency: str, creator_id: int) -> Group:
    repo = GroupRepository()
    existing_group = repo.get_by_name_and_creator(name, creator_id)
    if existing_group:
        raise GroupServiceException(f"You already have a group named '{name}'.")
    if not name or not name.strip():
        raise GroupServiceException("Group name cannot be empty.")
    new_group = Group(name=name, description=description, currency=currency, creator_id=creator_id)
    repo.add(new_group)
    return new_group