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
random.seed(0)



#create fake emails base on the name
def create_email(name):
    words = name.lower().split()
    email = "".join(words) + "@gmail.com"
    return email

def insert_office(num_office=6):
    for i in range(num_office):
        office = Office(id=i+1,name=f"office{i+1}",address=f.address())
        session.add(office)
    session.commit()

def insert_agents(num_agents=8):
    for i in range(num_agents):
        f_name = f.name()
        f_email = create_email(f_name)
        #making sure phone number in consistent format
        f_phone = ""
        while not f_phone.startswith("("):
            f_phone = f.phone_number()
        estate_agent = EstateAgent(id=i+1,name=f_name,email=f_email,phone=f_phone)
        session.add(estate_agent)
    session.commit()

def insert_house(num_house =30):
    date_time_list =[]
    for i in range(num_house):
        date_time_list.append(f.date_time_between(start_date="-180d",end_date="-91d"))
    for i in range(num_house):
        num_beds = random.randint(1,5)
        num_baths = random.randint(1,5)
        f_sold = False
        f_price = int(random.randrange(150000, 3000000))
        f_datelist = date_time_list[i]
        f_officeid = random.randint(1,5)
        f_zipcode = f'{f_officeid}000'
        f_agentid = random.randint(1,8)
        house = House(id=i+1,num_bedrooms=num_beds,
                    num_bathrooms=num_baths,
                    zipcode=f_zipcode,sold=f_sold,
                    list_price=f_price,date_listed =f_datelist,
                    office_id=f_officeid,agent_id=f_agentid)
        session.add(house)
    session.commit()

#buyer
def insert_buyers(num_buyer=25):
    for i in range(num_buyer):
        f_name = f.name()
        f_email = create_email(f_name)
        #making sure phone number in consistent format
        f_phone = ""
        while not f_phone.startswith("("):
            f_phone = f.phone_number()
        buyer = Buyer(id=i+1,name=f_name,email=f_email,phone=f_phone)
        session.add(buyer)
    session.commit()

def add_sale_commision(houseid,buyerid,saledate,price_sold=None):
    try:
        #updating house status
        house = session.query(House).get(houseid)
        list_price = price_sold if price_sold is not None else house.list_price
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
def insert_sale(num_sale=25):
    random_house_id =[]
    date_time_sold =[]
    for i in range(num_sale):
        date_time_sold.append(f.date_time_between(start_date="-30d"))

    for i in range(num_sale):
        house_id_insert = random.randint(1,num_sale)
        if house_id_insert in random_house_id:
            pass
        else:
            random_house_id.append(house_id_insert)
            buyer_id_insert= random.randint(1,num_sale)
            date_time_insert = random.choice(date_time_sold)
            add_sale_commision(house_id_insert,buyer_id_insert,date_time_insert)


insert_office()
office_table = pd.read_sql_table(table_name="offices", con=engine)
office_table.set_index('id', inplace=True)

insert_agents()
agents_table = pd.read_sql_table(table_name="estate_agents", con=engine)
agents_table.set_index('id', inplace=True)

insert_buyers()
buyers_table = pd.read_sql_table(table_name="buyers", con=engine)
buyers_table.set_index('id', inplace=True)

insert_house()
insert_sale()
sales_table = pd.read_sql_table(table_name="sales", con=engine)
sales_table.set_index('id', inplace=True)

houses_table = pd.read_sql_table(table_name="houses", con=engine)
houses_table.set_index('id', inplace=True)

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
