from Splity.adapters.repository import UserRepository, GroupRepository, BillParticipantRepository
from Splity.domainmodel.models import User
from Splity.services import groups_services, bill_services

def add_user(name,username):
    return UserRepository().add(User(name=name,username=username,email=f"{username}@test.com",password="x"))

def test_custom_split_edit_and_confirmed_repayment(app):
    owner=add_user("Owner","owner"); alex=add_user("Alex","alex"); mia=add_user("Mia","mia")
    group=groups_services.create_group("Trip","Friends","NZD",owner)
    repo=GroupRepository(); repo.join_by_code(alex,group.invite_code); repo.join_by_code(mia,group.invite_code)
    bill=bill_services.add_bill_service(owner,"Dinner",60,[owner,mia],group.id,payer_id=alex,split_mode="custom",custom_amounts={owner:20,mia:40})
    shares=BillParticipantRepository().all_participants_in_group(bill.id)
    assert {p.user_id:p.amount_owed for p in shares}=={owner:20.0,mia:40.0}
    _,before=bill_services.settling_algorithm(group.id)
    assert before[alex][1]==60 and before[owner][1]==-20 and before[mia][1]==-40
    repayment_id=bill_services.record_repayment(group.id,mia,alex,40)
    _,pending=bill_services.settling_algorithm(group.id); assert pending[mia][1]==-40
    bill_services.confirm_repayment(repayment_id,alex)
    _,confirmed=bill_services.settling_algorithm(group.id)
    assert confirmed[mia][1]==0 and confirmed[alex][1]==20
    bill_services.edit_bill_service(bill.id,owner,"Dinner updated",30,[owner,alex],owner,"equal")
    edited=groups_services.get_bill(bill.id)
    assert edited.description=="Dinner updated" and edited.amount==30

def test_member_with_balance_cannot_leave(app):
    owner=add_user("Owner","owner"); alex=add_user("Alex","alex")
    group=groups_services.create_group("Flat","Bills","NZD",owner)
    GroupRepository().join_by_code(alex,group.invite_code)
    bill_services.add_bill_service(owner,"Power",20,[owner,alex],group.id)
    try:
        groups_services.leave_from_group(group.id,alex)
        assert False,"Expected a balance guard"
    except groups_services.GroupServiceException as error:
        assert "cannot leave" in str(error).lower()
