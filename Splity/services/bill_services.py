from decimal import Decimal, ROUND_DOWN
from Splity.adapters.repository import BillRepository, BillParticipantRepository, UserRepository, GroupRepository, RepaymentRepository
from Splity.domainmodel.models import Bill

class BillServiceException(Exception):
    pass

def _member_ids(group_id):
    return {member.id for member in GroupRepository().get_group_members(group_id)}

def _require_member(group_id, user_id):
    if user_id not in _member_ids(group_id):
        raise BillServiceException("You are not a member of this group.")

def _normalise_shares(amount, participant_ids, split_mode, custom_amounts=None):
    ids=list(dict.fromkeys(int(i) for i in participant_ids))
    if not ids:
        raise BillServiceException("Select at least one person.")
    total=Decimal(str(amount)).quantize(Decimal("0.01"))
    if total <= 0:
        raise BillServiceException("Amount must be greater than zero.")
    if split_mode == "equal":
        base=(total/len(ids)).quantize(Decimal("0.01"),rounding=ROUND_DOWN)
        shares={uid:base for uid in ids}
        shares[ids[-1]] += total-sum(shares.values())
    else:
        custom_amounts=custom_amounts or {}
        try:
            shares={uid:Decimal(str(custom_amounts[uid])).quantize(Decimal("0.01")) for uid in ids}
        except (KeyError,TypeError,ValueError):
            raise BillServiceException("Enter a custom amount for every selected person.")
        if any(value < 0 for value in shares.values()):
            raise BillServiceException("Custom amounts cannot be negative.")
        if sum(shares.values()) != total:
            raise BillServiceException("Custom amounts must add up to the total expense.")
    return {uid:float(value) for uid,value in shares.items()}

def add_bill_service(user_id, description, amount, owe_members, group_id, payer_id=None, split_mode="equal", custom_amounts=None):
    _require_member(group_id,user_id)
    members=_member_ids(group_id)
    payer_id=int(payer_id or user_id)
    participant_ids=[int(i) for i in owe_members]
    if payer_id not in members or not set(participant_ids).issubset(members):
        raise BillServiceException("The payer and participants must belong to this group.")
    if BillRepository().get_bill_by_name_and_group_id(description,group_id):
        raise BillServiceException(f"An expense named '{description}' already exists in this group.")
    shares=_normalise_shares(amount,participant_ids,split_mode,custom_amounts)
    bill=Bill(user_id=payer_id,created_by_id=user_id,description=description.strip(),amount=float(amount),group_id=group_id)
    bill_id=BillRepository().create(bill)
    BillParticipantRepository().replace_participants(bill_id,shares)
    return BillRepository().get_by_id(bill_id)

def edit_bill_service(bill_id, requester_id, description, amount, participant_ids, payer_id, split_mode="equal", custom_amounts=None):
    bill=BillRepository().get_by_id(bill_id)
    if not bill:
        raise BillServiceException("Expense not found.")
    _require_member(bill.group_id,requester_id)
    group=GroupRepository().get_by_id(bill.group_id)
    if requester_id not in {bill.created_by_id,group.creator_id}:
        raise BillServiceException("Only the person who recorded this expense or the group owner can edit it.")
    members=_member_ids(bill.group_id)
    ids=[int(i) for i in participant_ids]
    if int(payer_id) not in members or not set(ids).issubset(members):
        raise BillServiceException("The payer and participants must belong to this group.")
    duplicate=BillRepository().get_bill_by_name_and_group_id(description,bill.group_id)
    if duplicate and duplicate.id != bill.id:
        raise BillServiceException("Another expense already uses that description.")
    shares=_normalise_shares(amount,ids,split_mode,custom_amounts)
    BillRepository().update(bill.id,int(payer_id),description.strip(),float(amount))
    BillParticipantRepository().replace_participants(bill.id,shares)
    return BillRepository().get_by_id(bill.id)

def delete_bill_service(bill_id,current_user_id,group_id):
    bill=BillRepository().get_by_id(bill_id)
    group=GroupRepository().get_by_id(group_id)
    if not bill or bill.group_id != group_id:
        raise BillServiceException("Expense not found.")
    _require_member(group_id,current_user_id)
    if current_user_id not in {bill.created_by_id,group.creator_id}:
        raise BillServiceException("User not authorised to delete expense.")
    BillRepository().delete_bill(bill_id)
    return bill

def get_bills_and_creators_service(group_id):
    repo=UserRepository()
    return [(bill,repo.get_by_id(bill.user_id)) for bill in BillRepository().get_all_bills(group_id)]

def total_group_spending(group_id):
    return round(sum(bill.amount for bill in BillRepository().get_all_bills(group_id)),2)

def calculate_net_balance(users,bills,participants):
    balances={user.id:[user.name,0.0] for user in users}
    for bill in bills:
        if bill.user_id in balances: balances[bill.user_id][1]+=bill.amount
    for participant in participants:
        if participant.user_id in balances: balances[participant.user_id][1]-=participant.amount_owed
    return balances

def settling_algorithm(group_id):
    users=GroupRepository().get_group_members(group_id)
    bills=BillRepository().get_all_bills(group_id)
    participant_repo=BillParticipantRepository()
    participants=[]
    for bill in bills: participants.extend(participant_repo.all_participants_in_group(bill.id))
    balances=calculate_net_balance(users,bills,participants)
    for payment in RepaymentRepository().get_confirmed_for_group(group_id):
        if payment.payer_id in balances: balances[payment.payer_id][1]+=payment.amount
        if payment.payee_id in balances: balances[payment.payee_id][1]-=payment.amount
    debtors=[[uid,data[0],-data[1]] for uid,data in balances.items() if data[1] < -0.005]
    creditors=[[uid,data[0],data[1]] for uid,data in balances.items() if data[1] > 0.005]
    settlements=[]
    i=j=0
    while i<len(debtors) and j<len(creditors):
        amount=round(min(debtors[i][2],creditors[j][2]),2)
        settlements.append((debtors[i][1],amount,creditors[j][1],debtors[i][0],creditors[j][0]))
        debtors[i][2]-=amount; creditors[j][2]-=amount
        if debtors[i][2] <= .005: i+=1
        if creditors[j][2] <= .005: j+=1
    return settlements,balances

def get_user_net_balances(balances,user_id):
    return balances.get(user_id,["Unknown",0.0])

def record_repayment(group_id,payer_id,payee_id,amount):
    _require_member(group_id,payer_id)
    _require_member(group_id,payee_id)
    if payer_id==payee_id: raise BillServiceException("You cannot repay yourself.")
    settlements,_=settling_algorithm(group_id)
    match=next((s for s in settlements if s[3]==payer_id and s[4]==payee_id),None)
    if not match: raise BillServiceException("There is no outstanding payment to this person.")
    amount=float(amount)
    if amount <= 0 or amount > match[1]+.005:
        raise BillServiceException(f"Amount must be between 0 and {match[1]:.2f}.")
    return RepaymentRepository().create(group_id,payer_id,payee_id,amount)

def confirm_repayment(repayment_id,current_user_id):
    repayment=RepaymentRepository().get_by_id(repayment_id)
    if not repayment: raise BillServiceException("Repayment not found.")
    if repayment.payee_id != current_user_id: raise BillServiceException("Only the receiver can confirm this repayment.")
    if repayment.status != "pending": raise BillServiceException("This repayment has already been processed.")
    RepaymentRepository().confirm(repayment_id)
    return repayment

def get_repayments(group_id):
    user_repo=UserRepository()
    return [(r,user_repo.get_by_id(r.payer_id),user_repo.get_by_id(r.payee_id)) for r in RepaymentRepository().get_for_group(group_id)]
