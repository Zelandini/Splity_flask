from Splity.adapters.repository import GroupRepository, UserRepository, BillRepository, BillParticipantRepository
from Splity.domainmodel.models import Group

class GroupServiceException(Exception): pass

def create_group(name,description,currency,creator_id):
    repo=GroupRepository()
    if repo.get_by_name_and_membership(name,creator_id): raise GroupServiceException(f"You already have a group named '{name}'.")
    group=Group(name.strip(),description.strip(),currency,creator_id)
    repo.add(group)
    return repo.get_by_invite_code(group.invite_code)

def get_group_details(group_id,user_id):
    repo=GroupRepository(); group=repo.get_by_id(group_id)
    if not group: raise GroupServiceException("Group not found.")
    members=repo.get_group_members(group_id)
    if user_id not in {member.id for member in members}: raise GroupServiceException(f"You are not in Group {group.name}.")
    return group,members

def join_group(invite_code,user_id):
    code=invite_code.strip().upper()
    if len(code)!=6: raise GroupServiceException("Invalid invite code format.")
    repo=GroupRepository()
    if not repo.join_by_code(user_id,code): raise GroupServiceException("Invalid invite code or you are already in this group.")
    return repo.get_by_invite_code(code)

def _require_zero_balance(group_id,user_id):
    from Splity.services import bill_services
    _,balances=bill_services.settling_algorithm(group_id)
    balance=balances.get(user_id,["",0])[1]
    if abs(balance)>.005:
        raise GroupServiceException(f"This member cannot leave yet because their balance is {balance:.2f}. Settle and confirm all repayments first.")

def leave_from_group(group_id,user_id):
    group,members=get_group_details(group_id,user_id)
    if user_id==group.creator_id: raise GroupServiceException("The group owner cannot leave or transfer ownership.")
    _require_zero_balance(group_id,user_id)
    GroupRepository().remove_member(group_id,user_id)
    return UserRepository().get_by_id(user_id),group

def remove_user(group_id,user_id,requester_id):
    group,members=get_group_details(group_id,requester_id)
    if group.creator_id!=requester_id: raise GroupServiceException("Only the group owner can remove members.")
    if user_id==group.creator_id: raise GroupServiceException("The owner cannot be removed.")
    if user_id not in {m.id for m in members}: raise GroupServiceException("User is not a member.")
    _require_zero_balance(group_id,user_id)
    user=UserRepository().get_by_id(user_id)
    GroupRepository().remove_member(group_id,user_id)
    return user

def delete_group(group_id,user_id):
    group,_=get_group_details(group_id,user_id)
    if user_id!=group.creator_id: raise GroupServiceException("Not authorised to delete this group.")
    GroupRepository().delete_group(group_id)
    return group

def edit_group(name,description,group_id,creator_id):
    repo=GroupRepository(); group=repo.get_by_id(group_id)
    if not group or group.creator_id!=creator_id: raise GroupServiceException("You are not allowed to edit this group.")
    duplicate=repo.get_by_name_and_membership(name,creator_id)
    if duplicate and duplicate.id!=group_id: raise GroupServiceException("You already belong to another group with this name.")
    group.name=name.strip(); group.description=description.strip()
    repo.edit_group_name(group_id,group.name); repo.edit_group_description(group_id,group.description)
    return group

def get_group(group_id): return GroupRepository().get_by_id(group_id)
def get_user_groups(user_id): return GroupRepository().get_user_groups(user_id)
def get_group_members(group_id): return GroupRepository().get_group_members(group_id)
def get_all_bills(group_id): return BillRepository().get_all_bills(group_id)
def get_bill(bill_id): return BillRepository().get_by_id(bill_id)
def get_bill_participants(bill_id): return BillParticipantRepository().all_participants_in_group(bill_id)
