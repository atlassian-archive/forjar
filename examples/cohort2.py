#! /usr/lib/python

import datetime

from forjar import *

class Users(Base):
    __tablename__ = 'Users'
    User_ID = Column(Integer, primary_key=True)
    date  = Column(DateTime, default=datetime.datetime.utcnow)
    Campaign_ID = Column(String(40))
    Created_Date  = Column(DateTime, default=datetime.datetime.utcnow)

    def forge(self, session, basetime, date, **kwargs):
        self.Campaign_ID = random.choice(['TV','TV','TV','AW','FB','WM','TV','FB','AW','WM','AW', 'AW', 'AW','AW','FB','FB','FB','TV','TV','TV','TV','WM','WM'])
        self.Created_Date = date
        
    period = DAY
    @classmethod
    def ntimes(self, i, time):
        return 1*pow(1.005, i)

    variance = ntimes
    
class Orders(Base):
    __tablename__ = 'Orders'
    Order_ID  = Column(Integer, primary_key=True)
    User_ID = Column(Integer, ForeignKey("Users.User_ID"), nullable=False)
    name = Column(String(40))
    date  = Column(DateTime, default=datetime.datetime.utcnow)
    Created_Date  = Column(DateTime, default=datetime.datetime.utcnow)
    def forge(self, session, basetime, date, **kwargs):
        self.User_ID = get_random(Users, session, basetime=basetime)
        self.name = random.choice(['A', 'B', 'C', 'D','E','F','G'])
        self.Created_Date = date

    period = DAY
    @classmethod
    def ntimes(self, i, time):
        return 1*pow(1.01, i)
        
    variance = ntimes
    

def main(forjar):
    forjar.forge_base(Users)
    forjar.forge_base(Orders)
    forjar.session.commit()
    forjar.print_results()

if __name__ == "__main__":
    forjar_main(main=main)
