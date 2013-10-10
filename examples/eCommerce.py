#! /usr/lib/python

import datetime
from forjar import *
from forjar.generators.users import gen_firstname, gen_lastname, gen_user_fullname
from forjar.generators.addr import gen_address
from forjar.generators.sites import gen_email
from forjar.generators.text import gen_random_text, gen_noun
    
class Users(Base):
    __tablename__ = 'Users'
    User_ID = Column(Integer, primary_key=True)
    Campaign_ID = Column(String(40))
    First_Name = Column(String(100))
    Last_Name = Column(String(100))
    date  = Column(DateTime, default=datetime.datetime.utcnow)
    Created_Date  = Column(DateTime, default=datetime.datetime.utcnow)
    Updated_Date  = Column(DateTime, default=datetime.datetime.utcnow)
    Company = Column(String(100))
    Address = Column(String(100))
    City = Column(String(40))
    State = Column(String(40))
    Zip = Column(String(40))
    Phone = Column(String(40))
    Email = Column(String(40))
    Web = Column(String(40))
    upid = Column(String(40))    
    def forge(self, session, basetime, date, **kwargs):
        self.Campaign_ID = random.choice(['TV','TV', 'AW','AW', 'AW', 'AW','AW','FB','FB','FB','FB','TV','TV','TV','TV','WM','WM','WM']) 
        self.Created_Date = date
        self.Updated_Date = date + datetime.timedelta(days=random.randint(7, 48))
        self.First_Name, self.Last_Name, self.Company, self.Address, self.City, self.State, self.Zip, self.Phone, self.Email, self.Web = gen_address()
        self.upid = random.choice(['A', 'B', 'C', 'D','E','F','G']) 
    period = DAY*2
    @classmethod
    def ntimes(self, i, time):
        return 1*pow(1.01, i)

    variance = ntimes
    
class Shipping_Address(Base):
    __tablename__ = 'Shipping_Address'
    Shipping_Address_ID = Column(Integer, primary_key=True)
    User_ID  = Column(Integer, ForeignKey("Users.User_ID"), nullable=False)
    First_Name = Column(String(100))
    Last_Name = Column(String(100))
    Created_Date  = Column(DateTime, default=datetime.datetime.utcnow)
    Updated_Date  = Column(DateTime, default=datetime.datetime.utcnow)
    date  = Column(DateTime, default=datetime.datetime.utcnow)
    Address = Column(String(100))
    City = Column(String(40))
    State = Column(String(40))
    Zip = Column(String(40))
    
    def forge(self, session, basetime, date, **kwargs):
        self.User_ID = get_random(Users, session, basetime=basetime)
        
    period = DAY*2
    @classmethod
    def ntimes(self, i, time):
        return 1*pow(1.01, i)

    variance = ntimes
 
class Credit_Cards(Base):
    __tablename__ = 'Credit_Cards'
    Credit_Card_ID = Column(Integer, primary_key=True)
    User_ID  = Column(Integer, ForeignKey("Users.User_ID"), nullable=False)
    Number = Column(String(40))
    Month = Column(Integer)
    Year = Column(Integer)
    First_Name = Column(String(100))
    Last_Name = Column(String(100))
    Verification_Value = Column(String(40))
    Created_Date  = Column(DateTime, default=datetime.datetime.utcnow)
    Updated_Date  = Column(DateTime, default=datetime.datetime.utcnow)
    date  = Column(DateTime, default=datetime.datetime.utcnow)
    Address = Column(String(100))
    City = Column(String(40))
    State = Column(String(40))
    Zip = Column(String(40))
    
    def forge(self, session, basetime, date, **kwargs):
        self.User_ID = get_random(Users, session, basetime=basetime)
        self.Number = "**** **** **** ****"
        self.Month = random.randint(1, 12)
        self.Year = random.randint(2012, 2016)
        self.Verification_Value = "***"

    period = DAY*2
    @classmethod
    def ntimes(self, i, time):
        return 1*pow(1.01, i)

    variance = ntimes
    
class Products(Base):
    __tablename__ = 'Products'
    Product_ID = Column(Integer, primary_key=True)
    Title = Column(String(40))
    Description = Column(String(40))
    Vendor_ID = Column(Integer)
    Category  = Column(String(100))
    MSRP = Column(Integer)
    Reseller_Price = Column(Integer)
    Weight = Column(Integer)
    date = Column(DateTime, default=datetime.datetime.utcnow)
    Created_Date  = Column(DateTime, default=datetime.datetime.utcnow)
    Updated_Date  = Column(DateTime, default=datetime.datetime.utcnow)
    UPC_CODE = Column(Integer)
    Availability = Column(Boolean)
    Rating = Column(Integer)
    Reviews = Column(Integer)
    upid = Column(String(40))
    def forge(self, session, basetime, date, **kwargs):
        self.Title = gen_random_text(2,5,True)
        self.Description = 'Product Description Omitted'
        self.Vendor_ID = random.randint(1000, 100000)
        self.Category = random.choice(['Aeronautics', 'Pets', 'Farming', 'Sports', 'Literature'])
        self.MSRP = random.randint(1, 200)
        self.Reseller_Price = self.MSRP - (self.MSRP * 0.20)
        self.Weight = random.randint(1, 100)
        self.UPC_CODE = random.randint(1000000, 9999999)
        self.upid = random.choice(['A', 'B', 'C', 'D','E','F','G'])
        self.Availability = random.choice(['0','1'])
        self.Rating = random.choice(['0','1','1','2','2','2','3','3','3','3','3','3','4','4','4','4','5','5','5'])
        self.Reviews = random.randint(0, 400)
        self.Created_Date = date
        self.Updated_Date = date + datetime.timedelta(days=random.randint(7, 48))
        
    period = DAY*3
    @classmethod
    def ntimes(self, i, time):
        return 1*pow(1.001, i)

    variance = ntimes
       
class Carts(Base):
    __tablename__ = 'Carts'
    User_ID  = Column(Integer, ForeignKey("Users.User_ID"), nullable=False)
    Cart_ID = Column(Integer, primary_key=True)
    Created_Date  = Column(DateTime, default=datetime.datetime.utcnow)
    Updated_Date  = Column(DateTime, default=datetime.datetime.utcnow)
    date = Column(DateTime, default=datetime.datetime.utcnow)
    
    def forge(self, session, basetime, date, **kwargs):
        self.Created_Date = date
        self.Updated_Date = date + datetime.timedelta(days=random.randint(7, 48))
        self.User_ID = get_random(Users, session, basetime=basetime)

    period = DAY
    @classmethod
    def ntimes(self, i, time):
        return 1*pow(1.01, i)
        
    variance = ntimes
    
class Orders(Base):
    __tablename__ = 'Orders'
    Order_ID  = Column(Integer, primary_key=True)
    User_ID = Column(Integer, ForeignKey("Users.User_ID"), nullable=False) 
    Product_ID = Credit_Card_ID = Column(Integer)
    upid = Column(String(40))
    Shipping_Address_ID  = Column(Integer)
    Credit_Card_ID = Column(Integer)    
    Subtotal = Column(Integer)
    Tax_Cost = Column(Integer)
    Shipping_Cost = Column(Integer)
    Total_Cost = Column(Integer)
    date = Column(DateTime, default=datetime.datetime.utcnow)
    Created_Date  = Column(DateTime, default=datetime.datetime.utcnow)
    Updated_Date  = Column(DateTime, default=datetime.datetime.utcnow)
    Status = Column(String(100))
    Transaction_Number = Column(Integer)
    Tracking_Number = Column(Integer)
    Tracking_Type = Column(String(40))
    Notes = Column(String(40))
    def forge(self, session, basetime, date, **kwargs):
        self.User_ID = get_random(Users, session, basetime=basetime)
        self.Product_ID = random.randint(1, 50)
        self.upid = random.choice(['A', 'B', 'C', 'D','E','F','G'])
        self.Subtotal = random.randint(10, 500)
        self.Tax_Cost = self.Subtotal * .09
        self.Shipping_Cost = random.randint(10, 100)
        self.Total_Cost = self.Subtotal + self.Tax_Cost + self.Shipping_Cost
        self.Created_Date = date
        self.Updated_Date = date + datetime.timedelta(days=random.randint(7, 48))
        self.Status = random.choice(['Delivered', 'Delivered', 'Cancelled', 'Received', 'In Transit', 'In Transit', 'Delivered', 'Delivered', 'Ready for Pickup'])
        self.Transaction_Number = random.randint(111111, 9999999)
        self.Tracking_Number = random.randint(11111111, 999999999)
        self.Tracking_Type = random.randint(1, 9)
        self.Notes = "Enter Notes Here"
    period = DAY
    @classmethod
    def ntimes(self, i, time):
        return 1*pow(1.01, i)
        
    variance = ntimes
    
class Order_Products(Base):
    __tablename__ = 'Order_Products'
    Order_Product_ID  = Column(Integer, primary_key=True)
    Order_ID  = Column(Integer, ForeignKey("Orders.Order_ID"), nullable=False)
    Product_ID = Credit_Card_ID = Column(Integer)
    Created_Date  = Column(DateTime, default=datetime.datetime.utcnow)
    Updated_Date  = Column(DateTime, default=datetime.datetime.utcnow)
    date = Column(DateTime, default=datetime.datetime.utcnow)
    
    def forge(self, session, basetime, date, **kwargs):
        self.Order_ID = get_random(Orders, session, basetime=basetime)
        self.Created_Date = date
        self.Updated_Date = date + datetime.timedelta(days=random.randint(7, 48))

    period = DAY
    @classmethod
    def ntimes(self, i, time):
        return 1*pow(1.01, i)
        
    variance = ntimes
    
class Cart_Products(Base):
    __tablename__ = 'Cart_Products'
    Cart_Product_ID  = Column(Integer, primary_key=True)
    Cart_ID  = Column(Integer, ForeignKey("Carts.Cart_ID"), nullable=False)
    Product_ID = Credit_Card_ID = Column(Integer)
    Created_Date  = Column(DateTime, default=datetime.datetime.utcnow)
    Updated_Date  = Column(DateTime, default=datetime.datetime.utcnow)
    date = Column(DateTime, default=datetime.datetime.utcnow)
    
    def forge(self, session, basetime, date, **kwargs):
        self.Created_Date = date
        self.Updated_Date = date + datetime.timedelta(days=random.randint(7, 48))
        self.Cart_ID = get_random(Carts, session, basetime=basetime)
        self.Product_ID = random.randint(1, 50)

    period = DAY
    @classmethod
    def ntimes(self, i, time):
        return 1*pow(1.01, i)
        
    variance = ntimes

def main(forjar):
    forjar.forge_base(Users)
    forjar.forge_base(Shipping_Address)
    forjar.forge_base(Credit_Cards)
    forjar.forge_base(Products)
    forjar.forge_base(Carts)
    forjar.forge_base(Orders)
    forjar.forge_base(Order_Products)
    forjar.forge_base(Cart_Products)
    forjar.session.commit()
    forjar.print_results()

if __name__ == "__main__":
    forjar_main(main=main)

