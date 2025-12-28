# /Splity_flask/Splity/services/bill_services.py
from typing import List

from Splity.adapters.repository import GroupRepository, UserRepository, BillRepository, BillParticipantRepository
from Splity.domainmodel.models import Group, Bill


class BillServiceException:
    pass

# def add_bill(description: str, amount: float, owe_members:List[int], group_id: int) -> Bill:
#     bill_repo = BillRepository()
#     bill = bill_repo.get_by_id()
#     bill_participant_repo = BillParticipantRepository()
#     group_repo = GroupRepository()
#     group_participant_repo = UserRepository()
#     if bill_repo:
#         raise GroupServiceException(f"You already have a bill with the same description '{name}'.")
#     if not name or not name.strip():
#         raise GroupServiceException("Group name cannot be empty.")
#     try:
#         new_group = Group(name=name, description=description, currency=currency, creator_id=creator_id)
#         repo.add(new_group)
#         return new_group
#     except Exception as e:
#         raise GroupServiceException(f"Failed to create group: {str(e)}")



