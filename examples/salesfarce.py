#! /usr/lib/python

import datetime

from forjar import *

class Account(Base):
    __tablename__ = 'Accounts'
    Account_ID  = Column(Integer, primary_key=True)
    Account_Name = Column(String(40))
    Account_Manager = Column(Integer, ForeignKey("User.User_ID"), nullable=False)
    Annual_Revenue = Column(Integer)
    Created_Date  = Column(DateTime, default=datetime.datetime.utcnow)
    Modified_Date  = Column(DateTime, default=datetime.datetime.utcnow)
    date = Column(DateTime, default=datetime.datetime.utcnow)
    #Billing_Street = Column(String(40))
    #Billing_City = Column(String(40))
    #Billing_Country = Column(String(40))
    #Billing_Postal_Code = = Column(String(40))
    def forge(self, session, basetime, date, **kwargs):
        self.Account_Name = gen_account()
        self.Account_Manager = get_random(User, session, basetime=basetime)
        self.Annual_Revenue = random.randint(200000, 2000000)
        self.Created_Date = date
        self.Modified_Date = date + datetime.timedelta(days=random.randint(7, 48))

    period = WEEK
    @classmethod
    def ntimes(self, i, time):
        return 1*pow(1.0005, i)
        
    variance = ntimes

class User(Base):
    __tablename__ = 'User'
    User_ID = Column(Integer, primary_key=True)
    date  = Column(DateTime, default=datetime.datetime.utcnow)
    Region = Column(String(40))
    Email  = Column(String(100))
    First_Name = Column(String(100))
    Last_Name = Column(String(100))
    Created_Date  = Column(DateTime, default=datetime.datetime.utcnow)

    def forge(self, session, basetime, date, **kwargs):
        self.First_Name = gen_firstname()
        self.Last_Name = gen_lastname()
        self.Region = random.choice(['Northeast', 'Central', 'Southwest', 'Northwest', 'East', 'West', 'North', 'South', 'Southeast', 'North', 'West', 'West','East'])
        self.Email = gen_full_email(self.First_Name, 'mysite.com')
        self.Created_Date = date
        
    period = MONTH
    @classmethod
    def ntimes(self, i, time):
        return 3*pow(0.9, i)

    variance = ntimes

class Contact(Base):
    __tablename__ = 'Contacts'
    Contact_ID = Column(Integer, primary_key=True)
    Account_ID = Column(Integer, ForeignKey("Accounts.Account_ID"), nullable=False)
    First_Name = Column(String(100))
    Last_Name = Column(String(100))
    date  = Column(DateTime, default=datetime.datetime.utcnow)
    Email  = Column(String(100))
    #Billing_Street = Column(String(40))
    #Billing_City = Column(String(40))
    #Billing_Country = Column(String(40))
    #Billing_Postal_Code = = Column(String(40))
    Created_Date  = Column(DateTime, default=datetime.datetime.utcnow)

    def forge(self, session, basetime, date, **kwargs):
        self.First_Name = gen_firstname()
        self.Last_Name = gen_lastname()
        self.Account_ID = get_random(Account, session, basetime=basetime)
        self.Created_Date = date
        self.Email = gen_email(self.First_Name)

    period = DAY
    @classmethod
    def ntimes(self, i, time):
        return 1*pow(1.0005, i)

    variance = ntimes
    
class Activity(Base):
    __tablename__ = 'Activities'
    Activity_ID  = Column(Integer, primary_key=True)
    Contact_ID = Column(Integer, ForeignKey("Contacts.Contact_ID"), nullable=False)
    date  = Column(DateTime, default=datetime.datetime.utcnow)
    Created_Date  = Column(DateTime, default=datetime.datetime.utcnow)
    Modified_Date  = Column(DateTime, default=datetime.datetime.utcnow)
    Comment = Column(String(40))
    Type = Column(String(40))
    Duration = Column(Integer)
    def forge(self, session, basetime, date, **kwargs):
        self.Contact_ID = get_random(Contact, session,basetime=basetime)
        self.Comment = 'Case Comment Omitted'
        self.Type = random.choice(['Call Inbound', 'Email Follow-Up', 'Call Initial', 'Call Follow-Up', 'Email Initial', 'Email Inbound', 'Meeting'])
        self.Duration = random.randint(5, 60)
        self.Created_Date = date
        self.Modified_Date = date + datetime.timedelta(days=random.randint(7, 48))

    period = FOURHOUR
    @classmethod
    def ntimes(self, i, time):
        return 1*pow(1.0001, i)
        
    variance = ntimes
    
class Lead(Base):
    __tablename__ = 'Leads'
    Lead_ID  = Column(Integer, primary_key=True)
    Converted_Contact_ID = Column(Integer, ForeignKey("Contacts.Contact_ID"), nullable=False)
    Created_ID = Column(Integer, ForeignKey("User.User_ID"), nullable=False)
    Annual_Revenue = Column(Integer)
    date  = Column(DateTime, default=datetime.datetime.utcnow)
    Created_Date  = Column(DateTime, default=datetime.datetime.utcnow)
    Converted_Date = Column(DateTime, default=datetime.datetime.utcnow)
    Modified_Date  = Column(DateTime, default=datetime.datetime.utcnow)
    Description = Column(String(40))
    Name = Column(String(100))
    Email = Column(String(100))
    def forge(self, session, basetime, date, **kwargs):
        self.Converted_Contact_ID = get_random(Contact, session, basetime=basetime)
        self.Created_ID = get_random(User, session)
        self.Annual_Revenue = random.randint(5000, 500000)
        self.Description = 'Case Description Omitted'
        self.Created_Date = date
        self.Converted_Date = date + datetime.timedelta(days=random.randint(5, 35))
        self.Modified_Date = date + datetime.timedelta(days=random.randint(7, 48))

    period = WEEK
    @classmethod
    def ntimes(self, i, time):
        return 3*pow(1.001, i)
        
    variance = ntimes
    
class Campaign(Base):
    __tablename__ = 'Campaigns'
    Campaign_ID  = Column(Integer, primary_key=True)
    Owner_ID = Column(Integer, ForeignKey("User.User_ID"), nullable=False)
    Actual_Cost = Column(Integer)
    Budgeted_Cost = Column(Integer)
    Expected_Revenue = Column(Integer)
    date  = Column(DateTime, default=datetime.datetime.utcnow)
    Created_Date  = Column(DateTime, default=datetime.datetime.utcnow)
    Campaign_Name = Column(String(100))
    Description = Column(String(40))
    Total_Contacts = Column(Integer)
    Total_Leads= Column(Integer)
    Total_Responses = Column(Integer)
    def forge(self, session, basetime, date, **kwargs):
        self.Owner_ID = get_random(User, session)
        self.Actual_Cost = random.randint(5000, 50000)
        self.Budgeted_Cost = random.randint(5000, 50000)
        self.Expected_Revenue = random.randint(50000, 500000)
        self.Description = 'Campaign Description Omitted'
        self.Created_Date = date
        self.Campaign_Name = gen_account()
        self.Modified_Date = date + datetime.timedelta(days=random.randint(7, 48))
        self.Total_Contacts = random.randint(50, 100)
        self.Total_Leads = random.randint(50, 150)
        self.Total_Responses = random.randint(10, 50)

    period = MONTH
    @classmethod
    def ntimes(self, i, time):
        return 3*pow(0.95, i)
        
    variance = ntimes
    
class Product(Base):
    __tablename__ = 'Products'
    Product_ID = Column(Integer, primary_key=True)
    Product_Name = Column(String(40))
    Product_Family  = Column(String(100))
    Description = Column(String(100))
    date = Column(DateTime, default=datetime.datetime.utcnow)
    Created_Date  = Column(DateTime, default=datetime.datetime.utcnow)

    def forge(self, session, basetime, date, **kwargs):
        self.Product_Name = get_noun().title()
        self.Product_Family = get_noun().title()
        self.Description = 'Product Description Omitted'
        self.Created_Date = date
        
    period = DAY 
    @classmethod
    def ntimes(self, i, time):
        return 3*pow(0.8, i)

    variance = ntimes
    
class Opportunity(Base):
    __tablename__ = 'Opportunities'
    Opportunity_ID  = Column(Integer, primary_key=True)
    Contact_ID = Column(Integer, ForeignKey("Contacts.Contact_ID"), nullable=False)
    Owner_ID = Column(Integer, ForeignKey("User.User_ID"), nullable=False)
    Lead_ID = Column(Integer, ForeignKey("Leads.Lead_ID"), nullable=False)
    Campaign_ID = Column(Integer, ForeignKey("Campaigns.Campaign_ID"), nullable=False)
    Product_ID = Column(Integer, ForeignKey("Products.Product_ID"), nullable=False)
    Amount = Column(Integer)
    date = Column(DateTime, default=datetime.datetime.utcnow)
    Created_Date = Column(DateTime, default=datetime.datetime.utcnow)
    Closed_Date = Column(DateTime, default=datetime.datetime.utcnow)
    Forecast_Category = Column(String(40))
    Last_Activity = Column(DateTime, default=datetime.datetime.utcnow)
    Opportunity_Type = Column(String(40))
    Probability = Column(Integer)
    Description = Column(String(40))
    Won = Column(Boolean)
    #Fiscal_Period = 
    #Fiscal Quarter =
    #Fiscal_Year = 
    def forge(self, session, basetime, date, **kwargs):
        self.Contact_ID = get_random(Contact, session)
        self.Owner_ID = get_random(User, session)
        self.Lead_ID = get_random(Lead, session)
        self.Campaign_ID = get_random(Campaign, session)
        self.Product_ID = get_random(Product, session)
        self.Amount = random.randint(1000, 100000)
        self.Description = 'Case Description Omitted'
        self.Created_Date = date
        self.Closed_Date = date + datetime.timedelta(days=random.randint(5, 120))
        self.Last_Activity = date + datetime.timedelta(days=random.randint(7, 48))
        self.Forecast_Category = random.choice(['Best Case', 'Pipeline', 'Pipeline', 'Pipeline', 'Pipeline', 'Omitted', 'Commit'])
        self.Opportunity_Type = random.choice(['Existing Customer - Upgrade', 'Existing Customer - Replacement', 'Existing Customer - Downgrade', 'New Customer'])
        self.Probability = random.choice(['10', '20', '30', '40', '50', '60', '70', '80' ,'90'])
        self.Won = random.choice(['0','1'])
    period = WEEK
    @classmethod
    def ntimes(self, i, time):
        return 2*pow(1.001, i)
        
    variance = ntimes



def main(forjar):
    forjar.forge_base(User)
    forjar.forge_base(Account)
    forjar.forge_base(Contact)
    forjar.forge_base(Activity)
    forjar.forge_base(Lead)
    forjar.forge_base(Campaign)
    forjar.forge_base(Product)
    forjar.forge_base(Opportunity)
    forjar.session.commit()
    forjar.print_results()

if __name__ == "__main__":
    forjar_main(main=main)
