# /Splity_flask/Splity/services/bill_services.py
from typing import List

from Splity.adapters.repository import BillRepository, BillParticipantRepository, UserRepository, GroupRepository
from Splity.domainmodel.models import Bill, User
from Splity.services import groups_services


class BillServiceException(Exception):
    pass

def add_bill(user_id: int,description: str, amount: float, owe_members:List[int], group_id: int) -> Bill:
    bill_repo = BillRepository()
    bill = bill_repo.get_bill_by_name_and_group_id(description, group_id)
    bill_participant_repo = BillParticipantRepository()
    if bill:
        if description.lower() == bill.description.lower():
            raise BillServiceException(f"You already have a bill with the same description '{bill.description}'.")
    if not description or not description.strip():
        raise BillServiceException("Bill description cannot be empty.")
    try:
        new_bill = Bill(user_id=user_id, description=description, amount=amount, group_id=group_id)
        # FIX 1: Capture the ID returned by the database
        created_bill_id = bill_repo.create(new_bill)

        # FIX 2: Use the new ID to fetch the date and properties from the DB
        # This also avoids the 'NoneType' has no attribute 'date' error
        saved_bill = bill_repo.get_by_id(created_bill_id)

        # FIX 3: Use the captured ID when adding participants
        split_amount = amount / len(owe_members) if owe_members else 0
        for participant_id in owe_members:
            bill_participant_repo.add_participant(bill_id=saved_bill.id,
                                                  user_id=participant_id,
                                                  amount_owed=split_amount)
        return new_bill
    except Exception as e:
        raise BillServiceException(f"Failed to create group: {str(e)}")

def delete_bill_serive(bill_id: int, current_user_id: int, group_id: int) -> Bill:
    bill_repo = BillRepository()
    bill = bill_repo.get_by_id(bill_id)
    if not bill:
        raise BillServiceException(f"Bill with id {bill_id} does not exist.")
    group_repo = GroupRepository()
    group = group_repo.get_by_id(group_id)
    if current_user_id != bill.user_id or current_user_id != group.creator_id:
        raise BillServiceException(f"User not authorised to delete bill.")
    try:
        success = bill_repo.delete_bill_repo(bill_id=bill.id)
        if not success:
            raise BillServiceException("Bill was not deleted.")
        return bill
    except Exception as e:
        raise BillServiceException(f"Failed to delete bill: {str(e)}")

def get_user_by_id(user_id: int) -> User:
    user_repo = UserRepository()
    user = user_repo.get_by_id(user_id)
    return user