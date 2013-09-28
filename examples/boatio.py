#! /usr/lib/python

import datetime

from forjar import *
from forjar.generators.users import gen_firstname, gen_user_fullname
from forjar.generators.sites import gen_email

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(40))
    email = Column(String(100))
    date = Column(DateTime, default=datetime.datetime.utcnow)

    def forge(self, **kwargs):
        self.name = gen_user_fullname()
        self.email = gen_email(self.name)

    period = DAY
    @classmethod
    def ntimes(self, i, time):
        return 5*pow(1.005, i)

    variance = ntimes

class Boat(Base):
    __tablename__ = 'boats'
    id = Column(Integer, primary_key=True)
    name = Column(String(40))
    type = Column(String(40))
    model = Column(String(40))
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    date = Column(DateTime, default=datetime.datetime.utcnow)
    price_per_hour = Column(Float, default=200)

    def forge(self, session, basetime, date, **kwargs):
        self.name = gen_firstname()
        self.type = random.choice(['sail', 'speed', 'sail', 'banana', 'house', 'sail', 'speed', 'speed', 'sail', 'yacht'])
        self.model = 'unknown'
        self.price_per_hour = max(random.gauss(200, 60), 20)
        self.owner_id = get_random(User, session, basetime=basetime)

    period = DAY
    @classmethod
    def ntimes(self, i, time):
        return 1*pow(1.005, i)

    variance = ntimes

class Trip(Base):
    __tablename__ = 'trips'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    boat_id = Column(Integer, ForeignKey("boats.id"), nullable=False)
    date = Column(DateTime, default=datetime.datetime.utcnow)
    start = Column(DateTime, default=datetime.datetime.utcnow)
    hours = Column(Integer, default=2)

    def forge(self, session, date=None, basetime=None):
        self.start = date + datetime.timedelta(days=random.randint(2, 20))
        self.hours = random.randint(2, 12)
        self.user_id = get_random(User, session, basetime=basetime)
        self.boat_id = get_random(Boat, session, basetime=basetime)

    period = DAY
    @classmethod
    def ntimes(self, i, time):
        return 1*pow(1.006, i)

    variance = ntimes

if __name__ == "__main__":
    forjar_main(main=gen_default_main(locals()),)
