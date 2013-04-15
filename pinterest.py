#! /usr/lib/python

from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey, MetaData
from sqlalchemy.orm import sessionmaker
import random
import datetime
#engine = create_engine('sqlite:///pinterest.db')
engine = create_engine('postgresql://postgres@localhost/pinterest')

from dataforge import *

Session = sessionmaker(bind=engine)
session = Session()


def DropAllTables(engine):
    meta = MetaData(engine)
    meta.reflect()
    meta.drop_all()

DropAllTables(engine)


class User(ForgeBase):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    fullname = Column(String)
    email = Column(String)
    created = Column(DateTime, default=datetime.datetime.utcnow)

class Board(ForgeBase):
    __tablename__ = 'board'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    created = Column(DateTime, default=datetime.datetime.utcnow)

    deps = [{'name': 'user_id', 'base': User, 'date': 'created'}, ]


class Pin(ForgeBase):
    __tablename__ = 'pin'
    id = Column(Integer, primary_key=True)
    image = Column(String)
    board_id = Column(Integer, ForeignKey("board.id"), nullable=False)
    repin_id = Column(Integer, ForeignKey("pin.id"), nullable=True)
    created = Column(DateTime, default=datetime.datetime.utcnow)

class Like(ForgeBase):
    __tablename__ = 'like'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    pin_id = Column(Integer, ForeignKey("pin.id"), nullable=True)
    created = Column(DateTime, default=datetime.datetime.utcnow)

class Follow(ForgeBase):
    __tablename__ = 'follow'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    board_id = Column(Integer, ForeignKey("board.id"), nullable=False)
    created = Column(DateTime, default=datetime.datetime.utcnow)

class Comment(ForgeBase):
    __tablename__ = 'comment'
    id = Column(Integer, primary_key=True)
    text = Column(String)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    pin_id = Column(Integer, ForeignKey("pin.id"), nullable=True)
    created = Column(DateTime, default=datetime.datetime.utcnow)


ForgeBase.metadata.create_all(engine)

def create_user(date=None):
    name = gen_name()
    email = gen_email(name)
    user = User(fullname=name, email=email, created=date)
    session.add(user)

def create_board(user_id=None, name=None, date=None):
    if user_id is None:
        user_id = get_random(User, session, date)
    board = Board(user_id=user_id, name=name, created=date)
    session.add(board)

def create_pin(board_id=None, image="", repin_id=None, date=None):
    repin_id = None
    if board_id is None:
        board_id = get_random(Board, session, date)
    pin = Pin(board_id=board_id, image=image, repin_id=repin_id, created=date)
    session.add(pin)

def create_follow(user_id=None, board_id=None, date=None):
    user_id = user_id or get_random(User, session, date)
    board_id = board_id or get_random(Board, session, date)
    board = Board(user_id=user_id, board_id=board_id, created=date)
    session.add(board)

def create_like(user_id=None, pin_id=None, date=None):
    # These could be done 'better' if they chose pins that the user was following...
    user_id = user_id or get_random(User, session, date)
    pin_id = pin_id or get_random(Pin, session, date)
    like = Like(user_id=user_id, pin_id=pin_id, created=date)
    session.add(like)

def create_comment(text=None, user_id=None, pin_id=None, date=None):
    # These could be done 'better' if they chose pins that the user was following...
    user_id = user_id or get_random(User, session, date)
    pin_id = pin_id or get_random(Pin, session, date)
    comment = Comment(text="some blurb", user_id=user_id, pin_id=pin_id, created=date)
    session.add(comment)


stop = datetime.datetime.now()
#start = stop - datetime.timedelta(days=365)
start = stop - datetime.timedelta(days=5)
dataforge = DataForge(start, stop, session)

#dataforge.forge(create_user, lambda i, x: pow(i, 1.02), DAY, lambda i, x: pow(i, 1.02))
#dataforge.forge(create_board, lambda i: 20*pow(i, 1.02), DAY, lambda i: 20*pow(i, 1.02))
#dataforge.forge(create_pin, lambda i: 50*pow(i, 1.03), DAY, lambda i: 40*pow(i, 1.01))
#dataforge.forge(create_follow, lambda i: 2*pow(i, 1.03), DAY, lambda i: 2*pow(i, 1.01))
#dataforge.forge(create_like, lambda i: 80*pow(i, 1.03), DAY, lambda i: 80*pow(i, 1.01))
#dataforge.forge(create_comment, lambda i: 50*pow(i, 1.03), DAY, lambda i: 40*pow(i, 1.01))

print "users", session.query(User).count()
print "boards", session.query(Board).count()
print "pins", session.query(Pin).count()

