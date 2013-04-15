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
    fullname = Column(String(100))
    email = Column(String(100))
    date = Column(DateTime, default=datetime.datetime.utcnow)

    def forge(self, **kwargs):
        self.fullname = gen_user_fullname()
        self.email = gen_email(self.fullname)


    period = DAY

    @classmethod
    def ntimes(self, i, time):
        return pow(i, 1.02)

    variance = ntimes


class Board(ForgeBase):
    __tablename__ = 'board'
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    date = Column(DateTime, default=datetime.datetime.utcnow)

    deps = [{'name': 'user_id', 'base': User, 'date': 'date'}, ]
    def forge(self, session=None, date=None):
        self.user_id = get_random(User, session, date=date)
        self.name = get_noun() + 's'


    period = DAY
    @classmethod
    def ntimes(self, i, date):
        return 20*pow(i, 1.02)
    variance = ntimes


class Pin(ForgeBase):
    __tablename__ = 'pin'
    id = Column(Integer, primary_key=True)
    image = Column(String(100))
    board_id = Column(Integer, ForeignKey("board.id"), nullable=False)
    repin_id = Column(Integer, ForeignKey("pin.id"), nullable=True)
    date = Column(DateTime, default=datetime.datetime.utcnow)

    def forge(self, session=None, date=None):
        self.board_id = get_random(Board, session, date=date)
        self.image = get_noun() + '.png'

    period = DAY
    @classmethod
    def ntimes(self, i, date):
        return 50*pow(i, 1.03)

    @classmethod
    def variance(self, i, date):
        return 30*pow(i, 1.03)



class Like(ForgeBase):
    __tablename__ = 'like'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    pin_id = Column(Integer, ForeignKey("pin.id"), nullable=True)
    date = Column(DateTime, default=datetime.datetime.utcnow)

    def forge(self, session=None, date=None):
        self.user_id = get_random(User, session, date=date)
        self.pin_id = get_random(Pin, session, date=date)

    period = DAY
    @classmethod
    def ntimes(self, i, date):
        return 80*pow(i, 1.02)
    variance = ntimes


class Follow(ForgeBase):
    __tablename__ = 'follow'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    board_id = Column(Integer, ForeignKey("board.id"), nullable=False)
    date = Column(DateTime, default=datetime.datetime.utcnow)

    def forge(self, session=None, date=None):
        self.user_id = get_random(User, session, date=date)
        self.board_id = get_random(Board, session, date=date)

    period = DAY
    @classmethod
    def ntimes(self, i, date):
        return 2*pow(i, 1.02)
    variance = ntimes


class Comment(ForgeBase):
    __tablename__ = 'comment'
    id = Column(Integer, primary_key=True)
    text = Column(String(100))
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    pin_id = Column(Integer, ForeignKey("pin.id"), nullable=True)
    date = Column(DateTime, default=datetime.datetime.utcnow)

    def forge(self, session=None, date=None):
        self.text = "%s %s %s" % (get_noun(), get_noun(), get_noun())
        self.user_id = get_random(User, session, date=date)
        self.board_id = get_random(Board, session, date=date)

    period = DAY
    @classmethod
    def ntimes(self, i, date):
        return 50*pow(i, 1.02)

    @classmethod
    def variance(self, i, date):
        return 50*pow(i, 1.02)


ForgeBase.metadata.create_all(engine)




stop = datetime.datetime.now()
#start = stop - datetime.timedelta(days=365)
start = stop - datetime.timedelta(days=9)
dataforge = DataForge(start, stop, session)

dataforge.forgeBase(User)
dataforge.forgeBase(Board)
dataforge.forgeBase(Pin)
dataforge.forgeBase(Follow)
dataforge.forgeBase(Like)
dataforge.forgeBase(Comment)

print "users", session.query(User).count()
print "boards", session.query(Board).count()
print "pins", session.query(Pin).count()
print "follows", session.query(Follow).count()
print "likes", session.query(Like).count()
print "comments", session.query(Comment).count()

