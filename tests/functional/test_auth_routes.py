
def test_register_duplicate_username_shows_error(client, register_user):
    register_user()
    response = register_user(email="other@test.com")
    page_output = response.get_data(as_text=True).lower()
    assert "already exists" in page_output


def test_login_invalid_password_shows_error(client, register_user, login_user):
    register_user()
    response = login_user(password="WrongPassword123")
    page_output = response.get_data(as_text=True).lower()
    assert "invalid username or password" in page_output


def test_authenticated_user_redirected_from_login_and_register(client, register_user, login_user):
    register_user()
    login_user()

    login_response = client.get("/login", follow_redirects=True)
    register_response = client.get("/register", follow_redirects=True)

    assert login_response.request.path == "/"
    assert register_response.request.path == "/"
