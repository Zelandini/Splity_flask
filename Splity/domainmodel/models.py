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
    def __init__(self, bill_id: int, user_id: int, description: str, created_date: datetime):
        self.__bill_id = bill_id
        self.__user_id = user_id
        self.__description = description
        self.__data = created_date if created_date else datetime.now()

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
        return self.__data

    def __repr__(self):
        return f"<Bill {self.id}: {self.user_id}: {self.description}>"



class BillParticipant:
    def __init__(self, bill_id: int, user_id: int, amount_owed: float, has_paid: bool):
        self.__bill_id = bill_id
        self.__user_id = user_id
        self.__amount_owed = amount_owed
        self.__has_paid = has_paid

