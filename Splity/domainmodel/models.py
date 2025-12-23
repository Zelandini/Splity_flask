import secrets
from datetime import datetime
from typing import Optional


class User:
    def __init__(self, name: str, username: str, email: str, password: str = None, user_id: Optional[int] = None):
        self.__id = user_id
        self.__name = name
        self.__username = username
        self.__email = email
        self.__password = password
        self.__groups = []

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
    def is_authenticated(self): return True

    @property
    def is_active(self): return True

    @property
    def is_anonymous(self): return False

    @property
    def groups(self): return self.__groups

    def add_group(self, group):
        self.__groups.append(group)

    def __repr__(self):
        return f"<User {self.id}: {self.username}>"


class Bill:
    def __init__(self, user_id: int, description: str, amount: float, created_date: datetime = None,
                 bill_id: Optional[int] = None, group_id: Optional[int] = None):
        self.__bill_id = bill_id
        self.__user_id = user_id
        self.__description = description
        self.__amount = amount
        self.__date = created_date if created_date else datetime.now()
        self.__group_id = group_id

    @property
    def id(self): return self.__bill_id

    @property
    def user_id(self): return self.__user_id

    @property
    def description(self): return self.__description

    @property
    def date(self): return self.__date

    @property
    def amount(self): return self.__amount

    @property
    def group_id(self): return self.__group_id


class BillParticipant:
    def __init__(self, bill_id: int, user_id: int, amount_owed: float, has_paid: bool = False,
                 participant_id: Optional[int] = None):
        self.__id = participant_id
        self.__bill_id = bill_id
        self.__user_id = user_id
        self.__amount_owed = amount_owed
        self.__has_paid = has_paid

    @property
    def id(self): return self.__id

    @property
    def bill_id(self): return self.__bill_id

    @property
    def user_id(self): return self.__user_id

    @property
    def amount_owed(self): return self.__amount_owed

    @property
    def has_paid(self): return self.__has_paid


class Group:
    def __init__(self, name: str, description: str ,currency: str, creator_id: Optional[int] = None, group_id: int = None):
        self.__id = group_id
        self.__name = name
        self.__description = description
        self.__creator_id = creator_id
        self.__currency = currency
        self.__invite_code = secrets.token_hex(3).upper()

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