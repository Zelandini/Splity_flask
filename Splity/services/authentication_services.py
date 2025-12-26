# /Splity_flask/Splity/services/authentication_services.py


from typing import Optional
from werkzeug.security import generate_password_hash, check_password_hash

from Splity.adapters.repository import UserRepository
from Splity.domainmodel.models import User


class AuthenticationException(Exception):
    pass


def add_user(name: str, username: str, email: str, password: str):
    repo = UserRepository()
    if repo.get_by_username(username):
        raise AuthenticationException(f"User {username} already exists")

    hashed_password = generate_password_hash(password)
    user = User(name=name, username=username, email=email, password=hashed_password)
    repo.add(user)

def authenticate_user(username: str, password: str) -> Optional[User]:
    repo = UserRepository()
    user = repo.get_by_username(username)

    if user is None:
        raise AuthenticationException("User not found.")

    if not check_password_hash(user.password, password):
        raise AuthenticationException("Invalid password.")

    return user