
from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import bcrypt
import _json

Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column("email", String)
    phone = Column("phone", String)
    password = Column("password", String)
    name = Column("name", String)
    city = Column("city", String)

    def __init__(self, email, phone, password, name, city):
        # self.id = id_counter
        self.email = email
        self.phone = phone
        self.password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        self.name = name
        self.city = city

    def __repr__(self):
        return f"{self.id} {self.email} {self.phone} {self.name} {self.city}"

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


engine = create_engine("sqlite:///ShanyraqDB2.db", echo=True)
Base.metadata.create_all(bind=engine)
Session = sessionmaker(bind=engine)
session = Session()


def print_all():
    print("PRINTING ALL:\n\n")
    users = session.query(User).all()
    for user in users:
        print(user)


def login(email, password):
    user = session.query(User).filter(User.email == email).first()
    if user:
        return user.verify_password(password)
    return False


def user_exists(email):
    return session.query(User).filter(User.email == email).count() > 0


def get_user(email):
    user = session.query(User).filter(User.email == email).first()
    if user:
        return {
            "id": user.id,
            "email": user.email,
            "phone": user.phone,
            "name": user.name,
            "city": user.city
        }
    return None


def update(username, data: _json):
    user_data = session.query(User).filter(User.email == username).first()
    for key, value in data.items():
        setattr(user_data, key, value)
    session.commit()


def delete_all_data():
    session.query(User).delete()
    session.commit()

