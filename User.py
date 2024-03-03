class User:
    # email: str
    # phone: str
    # password: str
    # name: str
    # city: str

    def __init__(self, email, phone, password, name, city):
        self.email = email
        self.phone = phone
        self.password = password
        self.name = name
        self.city = city


user_list: [User]


def add_user(email, phone, password, name, city):
    new_user = User(email, phone, password, name, city)
    for user in user_list:
        if user.email == email:
            return -1
    user_list.append(new_user)
    return 1
