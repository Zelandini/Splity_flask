from typing import Optional
from werkzeug.security import generate_password_hash, check_password_hash
from Splity.adapters.repository import UserRepository
from Splity.domainmodel.models import User

class AuthenticationException(Exception): pass

def add_user_service(name,username,email,password):
    repo=UserRepository()
    if repo.get_by_username(username): raise AuthenticationException(f"User {username} already exists")
    if repo.get_by_email(email): raise AuthenticationException("An account already uses this email.")
    user=User(name=name,username=username,email=email,password=generate_password_hash(password))
    return repo.add(user)

def add_google_user_service(name,email,google_sub):
    repo=UserRepository()
    existing=repo.get_by_google_sub(google_sub)
    if existing: return existing
    if repo.get_by_email(email): raise AuthenticationException("This email is already linked to another account.")
    base=(email.split("@")[0].lower().replace(".","_") or "user")[:60]
    username=base; suffix=1
    while repo.get_by_username(username):
        suffix+=1; username=f"{base}_{suffix}"
    user=User(name=name.strip(),username=username,email=email,password=None,google_sub=google_sub)
    user_id=repo.add(user)
    return repo.get_by_id(user_id)

def authenticate_user_service(username,password)->Optional[User]:
    user=UserRepository().get_by_username(username)
    if not user or not user.password or not check_password_hash(user.password,password):
        raise AuthenticationException("Invalid username or password.")
    return user
