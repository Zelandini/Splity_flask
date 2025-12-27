import pytest
from Splity.services import authentication_services
from Splity.adapters.repository import GroupRepository, UserRepository


def test_anonymous_user_cannot_create_group(client):
    """Anonymous users should be redirected to login page"""
    response = client.get('/create_group', follow_redirects=True)
    assert b"Please log in to access this page" in response.data


def test_create_group_success(authenticated_client):
    """Test that authenticated user can create a group"""
    response = authenticated_client.post('/create_group', data={
        "name": "Test Group",
        "description": "A test group",
        "currency": "USD"
    }, follow_redirects=True)

    assert response.status_code == 200
    page_output = response.get_data(as_text=True)

    assert "Test Group" in page_output
    assert "created" in page_output
    assert "Invite code:" in page_output


def test_join_group_with_valid_code(app, authenticated_client):
    """Test that a second user can join a group using invite code"""
    # 1. testuser creates a group
    response = authenticated_client.post('/create_group', data={
        "name": "Target Group",
        "description": "Join me",
        "currency": "USD"
    }, follow_redirects=True)

    assert response.status_code == 200

    # 2. Get the group from DB
    user_repo = UserRepository()
    group_repo = GroupRepository()
    user = user_repo.get_by_username("testuser")
    groups = group_repo.get_user_groups(user.id)

    assert len(groups) > 0, "The group was not found in the database!"
    group = groups[0]

    # 3. Logout and create a SECOND user
    authenticated_client.get('/logout', follow_redirects=True)

    with app.app_context():
        authentication_services.add_user("Second User", "seconduser", "second@test.com", "Password123")

    # Login as second user
    authenticated_client.post('/login', data={
        "username": "seconduser",
        "password": "Password123"
    }, follow_redirects=True)

    # 4. Second user joins the group
    response = authenticated_client.post('/join_group', data={
        "invite_code": group.invite_code
    }, follow_redirects=True)

    assert response.status_code == 200
    page_output = response.get_data(as_text=True)

    # Check for success message
    assert "Successfully joined Group" in page_output
    assert "Target Group" in page_output


def test_join_group_already_member(authenticated_client):
    """Test that joining a group you're already in shows appropriate message"""
    # 1. Create a group (creator is auto-added as member)
    authenticated_client.post('/create_group', data={
        "name": "My Group",
        "description": "Test",
        "currency": "USD"
    }, follow_redirects=True)

    # 2. Get the group
    user_repo = UserRepository()
    group_repo = GroupRepository()
    user = user_repo.get_by_username("testuser")
    groups = group_repo.get_user_groups(user.id)
    group = groups[0]

    # 3. Try to join again (already a member)
    response = authenticated_client.post('/join_group', data={
        "invite_code": group.invite_code
    }, follow_redirects=True)

    page_output = response.get_data(as_text=True)
    assert "already in this group" in page_output


def test_cannot_view_other_users_group(app, authenticated_client):
    """Test that users cannot view groups they're not members of"""
    # 1. testuser creates a group
    authenticated_client.post('/create_group', data={
        "name": "Secret Group",
        "description": "Private",
        "currency": "USD"
    }, follow_redirects=True)

    # Get the group ID
    user_repo = UserRepository()
    group_repo = GroupRepository()
    creator = user_repo.get_by_username("testuser")
    group = group_repo.get_user_groups(creator.id)[0]

    # 2. Logout and create a second user
    authenticated_client.get('/logout', follow_redirects=True)

    with app.app_context():
        authentication_services.add_user("Other User", "otheruser", "other@test.com", "Password123")

    # Login as second user
    authenticated_client.post('/login', data={
        "username": "otheruser",
        "password": "Password123"
    }, follow_redirects=True)

    # 3. Try to access testuser's group
    response = authenticated_client.get(f'/group/{group.id}', follow_redirects=True)

    page_output = response.get_data(as_text=True)
    assert f"You are not in Group {group.name}" in page_output
    # Should be redirected back home
    assert "Your Groups" in page_output


def test_access_non_existent_group(authenticated_client):
    """Test accessing a group that doesn't exist"""
    response = authenticated_client.get('/group/9999', follow_redirects=True)
    assert "Group not found" in response.get_data(as_text=True)


def test_join_group_invalid_code(authenticated_client):
    """Test joining with an invalid invite code"""
    response = authenticated_client.post('/join_group', data={
        "invite_code": "WRONG1"
    }, follow_redirects=True)

    page_output = response.get_data(as_text=True)
    # The service should return this message
    assert "Invalid invite code" in page_output


def test_join_group_invalid_code_format(authenticated_client):
    """Test that form validation works for codes that are too long"""
    # Send an invite code that's too long (> 10 characters)
    response = authenticated_client.post('/join_group', data={
        "invite_code": "LONG_INVALID_CODE"
    }, follow_redirects=True)

    page_output = response.get_data(as_text=True)
    # Check for the WTForms validation error
    assert "Field must be between 1 and 10 characters long" in page_output


def test_create_duplicate_group_name_fails(authenticated_client):
    """Test that creating a group with duplicate name fails"""
    # Create first group
    response1 = authenticated_client.post('/create_group', data={
        "name": "Repeat",
        "description": "First one",
        "currency": "USD"
    }, follow_redirects=True)

    assert response1.status_code == 200
    assert "created" in response1.get_data(as_text=True)

    # Try to create another group with same name
    response2 = authenticated_client.post('/create_group', data={
        "name": "Repeat",
        "description": "Second one",
        "currency": "EUR"
    }, follow_redirects=True)

    page_output = response2.get_data(as_text=True)
    # Check for the service error message
    assert "already have a group named" in page_output


def test_user_cannot_view_unjoined_group_details(app, authenticated_client):
    """Test that users can't view details of groups they haven't joined"""
    # 1. testuser creates a group
    authenticated_client.post('/create_group', data={
        "name": "Private Group",
        "description": "Exclusive",
        "currency": "USD"
    }, follow_redirects=True)

    # Get the group
    user_repo = UserRepository()
    group_repo = GroupRepository()
    user1 = user_repo.get_by_username("testuser")
    groups = group_repo.get_user_groups(user1.id)
    private_group = groups[0]

    # 2. Logout and create a second user
    authenticated_client.get('/logout', follow_redirects=True)

    with app.app_context():
        authentication_services.add_user("User Two", "usertwo", "two@test.com", "Password123")

    # Login as second user
    authenticated_client.post('/login', data={
        "username": "usertwo",
        "password": "Password123"
    }, follow_redirects=True)

    # 3. Try to access the private group
    response = authenticated_client.get(f'/group/{private_group.id}', follow_redirects=True)

    assert response.status_code == 200
    page_output = response.get_data(as_text=True)
    # Should see the "not in group" message
    assert "You are not in Group" in page_output


def test_different_users_can_create_groups_with_same_name(app, authenticated_client):
    """Test that different users can create groups with the same name"""
    from Splity.services import authentication_services
    from Splity.adapters.repository import GroupRepository, UserRepository

    # 1. User1 (testuser) creates "Trip to Italy"
    response1 = authenticated_client.post('/create_group', data={
        "name": "Trip to Italy",
        "description": "Summer vacation",
        "currency": "EUR"
    }, follow_redirects=True)

    assert response1.status_code == 200
    assert "created" in response1.get_data(as_text=True)

    # Verify User1's group was created
    user_repo = UserRepository()
    group_repo = GroupRepository()
    user1 = user_repo.get_by_username("testuser")
    user1_groups = group_repo.get_user_groups(user1.id)
    assert len(user1_groups) == 1
    assert user1_groups[0].name == "Trip to Italy"
    user1_group_id = user1_groups[0].id

    # 2. Logout and create User2
    authenticated_client.get('/logout', follow_redirects=True)

    with app.app_context():
        authentication_services.add_user("User Two", "usertwo", "two@test.com", "Password123")

    authenticated_client.post('/login', data={
        "username": "usertwo",
        "password": "Password123"
    }, follow_redirects=True)

    # 3. User2 creates THEIR OWN "Trip to Italy" - should succeed!
    response2 = authenticated_client.post('/create_group', data={
        "name": "Trip to Italy",
        "description": "My own trip",
        "currency": "USD"
    }, follow_redirects=True)

    assert response2.status_code == 200
    page_output = response2.get_data(as_text=True)

    # Should succeed (different creator)
    assert "created" in page_output
    assert "Invite code:" in page_output

    # Verify User2's group was created
    user2 = user_repo.get_by_username("usertwo")
    user2_groups = group_repo.get_user_groups(user2.id)
    assert len(user2_groups) == 1
    assert user2_groups[0].name == "Trip to Italy"
    user2_group_id = user2_groups[0].id

    # Verify they are DIFFERENT groups
    assert user1_group_id != user2_group_id

    # Verify they have different invite codes
    assert user1_groups[0].invite_code != user2_groups[0].invite_code


def test_user_joins_group_then_creates_group_with_same_name(app, authenticated_client):
    """Test that a user can create their own group even if they're in another group with same name"""
    from Splity.services import authentication_services
    from Splity.adapters.repository import GroupRepository, UserRepository

    # 1. User1 (testuser) creates "Roommates"
    authenticated_client.post('/create_group', data={
        "name": "Roommates",
        "description": "Shared expenses",
        "currency": "USD"
    }, follow_redirects=True)

    # Get the invite code
    user_repo = UserRepository()
    group_repo = GroupRepository()
    user1 = user_repo.get_by_username("testuser")
    user1_group = group_repo.get_user_groups(user1.id)[0]
    invite_code = user1_group.invite_code

    # 2. Create and login as User2
    authenticated_client.get('/logout', follow_redirects=True)

    with app.app_context():
        authentication_services.add_user("User Two", "usertwo", "two@test.com", "Password123")

    authenticated_client.post('/login', data={
        "username": "usertwo",
        "password": "Password123"
    }, follow_redirects=True)

    # 3. User2 joins User1's "Roommates" group
    response = authenticated_client.post('/join_group', data={
        "invite_code": invite_code
    }, follow_redirects=True)

    assert "Successfully joined Group" in response.get_data(as_text=True)

    # 4. User2 creates THEIR OWN "Roommates" group - should succeed!
    response = authenticated_client.post('/create_group', data={
        "name": "Roommates",
        "description": "My different roommates",
        "currency": "EUR"
    }, follow_redirects=True)

    assert response.status_code == 200
    page_output = response.get_data(as_text=True)

    # Should succeed - User2 hasn't CREATED a "Roommates" group before
    # (they only JOINED one)
    assert "created" in page_output

    # Verify User2 is now in TWO groups both named "Roommates"
    user2 = user_repo.get_by_username("usertwo")
    user2_groups = group_repo.get_user_groups(user2.id)
    assert len(user2_groups) == 2

    # Both groups have same name but different creators
    assert all(g.name == "Roommates" for g in user2_groups)
    creators = {g.creator_id for g in user2_groups}
    assert len(creators) == 2  # Two different creators


def test_user_cannot_create_duplicate_group_they_already_created(authenticated_client):
    """Test that a user CANNOT create two groups with the same name"""
    from Splity.adapters.repository import GroupRepository, UserRepository

    # 1. Create first "My Group"
    response1 = authenticated_client.post('/create_group', data={
        "name": "My Group",
        "description": "First one",
        "currency": "USD"
    }, follow_redirects=True)

    assert "created" in response1.get_data(as_text=True)

    # 2. Try to create another "My Group"
    response2 = authenticated_client.post('/create_group', data={
        "name": "My Group",
        "description": "Second one",
        "currency": "EUR"
    }, follow_redirects=True)

    page_output = response2.get_data(as_text=True)

    # Should fail with error message
    assert "already have a group named" in page_output

    # Verify only one group was created
    user_repo = UserRepository()
    group_repo = GroupRepository()
    user = user_repo.get_by_username("testuser")
    user_groups = group_repo.get_user_groups(user.id)

    # Filter to only groups created by this user (not joined)
    created_groups = [g for g in user_groups if g.creator_id == user.id]
    my_groups = [g for g in created_groups if g.name == "My Group"]

    assert len(my_groups) == 1


def test_edit_group_success(authenticated_client, app):
    # 1. Arrange: Create a group first
    authenticated_client.post('/create_group', data={
        "name": "Original Name", "description": "Old", "currency": "USD"
    }, follow_redirects=True)

    with app.app_context():
        from Splity.adapters.repository import GroupRepository
        repo = GroupRepository()
        # Get the group we just made
        group = repo.get_all()[0]
        group_id = group.id

    # 2. Act: Send updated data to the edit route
    response = authenticated_client.post(f'/group/{group_id}/edit', data={
        "name": "Updated Name",
        "description": "New Description",
    }, follow_redirects=True)

    # 3. Assert: Check redirection and database update
    assert response.status_code == 200
    assert "Updated Name" in response.get_data(as_text=True)

    with app.app_context():
        updated_group = repo.get_by_id(group_id)
        assert updated_group.name == "Updated Name"
        assert updated_group.description == "New Description"


def test_non_creator_cannot_edit_group(app, authenticated_client):
    # 1. Arrange: 'testuser' creates a group
    authenticated_client.post('/create_group', data={
        "name": "Test Group", "description": "Owner only", "currency": "USD"
    })

    with app.app_context():
        from Splity.adapters.repository import GroupRepository
        group = GroupRepository().get_all()[0]
        group_id = group.id

    # 2. Arrange: Switch to a different user
    authenticated_client.get('/logout', follow_redirects=True)
    # (Assuming you have a helper to register/login a second user)
    # login_as_user(authenticated_client, "otheruser")

    # 3. Act: Try to edit 'testuser's group
    response = authenticated_client.post(f'/group/{group_id}/edit', data={
        "name": "Hacked Name"
    }, follow_redirects=True)

    # 4. Assert: Should redirect with an error message
    assert "You do not have permission" in response.get_data(as_text=True)

    # Double check the DB wasn't changed
    with app.app_context():
        original_group = GroupRepository().get_by_id(group_id)
        assert original_group.name == "Test Group"