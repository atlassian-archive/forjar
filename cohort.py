#! /usr/lib/python

import datetime
engine_url = 'sqlite:///monkdesk.db'

from dataforge import *
stop = datetime.datetime.now()
start = stop - datetime.timedelta(days=30*8)
start = stop - datetime.timedelta(days=5)

dataforge = DataForge(start, stop, engine_url )
session = dataforge.session


class User(ForgeBase):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(40))
    date = Column(DateTime, default=datetime.datetime.utcnow)

    def forge(self, **kwargs):
        self.name = gen_firstname()

    period = DAY
    @classmethod
    def ntimes(self, i, time):
        return 10*pow(i, 1.15)

    variance = ntimes


class Event(ForgeBase):
    __tablename__ = 'events'
    id = Column(Integer, primary_key=True)
    key = Column(String(10))
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    date = Column(DateTime, default=datetime.datetime.utcnow)

    def forge(self, session, date=None, basetime=None):
        self.key = random.choice(['like', 'like', 'like', 'like', 'share', 'comment', 'share'])

        def get_log_random_choice(cnt):
            return int(pow(random.randrange(0, cnt*cnt), .5))

        self.user_id = get_random(User, session, basetime=basetime, choicefunc=get_log_random_choice)

    period = DAY
    @classmethod
    def ntimes(self, i, time):
        return 8*pow(i, 1.15)

    variance = ntimes


dataforge.drop_tables()
dataforge.create_tables()

dataforge.forge_base(User)
dataforge.forge_base(Event)
dataforge.print_results()
#print 'users', dataforge.count_base(User)
