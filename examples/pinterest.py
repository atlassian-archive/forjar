#! /usr/lib/python

#from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey, MetaData
import datetime

from forjar import *
stop = datetime.datetime.now()
start = stop - datetime.timedelta(days=30*8)
start = stop - datetime.timedelta(days=5)

from forjar.generators.users import gen_firstname, gen_user_fullname
from forjar.generators.sites import gen_email
from forjar.generators.text import gen_noun

class User(Base):
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


class Board(Base):
    __tablename__ = 'boards'
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    date = Column(DateTime, default=datetime.datetime.utcnow)

    deps = [{'name': 'user_id', 'base': User, 'date': 'date'}, ]
    def forge(self, session, date=None, basetime=None):
        self.user_id = get_random(User, session, basetime=basetime)
        self.name = gen_noun() + 's'


    period = DAY
    @classmethod
    def ntimes(self, i, date):
        return 20*pow(i, 1.02)
    variance = ntimes


class Pin(Base):
    __tablename__ = 'pins'
    id = Column(Integer, primary_key=True)
    image = Column(String(100))
    board_id = Column(Integer, ForeignKey("boards.id"), nullable=False)
    repin_id = Column(Integer, ForeignKey("pins.id"), nullable=True)
    date = Column(DateTime, default=datetime.datetime.utcnow)

    def forge(self, session, date=None, basetime=None):
        self.board_id = get_random(Board, session, basetime=basetime)
        self.image = gen_noun() + '.png'

    period = DAY
    @classmethod
    def ntimes(self, i, date):
        return 50*pow(i, 1.03)

    @classmethod
    def variance(self, i, date):
        return 30*pow(i, 1.03)



class Like(Base):
    __tablename__ = 'likes'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    pin_id = Column(Integer, ForeignKey("pins.id"), nullable=True)
    date = Column(DateTime, default=datetime.datetime.utcnow)

    def forge(self, session, date=None, basetime=None):
        self.user_id = get_random(User, session, basetime=basetime)
        self.pin_id = get_random(Pin, session, basetime=basetime)

    period = DAY
    @classmethod
    def ntimes(self, i, date):
        return 80*pow(i, 1.02)
    variance = ntimes


class Follow(Base):
    __tablename__ = 'follows'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    board_id = Column(Integer, ForeignKey("boards.id"), nullable=False)
    date = Column(DateTime, default=datetime.datetime.utcnow)

    def forge(self, session, date=None, basetime=None):
        self.user_id = get_random(User, session, basetime=basetime)
        self.board_id = get_random(Board, session, basetime=basetime)

    period = DAY
    @classmethod
    def ntimes(self, i, date):
        return 2*pow(i, 1.02)
    variance = ntimes


class Comment(Base):
    __tablename__ = 'comments'
    id = Column(Integer, primary_key=True)
    text = Column(String(100))
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    pin_id = Column(Integer, ForeignKey("pins.id"), nullable=True)
    date = Column(DateTime, default=datetime.datetime.utcnow)

    def forge(self, session, date=None, basetime=None):
        self.text = "%s %s %s" % (gen_noun(), gen_noun(), gen_noun())
        self.user_id = get_random(User, session, basetime=basetime)
        self.board_id = get_random(Board, session, basetime=basetime)

    period = DAY
    @classmethod
    def ntimes(self, i, date):
        return 50*pow(i, 1.02)

    @classmethod
    def variance(self, i, date):
        return 50*pow(i, 1.02)


if __name__ == "__main__":
    forjar_main(main=gen_default_main(locals()),)
