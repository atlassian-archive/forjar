#! /usr/lib/python

#from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey, MetaData
import datetime
engine_url = 'sqlite:///monkdesk.db'

from dataforge import *
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
        return 8*pow(i, 1.01)

    variance = ntimes


class Company(ForgeBase):
    __tablename__ = 'companies'
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    date = Column(DateTime, default=datetime.datetime.utcnow)

    deps = [{'name': 'user_id', 'base': User, 'date': 'date'}, ]
    def forge(self, session, date=None, basetime=None):
        self.user_id = get_random(User, session, basetime=basetime)
        self.name = get_noun() + 's'


    period = DAY
    @classmethod
    def ntimes(self, i, date):
        return 20*pow(i, 1.02)
    variance = ntimes


class Agent(ForgeBase):
    __tablename__ = 'agents'
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    company_id = Column(Integer, ForeignKey("company.id"), nullable=False)
    level = Column(String(10))
    date = Column(DateTime, default=datetime.datetime.utcnow)

    period = DAY
    @classmethod
    def ntimes(self, i, date):
        return 20*pow(i, 1.02)
    variance = ntimes

    def forge(self, session, basetime=None, **kwargs):
        self.level = random.choice(['agent', 'admin', 'agent', 'agent', 'owner', 'viewer', 'viewer'])
        self.user_id = get_random(User, session, basetime=basetime)
        self.company_id = get_random(Company, session, basetime=basetime)


class Ticket(ForgeBase):
    __tablename__ = 'tickets'
    id = Column(Integer, primary_key=True)
    submitter_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    assigned_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    status = Column(String(10))
    date = Column(DateTime, default=datetime.datetime.utcnow)

    def forge(self, session, date=None, basetime=None):
        self.status = "open"

    period = DAY
    @classmethod
    def ntimes(self, i, date):
        return 50*pow(i, 1.03)

    @classmethod
    def variance(self, i, date):
        return 30*pow(i, 1.03)

class TicketComment(ForgeBase):
    __tablename__ = 'ticketcomments'

    commenter_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    ticket_id = Column(Integer, ForeignKey("ticket.id"), nullable=False)
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

class Attachment(ForgeBase):
    __tablename__ = 'attachment'
    id = Column(Integer, primary_key=True)
    ticketcomment_id = Column(Integer, ForeignKey("ticketcomments.id"), nullable=False)
    image = Column(String(100))

    def forge(self, session, basetime):
        self.ticketcomment_id = get_random(TicketComment, session, basetime=basetime)
        self.image = get_noun() + '.png'


class Comment(ForgeBase):
    __tablename__ = 'comments'
    id = Column(Integer, primary_key=True)
    text = Column(String(100))
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    pin_id = Column(Integer, ForeignKey("pins.id"), nullable=True)
    date = Column(DateTime, default=datetime.datetime.utcnow)

    def forge(self, session, date=None, basetime=None):
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


dataforge.forge_base(User)
dataforge.forge_base(Board)
dataforge.forge_base(Pin)
dataforge.forge_base(Follow)
dataforge.forge_base(Like)
dataforge.forge_base(Comment)
dataforge.print_results()
