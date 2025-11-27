
class User:
    def __init__(self, user_id: int, name: str, username: str, email: str, password: str = None):
        self.__id = user_id
        self.__name = name
        self.__username = username
        self.__email = email
        self.__password = password
        self.__bills = []

    @property
    def id(self, user_id: int):
        if user_id is not None and (type(user_id) is not int or user_id < 0):
            raise ValueError("User ID must be a positive integer or None")
        self.__id = user_id

    @property
    def name(self, name: str):
        self.__name = name

    @property
    def username(self, username: str):
        self.__username = username

    @property
    def email(self, email: str):
        self.__email = email

    @property
    def password(self, password: str):
        self.__password = password

    def __repr__(self):
        return f"<User {self.id}: {self.username}>"
