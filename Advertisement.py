from sqlalchemy import create_engine, Column, String, Integer, Float, ForeignKeyConstraint, MetaData, Table
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine import reflection
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel

from User import get_user


class Addd(BaseModel):
    type: str
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
    type = Column("type", String)
    price = Column("price", Integer)
    address = Column("address", String)
    area = Column("area", Float)
    rooms_count = Column("rooms_count", Integer)
    description = Column("description", String)

    def __init__(self, user, tip, price, address, area, rooms_count, description):
        self.user = user
        self.type = tip
        self.price = price
        self.address = address
        self.area = area
        self.rooms_count = rooms_count
        self.description = description

    def __repr__(self):
        return f"{self.id} {self.user} {self.type} {self.address} {self.area} {self.rooms_count} {self.description}"


class Favorite(Base):
    __tablename__ = "Favorites"
    id = Column("id", Integer, primary_key=True, autoincrement=True)
    user_id = Column("user_id", Integer)
    ad_id = Column("ad_id", Integer)

    __table_args__ = (
        ForeignKeyConstraint(['user_id'], ['ads.id']),
        ForeignKeyConstraint(['ad_id'], ['ads.id']),
    )
    def __init__(self, user_id, ad_id):
        self.user_id = user_id
        self.ad_id = ad_id

engine = create_engine("sqlite:///Advertisements.db", echo=True)
Base.metadata.create_all(bind=engine)
Session = sessionmaker(bind=engine)
session = Session()


def add_advertisement(user, data: Addd):
    ad = Advertisement(user, data.type, data.price, data.address, data.area, data.rooms_count, data.description)
    session.add(ad)
    session.commit()
    return ad.id


def get_ad(ad_id: int, count=0):
    ad = session.query(Advertisement).get(ad_id)
    if ad:
        user = get_user(ad.user)
        return {
            "id": ad.id,
            "type": ad.type,
            "price": ad.price,
            "address": ad.address,
            "rooms_count": ad.rooms_count,
            "description": ad.description,
            "user_id": user["id"],
            "total_comments": count
        }


def print_all_ad():
    inspector = reflection.Inspector.from_engine(engine)

    # Get the table names
    table_names = inspector.get_table_names()

    print("Tables in the database:")
    for table_name in table_names:
        print(table_name)

    # Get the data from each table
    for table_name in table_names:
        print(f"Data in table '{table_name}':")
        metadata = MetaData()
        table = Table(table_name, metadata, autoload_with=engine)
        with engine.connect() as connection:
            result = connection.execute(table.select())
            for row in result.fetchall():
                print(row)



def update_add(ad_id: int, username, data: dict):
    ad = session.query(Advertisement).get(ad_id)
    if ad:
        if ad.user != username:
            return -1
        for key, value in data.items():
            setattr(ad, key, value)
        session.commit()
        return 1
    return 0


def delete_add(ad_id: int, username):
    ad = session.query(Advertisement).get(ad_id)
    if ad:
        if ad.user != username:
            return -1
        session.delete(ad)
        session.commit()
        return 1
    return 0


def add_to_favorite(user_id: int, ad_id: int):
    new_favorite_item = Favorite(user_id, ad_id)
    session.add(new_favorite_item)
    session.commit()
    return 1

