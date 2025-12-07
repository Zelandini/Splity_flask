from datetime import datetime

class User:
    def __init__(self, user_id: int, name: str, username: str, email: str, password: str = None):
        self.__id = user_id
        self.__name = name
        self.__username = username
        self.__email = email
        self.__password = password

    @property
    def id(self):
        return self.__id

    @property
    def name(self):
        return self.__name

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    @property
    def username(self):
        return self.__username

    @property
    def email(self):
        return self.__email

    @property
    def password(self):
        return self.__password

    def __repr__(self):
        return f"<User {self.id}: {self.username}>"


class Bill:
    def __init__(self, bill_id: int, user_id: int, description: str, created_date: datetime, amount: float):
        self.__bill_id = bill_id
        self.__user_id = user_id
        self.__description = description
        self.__amount = amount
        self.__date = created_date if created_date else datetime.now()

    @property
    def id(self):
        return self.__bill_id

    @property
    def user_id(self):
        return self.__user_id

    @property
    def description(self):
        return self.__description

    @property
    def date(self):
        return self.__date

    @property  # ← FIXED: Added @property
    def amount(self):
        return self.__amount

    def __repr__(self):
        return f"<Bill {self.id}: {self.date}: {self.user_id}>"


class BillParticipant:
    def __init__(self, participant_id: int, bill_id: int, user_id: int, amount_owed: float, has_paid: bool):
        self.__id = participant_id
        self.__bill_id = bill_id
        self.__user_id = user_id
        self.__amount_owed = amount_owed
        self.__has_paid = has_paid

    @property
    def id(self):
        return self.__id

    @property
    def bill_id(self):
        return self.__bill_id

    @property  # ← FIXED: Changed from id to bill_id
    def bill_id(self):
        return self.__bill_id

    @property
    def user_id(self):
        return self.__user_id

    @property
    def amount_owed(self):
        return self.__amount_owed

    @property
    def has_paid(self):
        return self.__has_paid

    def __repr__(self):
        return f"<BillParticipant bill:{self.bill_id} user:{self.user_id}>"