# /Splity_flask/Splity/services/bill_services.py
from typing import List
from collections import defaultdict

from Splity.adapters.orm import BillParticipantORM
from Splity.adapters.repository import BillRepository, BillParticipantRepository, UserRepository, GroupRepository
from Splity.domainmodel.models import Bill, User, BillParticipant
from Splity.services import groups_services


class BillServiceException(Exception):
    pass

def add_bill_service(user_id: int,description: str, amount: float, owe_members:List[int], group_id: int) -> Bill:
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

def delete_bill_service(bill_id: int, current_user_id: int, group_id: int) -> Bill:
    bill_repo = BillRepository()
    bill = bill_repo.get_by_id(bill_id)
    if not bill:
        raise BillServiceException(f"Bill with id {bill_id} does not exist.")
    group_repo = GroupRepository()
    group = group_repo.get_by_id(group_id)
    if current_user_id != bill.user_id:
        if current_user_id != group.creator_id:
            raise BillServiceException(f"User not authorised to delete bill.")
    try:
        success = bill_repo.delete_bill(bill_id=bill.id)
        if not success:
            raise BillServiceException("Bill was not deleted.")
        return bill
    except Exception as e:
        raise BillServiceException(f"Failed to delete bill: {str(e)}")

def get_user_by_id_service(user_id: int) -> User:
    user_repo = UserRepository()
    user = user_repo.get_by_id(user_id)
    return user

def get_bills_and_creators_service(group_id: int):
    bills = groups_services.get_all_bills(group_id)
    bill_data = []
    for bill in bills:
        creator = get_user_by_id_service(bill.user_id)
        bill_data.append((bill, creator))
    return bill_data

def total_group_spending(group_id: int):
    bills = groups_services.get_all_bills(group_id)
    total = sum([bill.amount for bill in bills])
    print(total)
    return total

def total_user_spending(group_id: int, user_id: int):
    bills_repo = BillRepository()
    bills = bills_repo.get_all_bills_in_group_by_user(group_id, user_id)
    if not bills:
        return 0
    return sum([bill.amount for bill in bills])

def get_all_bill_participants_service(bill_id: int):
    bills_repo = BillParticipantRepository()
    bill_participants = bills_repo.all_participants_in_group(bill_id)
    if not bill_participants:
        return []
    return bill_participants


def get_user_net_balances(users_net_balance: dict, user_id: int) -> dict:
    if users_net_balance[user_id]:
        return users_net_balance[user_id]
    return {}



def calculate_net_balance(users, bills, participants):
    user_balances = {user.id: [user.name, 0.0] for user in users}
    for bill in bills:
        if bill.user_id in user_balances:
            user_balances[bill.user_id][1] += bill.amount
    for participant in participants:
        if participant.user_id in user_balances:
            user_balances[participant.user_id][1] -= participant.amount_owed
    return user_balances


def settling_algorithm(group_id: int):
    users = groups_services.get_group_members(group_id)
    bills = groups_services.get_all_bills(group_id)
    participants = []
    for bill in bills:
        participants += get_all_bill_participants_service(bill.id)
    final_dict = calculate_net_balance(users, bills, participants)
    net_balances = final_dict
    balances = {item[0]: item[1] for item in final_dict.values()}
    texts = []
    while max(balances.values()) > 0.01:
        debtor_name, debtor_bal = min(balances.items(), key=lambda x: x[1])
        creditor_name, creditor_bal = max(balances.items(), key=lambda x: x[1])
        amount_to_transfer = min(abs(debtor_bal), creditor_bal)
        balances[debtor_name] += amount_to_transfer
        balances[creditor_name] -= amount_to_transfer
        texts.append([debtor_name, round(amount_to_transfer, 2), creditor_name])
    return texts, net_balances
