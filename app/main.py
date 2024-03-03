from sqlalchemy import create_engine, ForeignKey, Column, String
from sqlalchemy.orm import sessionmaker, declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    email = Column("email", String, primary_key=True)
    phone = Column("phone", String)
    password = Column("password", String)
    name = Column("name", String)
    city = Column("city", String)

    def __init__(self, email, phone, password, name, city):
        self.email = email
        self.phone = phone
        self.password = password
        self.name = name
        self.city = city

    def __repr__(self):
        return f"{self.email}\n{self.phone}\n{self.password}\n{self.name}\n{self.city}"


engine = create_engine("sqlite:///ShanyraqDB.db", echo=True)
Base.metadata.create_all(bind=engine)  # creates table(s)
Session = sessionmaker(bind=engine)  # class
session = Session()  # its instance

user1 = User("aa", "+7 705 213 40 12", "pass", "Beka", "Astana")
user2 = User("ss", "+7 777 102 31 10", "word", "Maks", "Almaty")
user3 = User("dd", "+7 705 942 21 10", "pw", "Samat", "Almaty")
user4 = User("ff", "+7 705 921 92 94", "fd", "Olzhas", "Pavlodar")

session.add(user1)
session.add(user2)
session.add(user3)
session.add(user4)
session.commit()
find = session.query(User).filter(User.email == 'ss')
print(f"\n\nresult:")
for f in find:
    print(f)
print(len(find))


# @app.post("/auth/users")
# def sign_up(email: str = Form(...), phone: str = Form(...), password: str = Form(...), name: str = Form(...),
#             city: str = Form(...)):
#     adding_user = add_user(email, phone, password, name, phone)
#     if adding_user == -1:
#         return {"User already registered!"}
#     return {"User1"}


# if __name__ == '__main__':
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)
