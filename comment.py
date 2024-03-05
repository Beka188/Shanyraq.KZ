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
    author_id = Column("author_id", Integer)
    content = Column("content", String)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    advertisement_id = Column("ad_id", Integer)

    def __init__(self, content, author_id, ad_id):
        self.author_id = author_id
        self.content = content
        self.advertisement_id = ad_id

    def __repr__(self):
        return f"{self.id} {self.author_id} {self.content} {self.created_at}"


engine = create_engine("sqlite:///Comments.db", echo=True)
Base.metadata.create_all(bind=engine)
Session = sessionmaker(bind=engine)
session = Session()


def add_comment(content, user_id, ad_id):
    new_comment = Comment(content["content"], user_id, ad_id)
    session.add(new_comment)
    session.commit()


def get_comments(ad_id):
    comments = session.query(Comment).filter(Comment.advertisement_id == ad_id).all()
    # print([("content": co.content) for co in comments])
    return [to_json(co) for co in comments]


def to_json(comment):
    return {
        "id": comment.id,
        "content": comment.content,
        "created_at": comment.created_at,
        "author_id": comment.author_id
    }
def print_all_comments():
    comments = session.query(Comment).all()
    for com in comments:
        print(com)
