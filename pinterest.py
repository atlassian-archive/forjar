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
    __tablename__ = 'users'
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
        return 8*pow(i, 1.02)

    variance = ntimes


class Board(ForgeBase):
    __tablename__ = 'boards'
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    date = Column(DateTime, default=datetime.datetime.utcnow)

    deps = [{'name': 'user_id', 'base': User, 'date': 'date'}, ]
    def forge(self, session=None, date=None, basetime=None):
        self.user_id = get_random(User, session, basetime=basetime)
        self.name = get_noun() + 's'


    period = DAY
    @classmethod
    def ntimes(self, i, date):
        return 20*pow(i, 1.02)
    variance = ntimes


class Pin(ForgeBase):
    __tablename__ = 'pins'
    id = Column(Integer, primary_key=True)
    image = Column(String(100))
    board_id = Column(Integer, ForeignKey("boards.id"), nullable=False)
    repin_id = Column(Integer, ForeignKey("pins.id"), nullable=True)
    date = Column(DateTime, default=datetime.datetime.utcnow)

    def forge(self, session=None, date=None, basetime=None):
        self.board_id = get_random(Board, session, basetime=basetime)
        self.image = get_noun() + '.png'

    period = DAY
    @classmethod
    def ntimes(self, i, date):
        return 50*pow(i, 1.03)

    @classmethod
    def variance(self, i, date):
        return 30*pow(i, 1.03)



class Like(ForgeBase):
    __tablename__ = 'likes'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    pin_id = Column(Integer, ForeignKey("pins.id"), nullable=True)
    date = Column(DateTime, default=datetime.datetime.utcnow)

    def forge(self, session=None, date=None, basetime=None):
        self.user_id = get_random(User, session, basetime=basetime)
        self.pin_id = get_random(Pin, session, basetime=basetime)

    period = DAY
    @classmethod
    def ntimes(self, i, date):
        return 80*pow(i, 1.02)
    variance = ntimes


class Follow(ForgeBase):
    __tablename__ = 'follows'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    board_id = Column(Integer, ForeignKey("boards.id"), nullable=False)
    date = Column(DateTime, default=datetime.datetime.utcnow)

    def forge(self, session=None, date=None, basetime=None):
        self.user_id = get_random(User, session, basetime=basetime)
        self.board_id = get_random(Board, session, basetime=basetime)

    period = DAY
    @classmethod
    def ntimes(self, i, date):
        return 2*pow(i, 1.02)
    variance = ntimes


class Comment(ForgeBase):
    __tablename__ = 'comments'
    id = Column(Integer, primary_key=True)
    text = Column(String(100))
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    pin_id = Column(Integer, ForeignKey("pins.id"), nullable=True)
    date = Column(DateTime, default=datetime.datetime.utcnow)

    def forge(self, session=None, date=None, basetime=None):
        self.text = "%s %s %s" % (get_noun(), get_noun(), get_noun())
        self.user_id = get_random(User, session, basetime=basetime)
        self.board_id = get_random(Board, session, basetime=basetime)

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
start = stop - datetime.timedelta(days=14)
dataforge = DataForge(start, stop, session)

clockstart = datetime.datetime.now()

dataforge.forgeBase(User)
dataforge.forgeBase(Board)
dataforge.forgeBase(Pin)
dataforge.forgeBase(Follow)
dataforge.forgeBase(Like)
dataforge.forgeBase(Comment)

print 'finished  in', (datetime.datetime.now() - clockstart)

print "users", session.query(User).count(), User.count
print "boards", session.query(Board).count(), Board.count
print "pins", session.query(Pin).count(), Pin.count
print "follows", session.query(Follow).count(), Follow.count
print "likes", session.query(Like).count(), Like.count
print "comments", session.query(Comment).count(), Comment.count

