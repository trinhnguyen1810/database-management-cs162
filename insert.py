from models import *
from faker import Faker
from sqlalchemy.orm import sessionmaker 
import pandas as pd
from sqlalchemy import case
from datetime import datetime
import random


Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine) 

Session = sessionmaker(bind=engine)
session = Session()


f = Faker(["en_US"])
#create date time that range 4 months that get sold
date_time_sold =[]
for i in range(30):
    date_time_sold.append(f.date_time_between(start_date="-120d"))

date_time_list =[]
for i in range(30):
    date_time_list.append(f.date_time_between(start_date="-180d",end_date="-121"))

#create fake emails base on the name
def create_email(name):
    words = name.lower().split()
    email = "".join(words) + "@gmail.com"
    return email


#office
for i in range(5):
    office = Office(id=i,name=f"office{i}",address=f.address())
    session.add(office)

session.commit()

#agent
for i in range(8):
    f_name = f.name()
    f_email = create_email(f_name)
    f_phone= f.phone()
    f_officeid = random.randint(0,4)
    estate_agent = EstateAgent(id=i,name=f_name,email=f_email,phone=f_phone,office_id=f_officeid)
    session.add(estate_agent)
session.commit()

#house
for i in range(30):
    num_beds = random.randint(0,5)
    num_baths = random.randint(0,5)
    f_zipcode = f.zipcode()
    f_sold = random.choices([True,False],weights=[0.8,0,2])
    f_price = random.randint(150000,3000000)
    f_datelist = date_time_list[i]
    f_officeid = random.randint(0,4)
    f_agentid = random.randint(0,7)
    house = House(id=i,num_bedrooms=num_beds,
                  num_bathrooms=num_baths,
                  zipcode=f_zipcode,sold=f_sold,
                  list_price=f_price,date_listed =f_datelist,
                  office_id=f_officeid,agent_id=f_agentid)
    session.add(house)
session.commit()

#buyer
for i in range(18):
    f_name = f.name()
    f_email = create_email(f_name)
    f_phone= f.phone()
    buyer = Buyer(id=i,name=f_name,email=f_email,phone=f_phone)
session.commit()











