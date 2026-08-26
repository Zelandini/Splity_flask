import secrets
from datetime import datetime, timezone
from typing import Optional

class User:
    def __init__(self, name, username, email, password=None, user_id=None, google_sub=None):
        self.__id=user_id; self.__name=name; self.__username=username; self.__email=email
        self.__password=password; self.__google_sub=google_sub; self.__groups=[]
    @property
    def id(self): return self.__id
    def get_id(self): return str(self.__id)
    @property
    def name(self): return self.__name
    @property
    def username(self): return self.__username
    @property
    def email(self): return self.__email
    @property
    def password(self): return self.__password
    @property
    def google_sub(self): return self.__google_sub
    @property
    def is_authenticated(self): return True
    @property
    def is_active(self): return True
    @property
    def is_anonymous(self): return False
    @property
    def groups(self): return self.__groups
    def add_group(self, group): self.__groups.append(group)
    def set_name(self, name): self.__name=name
    def set_username(self, username): self.__username=username
    def set_email(self, email): self.__email=email
    def set_password(self, password): self.__password=password
    def __repr__(self): return f"<User {self.id}: {self.username}>"

class Bill:
    def __init__(self, user_id, description, amount, created_date=None, bill_id=None, group_id=None, created_by_id=None):
        self.__bill_id=bill_id; self.__user_id=user_id; self.__created_by_id=created_by_id or user_id
        self.__description=description; self.__amount=amount
        self.__date=created_date or datetime.now(timezone.utc); self.__group_id=group_id
    @property
    def id(self): return self.__bill_id
    @property
    def user_id(self): return self.__user_id
    @property
    def created_by_id(self): return self.__created_by_id
    @property
    def description(self): return self.__description
    @property
    def date(self): return self.__date
    @property
    def amount(self): return self.__amount
    @property
    def group_id(self): return self.__group_id
    @date.setter
    def date(self, value): self.__date=value

class BillParticipant:
    def __init__(self, bill_id, user_id, amount_owed, participant_id=None):
        self.__id=participant_id; self.__bill_id=bill_id; self.__user_id=user_id; self.__amount_owed=amount_owed
    @property
    def id(self): return self.__id
    @property
    def bill_id(self): return self.__bill_id
    @property
    def user_id(self): return self.__user_id
    @property
    def amount_owed(self): return self.__amount_owed

class Group:
    def __init__(self, name, description, currency, creator_id=None, group_id=None, invite_code=None):
        self.__id=group_id; self.__name=name; self.__description=description; self.__creator_id=creator_id
        self.__currency=currency; self.__invite_code=invite_code or secrets.token_hex(3).upper()
    @property
    def id(self): return self.__id
    @property
    def name(self): return self.__name
    @property
    def invite_code(self): return self.__invite_code
    @property
    def currency(self): return self.__currency
    @property
    def creator_id(self): return self.__creator_id
    @property
    def description(self): return self.__description
    @name.setter
    def name(self, value): self.__name=value
    @description.setter
    def description(self, value): self.__description=value
