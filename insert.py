from models import *
from faker import Faker
from sqlalchemy.orm import sessionmaker 
import pandas as pd
from sqlalchemy import case
from datetime import datetime
import random
import tabulate

#creating engine and sessions
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

# function to inserting fake office data
def insert_office(num_office=6):
    for i in range(num_office):
        office = Office(id=i+1,name=f"office{i+1}",address=f.address())
        session.add(office)
    session.commit()

#function to inserting fake agents data
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

#function to inserting fake house data
def insert_house(num_house =30,datetime_start=datetime(2023, 1, 1),datetime_end=datetime(2023,3,1)):
    date_time_list =[]
    for i in range(num_house):
        #get random dates: defaults between 1/1/2023 and 1/3/2023
        date_time_list.append(f.date_time_between_dates(datetime_start=datetime_start,datetime_end=datetime_end))
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
    print(f.date)

#function to inserting fake buyers data
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


def add_sale_commision(houseid, buyerid, saledate, price_sold=None, session=None):
    try:
        # update house status to sold and get list price
        house = session.query(House).get(houseid)
        list_price = price_sold if price_sold is not None else house.list_price
        commission_rate = case(
            (list_price < 100000, 0.1), 
            (list_price < 200000, 0.075), 
            (list_price < 500000, 0.06), 
            (list_price < 1000000, 0.05),
            (list_price > 1000000, 0.04),
        )
        house.sold = True

        # add sale entry to the table
        agentid = house.agent_id 
        transaction = Sale(house_id=houseid, estate_agent_id=agentid, buyer_id=buyerid, sale_price=list_price, sale_date=saledate)
        session.add(transaction)
        session.flush()  # flush the transaction to generate a sale ID

        # add commission entry to table
        saleid = transaction.id 
        commission = Commission(sale_id=saleid, estate_agent_id=agentid, buyer_id=buyerid, commission=list_price * commission_rate)
        session.add(commission)

    except:
        # if an exception occurs,roll back the transaction to ensure data consistency
        session.rollback()
        raise

#insert sale data
#use transactions
def insert_sale(num_sale=25):
    #try inserting sales
    try:
        random_house_id = []
        date_time_sold = []   
        for i in range(num_sale):
            date_time_sold.append(f.date_time_between_dates(datetime_start=datetime(2023, 3, 2),datetime_end=datetime(2023,4,9)))
            
        # loop over all the sales
        for i in range(num_sale):
            # create a new session for this transaction
            session = Session()
            
            # start transaction to insert sales
            session.begin()
            
            # generate random data for the sale
            house_id_insert = random.randint(1,num_sale)

            # ensure that the same house is not sold twice in the same transaction
            if house_id_insert in random_house_id:
                session.rollback()
                session.close()
                continue

            else:
                random_house_id.append(house_id_insert)
                buyer_id_insert = random.randint(1,num_sale)
                date_time_insert = random.choice(date_time_sold)

                # call function to add sale and commission entries for each sale
                add_sale_commision(house_id_insert, buyer_id_insert, date_time_insert,session=session)

                # commit transaction to insert sale and commission entries together
                session.commit()

                # close session
                session.close()

    # catch any exception and roll back the transaction to ensure data consistency
    except:
        session.rollback()
        session.close()
        raise

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
session.close()


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
