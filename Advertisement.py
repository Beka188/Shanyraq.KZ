from sqlalchemy import create_engine, Column, String, Integer, Float
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import _json
class Addd:
    tip: str
    price: int
    address: str
    area: float
    rooms_count: int
    description: str

Base = declarative_base()


class Advertisement(Base):
    __tablename__ = "ads"
    id = Column("id", Integer, primary_key=True, autoincrement=True)
    user = Column("user", String)
    tip = Column("type", String)
    price = Column("price", Integer)
    address = Column("address", String)
    area = Column("area", Float)
    rooms_count = Column("rooms_count", Integer)
    description = Column("description", String)

    def __init__(self, user, tip, price, address, area, rooms_count, description):
        self.user = user
        self.tip = tip
        self.price = price
        self.address = address
        self.area = area
        self.rooms_count = rooms_count
        self.description = description

    def __repr__(self):
        return f"{self.id} {self.user} {self.tip} {self.address} {self.area} {self.rooms_count} {self.description}"


engine = create_engine("sqlite:///Advertisements.db", echo=True)
Base.metadata.create_all(bind=engine)
Session = sessionmaker(bind=engine)
session = Session()


def add_advertisement(user, data: Addd):
    ad = Advertisement(user, data.tip, data.price, data.address, data.area, data.rooms_count, data.description)
    session.add(ad)
    session.commit()
    return ad.id


def print_all_ad():
    print("PRINTING ALL:\n\n")
    ads = session.query(Advertisement).all()
    for ad in ads:
        print(ad)
