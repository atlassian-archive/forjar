#! /usr/lib/python

import datetime
import pickle
import random
import string
import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.declarative.api import _declarative_constructor


names = pickle.load(open('loaders/names.p', 'rb'))
sites = pickle.load(open('loaders/sites.p', 'rb'))
nouns = pickle.load(open('loaders/nouns.p', 'rb'))

# Periods
MICROSECOND = 1
SECOND = 1000000*MICROSECOND
MINUTE = 60*SECOND
HOUR = 60*MINUTE
DAY = 24*HOUR
MONTH = 30*DAY
YEAR = 365*DAY


class NoMatches(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)


class ForgeBase(object):
    deps = []
    def __init__(self, **kwargs):
        forgesession = kwargs.pop('forgesession')
        try:
            self.forge(session=forgesession, **kwargs)
        except NoMatches, e:
            print "no matches", e
            return
        _declarative_constructor(self, **kwargs)
        forgesession.add(self)

ForgeBase = declarative_base( cls = ForgeBase,
                           constructor = None )

def gen_user_fullname():
    return "%s %s. %s" % (random.choice(names['first']), random.choice(string.uppercase), random.choice(names['last']))

def gen_email(name):
    return "%s@%s" % (name.split(' ')[0], random.choice(sites))

def get_noun():
    return random.choice(nouns)

def get_random(Table, session, date=None):
    query = session.query(Table)
    cnt = query.count()
    if cnt == 0:
        print "no matches!"
        raise NoMatches(Table)
    if date is not None:
        query = query.filter(Table.date < date)
    rand_id = random.randrange(0, cnt) + 1
    return rand_id

class DataForge:

    def __init__(self, start, stop, session):
        self.start = start
        self.stop = stop
        self.session = session

    def forgeBase(self, Base, ntimes=None, period=None, variance=None):
        def f(**kwargs):
            return Base(**kwargs)

        ntimes = ntimes or Base.ntimes
        period = period or Base.period
        variance = variance or Base.variance
        return self.forge(f, ntimes, period, variance)

    def forge(self, func, ntimes, period, variance):

        # the variance can be a function
        var = variance
        if type(variance) == int:
            variance = lambda time, iter: var

        nt = ntimes
        if type(ntimes) == int:
            ntimes = lambda time, iter: nt

        iterations = int((self.stop-self.start).total_seconds()/(period/SECOND))
        start = self.start
        for i, time in [(i, start + datetime.timedelta(microseconds=i*period)) for i in range(0, iterations)]:
            v = int(variance(i, time))
            t = int(ntimes(i, time)) + random.randint(-v, v)
            print func.__name__, t, i, v
            dts = sorted([random.randint(0, period) for junk in range(0, t)])
            for dt in dts:
                date = time + datetime.timedelta(microseconds=dt)
                func(date=date, forgesession=self.session)

        self.session.commit()
