#! /usr/lib/python

import datetime

from dataforge import *
stop = datetime.datetime.now()
start = stop - datetime.timedelta(days=30*8)
start = stop - datetime.timedelta(days=5)

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(40))
    date = Column(DateTime, default=datetime.datetime.utcnow)

    def forge(self, **kwargs):
        self.name = gen_firstname()

    period = DAY
    @classmethod
    def ntimes(self, i, time):
        return 2*pow(i, 1.05)

    variance = ntimes


class Event(Base):
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
        return pow(i, 1.06)

    variance = ntimes


def main(forjar):

    forjar.forge_base(User)
    forjar.forge_base(Event)
    forjar.print_results()

if __name__ == "__main__":
    forjar_main(main=main, start=start, stop=stop)
