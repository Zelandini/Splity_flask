import pytest
from Splity.services import groups_services
from Splity.adapters.repository import UserRepository


def test_add_user_hashes_password(app, client):
    client.post('/register', data={
        "name": "Bob", "username": "bob", "email": "bob@test.com",
        "password": "secret123", "password2": "secret123"
    }, follow_redirects=True)
    user = UserRepository().get_by_username("bob")
    assert user.password != "secret123"  # Must be hashed!


def test_create_group_duplicate_name_fails(app, client):
    # Setup: register a user via the HTTP endpoint
    client.post('/register', data={
        "name": "Bob", "username": "bob", "email": "bob@test.com",
        "password": "pass", "password2": "pass"
    }, follow_redirects=True)
    user = UserRepository().get_by_username("bob")

    # First creation works
    groups_services.create_group("Ski Trip", "Fun", "USD", user.id)

    # Second creation with same name should raise Exception
    with pytest.raises(groups_services.GroupServiceException) as exc:
        groups_services.create_group("Ski Trip", "Duplicate", "USD", user.id)
    assert "already have a group named" in str(exc.value)


def test_create_and_retrieve_group(app, client):
    # Create a user and a group via registration endpoint, then verify retrieval
    client.post('/register', data={
        "name": "Bob", "username": "bob", "email": "bob@test.com",
        "password": "pass", "password2": "pass"
    }, follow_redirects=True)
    user = UserRepository().get_by_username("bob")

    created = groups_services.create_group("Ski Trip", "Fun", "USD", user.id)

    # Ensure the group was created and can be looked up
    user_groups = groups_services.get_user_groups(user.id)
    assert any(g.name == "Ski Trip" for g in user_groups)
