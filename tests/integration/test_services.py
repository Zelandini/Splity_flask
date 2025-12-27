import pytest
from Splity.services import authentication_services, groups_services
from Splity.adapters.repository import UserRepository


def test_add_user_hashes_password(app):
    authentication_services.add_user("Bob", "bob", "bob@test.com", "secret123")
    user = UserRepository().get_by_username("bob")
    assert user.password != "secret123"  # Must be hashed!


def test_create_group_duplicate_name_fails(app):
    # Setup: Add a user
    authentication_services.add_user("Bob", "bob", "bob@test.com", "pass")
    user = UserRepository().get_by_username("bob")

    # First creation works
    groups_services.create_group("Ski Trip", "Fun", "USD", user.id)

    # Second creation with same name should raise Exception
    with pytest.raises(groups_services.GroupServiceException) as exc:
        groups_services.create_group("Ski Trip", "Duplicate", "USD", user.id)
    assert "already have a group named" in str(exc.value)


def test_edit_group(app):
    authentication_services.add_user("Bob", "bob", "bob@test.com", "pass")
    user = UserRepository().get_by_username("bob")

    groups_services.edit_group("Ski Trip", "Fun", user.id)