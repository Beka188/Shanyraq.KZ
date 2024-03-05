import datetime
from sqlalchemy import create_engine, Column, String, Integer, DateTime
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel

Base = declarative_base()

class com(BaseModel):
    content: str


class Comment(Base):
    __tablename__ = "Comments"
    id = Column("id", Integer, primary_key=True, autoincrement=True)
    username = Column("username", String)
    content = Column("content", String)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    advertisement_id = Column("ad_id", Integer)

    def __init__(self, content, username, ad_id):
        self.username = username
        self.content = content
        self.advertisement_id = ad_id

    def __repr__(self):
        return f"{self.id} {self.username} {self.content} {self.created_at}"


engine = create_engine("sqlite:///Advertisements.db", echo=True)
Base.metadata.create_all(bind=engine)
Session = sessionmaker(bind=engine)
session = Session()


def add_comment(content, username, ad_id):
    new_comment = Comment(content["content"], username, ad_id)
    session.add(new_comment)
    session.commit()


def print_all_comments():
    comments = session.query(Comment).all()
    for com in comments:
        print(com)
