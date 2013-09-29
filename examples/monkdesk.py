#! /usr/lib/python

import datetime
engine_url = 'sqlite:///monkdesk.db'

from forjar import *
from forjar.generators.text import gen_random_text, gen_noun
from forjar.generators.users import gen_user_fullname
from forjar.generators.sites import gen_email


stop = datetime.datetime.now()
#start = stop - datetime.timedelta(days=365)
start = stop - datetime.timedelta(days=5)



class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    fullname = Column(String(100))
    email = Column(String(100))
    date = Column(DateTime, default=datetime.datetime.utcnow)

    def forge(self, **kwargs):
        self.fullname = gen_user_fullname()
        self.email = gen_email(self.fullname)


class Plan(Base):
    __tablename__ = 'plan'
    id = Column(Integer, primary_key=True)
    name = Column(String(20))
    per = Column(String(20))
    price_per_user = Column(Float, default=0)


class Company(Base):
    __tablename__ = 'companies'
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    date = Column(DateTime, default=datetime.datetime.utcnow)

    deps = [{'name': 'user_id', 'base': User, 'date': 'date'}, ]
    def forge(self, session, date=None, basetime=None):
        self.name = gen_noun() + 's'

    def post_forge(self, session, date=None, basetime=None):
        user = User(forgesession=session, date=date, basetime=basetime)
        session.commit()
        Agent(user_id=user.id, company_id=self.id, forgesession=session, date=date, basetime=basetime)
        session.commit()

    period = DAY
    @classmethod
    def ntimes(self, i, date):
        return 1*pow(i, 1.02)
    variance = ntimes


class Agent(Base):
    __tablename__ = 'agents'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)
    level = Column(String(10))
    date = Column(DateTime, default=datetime.datetime.utcnow)

    period = DAY
    @classmethod
    def ntimes(self, i, date):
        return 20*pow(i, 1.02)
    variance = ntimes

    def forge(self, session, basetime=None, **kwargs):
        self.level = random.choice(['agent', 'admin', 'agent', 'agent', 'owner', 'viewer', 'viewer'])
        if not hasattr(kwargs, 'user_id'):
            self.user_id = get_random(User, session, basetime=basetime)
        if not hasattr(kwargs, 'company_id'):
            self.company_id = get_random(Company, session, basetime=basetime)


class Ticket(Base):
    __tablename__ = 'tickets'
    id = Column(Integer, primary_key=True)
    submitter_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    assigned_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    status = Column(String(10))
    date = Column(DateTime, default=datetime.datetime.utcnow)

    def forge(self, session, date=None, basetime=None):
        self.status = "open"
        self.submitter_id = get_random(User, session, basetime=basetime)

    period = DAY
    @classmethod
    def ntimes(self, i, date):
        return 50*pow(i, 1.03)

    @classmethod
    def variance(self, i, date):
        return 30*pow(i, 1.03)

class TicketComment(Base):
    __tablename__ = 'ticketcomments'
    id = Column(Integer, primary_key=True)
    commenter_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    ticket_id = Column(Integer, ForeignKey("tickets.id"), nullable=False)
    text = Column(String(1000))
    source = Column(String(10))
    public = Column(Boolean, default=False)
    date = Column(DateTime, default=datetime.datetime.utcnow)

    def forge(self, session, date=None, basetime=None):
        self.text = gen_random_text()
        self.public = (random.randint(0, 8) == 2)
        self.source = random.choice(['web', 'email', 'email', 'email', 'web', 'mobile', 'chat', 'api'])
        self.commenter_id = get_random(User, session, basetime=basetime)
        self.ticket_id = get_random(Ticket, session, basetime=basetime)

    period = DAY
    ntimes = 8

class Attachment(Base):
    __tablename__ = 'attachment'
    id = Column(Integer, primary_key=True)
    ticketcomment_id = Column(Integer, ForeignKey("ticketcomments.id"), nullable=False)
    image = Column(String(100))

    def forge(self, session, basetime):
        self.ticketcomment_id = get_random(TicketComment, session, basetime=basetime)
        self.image = gen_noun() + '.png'



def forjar_extras(forjaria):
    Plan(name='Regular', price_per_user='24.00', per='month', forgesession=forjaria.session, basetime=None)
    Plan(name='Plus', price_per_user='49.00',  per='month', forgesession=forjaria.session, basetime=None)
    Plan(name='Enterprise', price_per_user='99.00', per='month', forgesession=forjaria.session, basetime=None)


if __name__ == "__main__":
    forjar_main(main=gen_default_main(locals(), forjar_extras),)
