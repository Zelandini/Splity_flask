from Splity.adapters.repository import BillRepository, GroupRepository, UserRepository


def _group_members_choices(group_id: int):
    group_repo = GroupRepository()
    members = group_repo.get_group_members(group_id)
    return [f"{member.name} | @{member.username}" for member in members]


def test_create_bill_success(authenticated_client):
    authenticated_client.post('/create_group', data={
        "name": "Bills Group",
        "description": "Shared bills",
        "currency": "USD"
    }, follow_redirects=True)

    user_repo = UserRepository()
    group_repo = GroupRepository()
    creator = user_repo.get_by_username("testuser")
    group = group_repo.get_user_groups(creator.id)[0]

    response = authenticated_client.post(
        f'/group/{group.id}/create_bill',
        data={
            "description": "Dinner",
            "names": _group_members_choices(group.id),
            "amount": 42,
        },
        follow_redirects=True,
    )

    assert response.status_code == 200
    bill_repo = BillRepository()
    bill = bill_repo.get_bill_by_name_and_group_id("Dinner", group.id)
    assert bill is not None


def test_delete_bill_requires_creator_or_owner(authenticated_client):
    authenticated_client.post('/create_group', data={
        "name": "Delete Bill Group",
        "description": "Shared bills",
        "currency": "USD"
    }, follow_redirects=True)

    user_repo = UserRepository()
    group_repo = GroupRepository()
    creator = user_repo.get_by_username("testuser")
    group = group_repo.get_user_groups(creator.id)[0]

    authenticated_client.post(
        f'/group/{group.id}/create_bill',
        data={
            "description": "Snacks",
            "names": _group_members_choices(group.id),
            "amount": 12,
        },
        follow_redirects=True,
    )

    bill_repo = BillRepository()
    bill = bill_repo.get_bill_by_name_and_group_id("Snacks", group.id)

    authenticated_client.get('/logout', follow_redirects=True)
    authenticated_client.post('/register', data={
        "name": "Other User", "username": "otheruser",
        "email": "other@test.com", "password": "Password123",
        "password2": "Password123"
    }, follow_redirects=True)
    authenticated_client.post('/login', data={
        "username": "otheruser",
        "password": "Password123"
    }, follow_redirects=True)

    response = authenticated_client.get(
        f'/group/{group.id}/delete_bill/{bill.id}',
        follow_redirects=True,
    )

    assert "not authorised" in response.get_data(as_text=True).lower()
