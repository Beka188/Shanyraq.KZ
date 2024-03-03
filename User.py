from sqlalchemy import create_engine, ForeignKey, Column, String
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.orm.exc import NoResultFound

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


def user_exists(email, phone):
    try:
        existing_user = session.query(User).filter(User.email == email).one()
        return existing_user.email == email
    except NoResultFound:
        return False


def add_user(email, phone, password, name, city):
    user = User(email, phone, password, name, city)
    if not user_exists(email, phone):
        session.add(user)
        session.commit()
        return 200
    else:
        return 201  # ? User already exists
