from Splity.adapters.repository import (
    BillParticipantRepository,
    BillRepository,
    GroupRepository,
    UserRepository,
)
from Splity.domainmodel.models import User
from Splity.services import bill_services, groups_services


def _add_user(user_repo, name, username, email, password="Pass123"):
    return user_repo.add(User(name=name, username=username, email=email, password=password))


def test_add_bill_creates_participants_and_splits(app):
    user_repo = UserRepository()
    group_repo = GroupRepository()

    user1_id = _add_user(user_repo, "User One", "user1", "user1@test.com")
    user2_id = _add_user(user_repo, "User Two", "user2", "user2@test.com")

    groups_services.create_group("Bills", "Group", "USD", user1_id)
    group = group_repo.get_by_name_and_creator("Bills", user1_id)

    group_repo.join_by_code(user2_id, group.invite_code)

    members = group_repo.get_group_members(group.id)
    owe_members = [member.id for member in members]

    bill_services.add_bill_service(user1_id, "Dinner", 30, owe_members, group.id)

    bill_repo = BillRepository()
    bill = bill_repo.get_bill_by_name_and_group_id("Dinner", group.id)
    participants = BillParticipantRepository().all_participants_in_group(bill.id)

    assert len(participants) == len(members)
    assert all(p.amount_owed == 15 for p in participants)


def test_settling_algorithm_returns_balances(app):
    user_repo = UserRepository()
    group_repo = GroupRepository()

    user1_id = _add_user(user_repo, "User One", "user1", "user1@test.com")
    user2_id = _add_user(user_repo, "User Two", "user2", "user2@test.com")

    groups_services.create_group("Settle", "Group", "USD", user1_id)
    group = group_repo.get_by_name_and_creator("Settle", user1_id)
    group_repo.join_by_code(user2_id, group.invite_code)

    members = group_repo.get_group_members(group.id)
    owe_members = [member.id for member in members]

    bill_services.add_bill_service(user1_id, "Pizza", 20, owe_members, group.id)

    settlements, net_balances = bill_services.settling_algorithm(group.id)

    assert "User One" in [item[0] for item in net_balances.values()]
    assert "User Two" in [item[0] for item in net_balances.values()]
    assert any(
        settlement[0] == "User Two" and settlement[2] == "User One"
        for settlement in settlements
    )
