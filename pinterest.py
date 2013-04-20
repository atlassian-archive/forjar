#! /usr/lib/python

#from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey, MetaData
import datetime
engine_url = 'sqlite:///pinterest.db'

from dataforge import *

engine_url = 'postgresql://postgres@localhost/pinterest'

stop = datetime.datetime.now()
#start = stop - datetime.timedelta(days=365)
start = stop - datetime.timedelta(days=5)


dataforge = DataForge(start, stop, engine_url )
session = dataforge.session



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


dataforge.drop_tables()
dataforge.create_tables()

clockstart = datetime.datetime.now()

dataforge.forge_base(User)
dataforge.forge_base(Board)
dataforge.forge_base(Pin)
dataforge.forge_base(Follow)
dataforge.forge_base(Like)
dataforge.forge_base(Comment)

print 'finished  in', (datetime.datetime.now() - clockstart)

print "users", dataforge.count_base(User), User.count
print "boards", dataforge.count_base(Board), Board.count
print "pins", dataforge.count_base(Pin), Pin.count
print "follows", dataforge.count_base(Follow), Follow.count
print "likes", dataforge.count_base(Like), Like.count
print "comments", dataforge.count_base(Comment), Comment.count

