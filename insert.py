from models import *
from faker import Faker
from sqlalchemy.orm import sessionmaker 
import pandas as pd
from sqlalchemy import case
from datetime import datetime
import random
import tabulate
#from IPython.display import display



Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine) 

Session = sessionmaker(bind=engine)
session = Session()


f = Faker(["en_US"])
Faker.seed(0)
#create date time that range 4 months that get sold
date_time_sold =[]
for i in range(20):
    date_time_sold.append(f.date_time_between(start_date="-30d"))

date_time_list =[]
for i in range(20):
    date_time_list.append(f.date_time_between(start_date="-180d",end_date="-91d"))

#create fake emails base on the name
def create_email(name):
    words = name.lower().split()
    email = "".join(words) + "@gmail.com"
    return email


#office
for i in range(6):
    office = Office(id=i,name=f"office{i}",address=f.address())
    session.add(office)

session.commit()

#agent
for i in range(6):
    f_name = f.name()
    f_email = create_email(f_name)
    #making sure phone number in consistent format
    f_phone = ""
    while not f_phone.startswith("("):
        f_phone = f.phone_number()
    f_officeid = random.randint(0,4)
    estate_agent = EstateAgent(id=i,name=f_name,email=f_email,phone=f_phone,office_id=f_officeid)
    session.add(estate_agent)
session.commit()

#house
for i in range(15):
    num_beds = random.randint(0,5)
    num_baths = random.randint(0,5)
    f_sold = False
    f_price = int(random.randrange(150000, 3000000))
    f_datelist = date_time_list[i]
    f_officeid = random.randint(0,4)
    f_zipcode = f'{f_officeid+1}000'
    f_agentid = random.randint(0,7)
    house = House(id=i,num_bedrooms=num_beds,
                  num_bathrooms=num_baths,
                  zipcode=f_zipcode,sold=f_sold,
                  list_price=f_price,date_listed =f_datelist,
                  office_id=f_officeid,agent_id=f_agentid)
    session.add(house)
session.commit()

#buyer
for i in range(15):
    f_name = f.name()
    f_email = create_email(f_name)
    #making sure phone number in consistent format
    f_phone = ""
    while not f_phone.startswith("("):
        f_phone = f.phone_number()
    buyer = Buyer(id=i,name=f_name,email=f_email,phone=f_phone)
    session.add(buyer)
session.commit()


def add_sale_commision(houseid,buyerid,saledate):
    try:
        #updating house status
        house = session.query(House).get(houseid)
        list_price = house.list_price
        commission_rate = case(
        (list_price < 100000, 0.1), 
        (list_price < 200000, 0.075), 
        (list_price < 500000, 0.06), 
        (list_price < 1000000, 0.05),
        (list_price > 1000000, 0.04),
        )
        house_listing = session.query(House).get(houseid)
        house_listing.sold = True
        session.commit()

        #add sales entry to table
        house = session.query(House).get(houseid)
        agentid = house.agent_id 
        transaction = Sale(house_id = houseid, buyer_id = buyerid, estate_agent_id =agentid,sale_price=list_price, sale_date =saledate)
        session.add(transaction)
        session.commit()

        #add commision entry to the table
        sale = session.query(Sale).filter(Sale.house_id == houseid).first()
        saleid = sale.id 
        house = session.query(House).get(houseid)
        agentid = house.agent_id 
        commission= Commission(estate_agent_id = agentid, buyer_id = buyerid, sale_id = saleid, commission = list_price * commission_rate)
        session.add(commission)
        session.commit()
        session.close()

    except:
        session.rollback()
        raise


#insert sale data
random_house_id =[]
for i in range(12):
    house_id_insert = random.randint(0,12)
    if house_id_insert in random_house_id:
        pass
    else:
        random_house_id.append(house_id_insert)
        buyer_id_insert= random.randint(0,17)
        date_time_insert = random.choice(date_time_sold)
        print(date_time_insert)
        add_sale_commision(house_id_insert,buyer_id_insert,date_time_insert)


Session = sessionmaker(bind=engine)
session = Session()

office_table = pd.read_sql_table(table_name="offices", con=engine)
office_table.set_index('id', inplace=True)

agents_table = pd.read_sql_table(table_name="estate_agents", con=engine)
agents_table.set_index('id', inplace=True)

houses_table = pd.read_sql_table(table_name="houses", con=engine)
houses_table.set_index('id', inplace=True)



buyers_table = pd.read_sql_table(table_name="buyers", con=engine)
buyers_table.set_index('id', inplace=True)

sales_table = pd.read_sql_table(table_name="sales", con=engine)
sales_table.set_index('id', inplace=True)

commisions_table = pd.read_sql_table(table_name="commissions", con=engine)
commisions_table.set_index('id', inplace=True)

print("Offices Table\n")
print(office_table.to_markdown())
print("\n" * 2 )
print("Agents Table\n")
print(agents_table.to_markdown())
print("\n" * 2 )
print("Houses Table\n")
print(houses_table.to_markdown(floatfmt='.0f'))
print("\n" * 2 )
print("Buyers Table\n")
print(buyers_table.to_markdown())
print("\n" * 2 )
print("Sales Table\n")
print(sales_table.to_markdown(floatfmt='.0f'))
print("\n" * 2 )
print("Commissions Table\n")
print(commisions_table.to_markdown(floatfmt='.0f'))
print("\n" * 2 )