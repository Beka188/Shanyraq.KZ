from sqlalchemy import create_engine, Column, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import bcrypt

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
        self.password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        self.name = name
        self.city = city

    def __repr__(self):
        return f"{self.email} {self.phone} {self.password} {self.name} {self.city}"

    def verify_password(self, password):
        return bcrypt.checkpw(password.encode(), self.password.encode('utf-8'))


def add_user(email, phone, password, name, city):
    if not user_exists(email):
        user = User(email, phone, password, name, city)
        session.add(user)
        session.commit()
        return 200
    else:
        return 409


engine = create_engine("sqlite:///ShanyraqDB.db", echo=True)
Base.metadata.create_all(bind=engine)
Session = sessionmaker(bind=engine)
session = Session()


def print_all():
    print("PRINTING:\n\n")
    users = session.query(User).all()
    print(len(users))
    for user in users:
        print(user.__repr__())


def login(email, password):
    user = session.query(User).filter(User.email == email).first()
    if user:
        return user.verify_password(password)
    return False


def user_exists(email):
    return session.query(User).filter(User.email == email).count() > 0
