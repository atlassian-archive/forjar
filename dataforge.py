#! /usr/lib/python

import datetime
import pickle
import random
import string

names = pickle.load(open('loaders/names.p', 'rb'))
sites = pickle.load(open('loaders/sites.p', 'rb'))

# Periods
MICROSECOND = 1
SECOND = 1000000*MICROSECOND
MINUTE = 60*SECOND
HOUR = 60*MINUTE
DAY = 24*HOUR
MONTH = 30*DAY
YEAR = 365*DAY

def gen_name():
    return "%s %s. %s" % (random.choice(names['first']), random.choice(string.uppercase), random.choice(names['last']))

def gen_email(name):
    return "%s@%s" % (name.split(' ')[0], random.choice(sites))

def get_random(Table, session, date=None):
    query = session.query(Table)
    if date is not None:
        query = query.filter(Table.created < date)
    rand_id = random.randrange(0, query.count()) + 1
    return rand_id

class Alternator:
    def __init__(self, start, stop, session):
        self.start = start
        self.stop = stop
        self.session = session

    def generate(self, func, ntimes, period, variance):

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
                func(date=date)

        self.session.commit()
