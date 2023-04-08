from models import *
from insert import  *
from sqlalchemy.orm import sessionmaker
from sqlalchemy import func,text
import numpy as np

#Find the top 5 offices with the most sales for that month.
#Find the top 5 estate agents who have sold the most for the month (include their contact details and their sales details so that it is easy contact them and congratulate them).
#Calculate the commission that each estate agent must receive and store the results in a separate table.
#For all houses that were sold that month, calculate the average number of days on the market.


# Create engine and session
engine = create_engine('sqlite:///real_estate.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

#Question 1
#Find the top 5 offices with the most sales for that month.
def query_top_offices_sales(month,year):
    #create sql statement to select the top 5 offices with the most sales for a given month and year
    statement = text(f"""
        SELECT
            houses.office_id,
            offices.name,
            SUM(sales.sale_price)
        FROM
            sales
            INNER JOIN houses ON sales.house_id = houses.id
            INNER JOIN offices ON houses.office_id = offices.id
        WHERE
            strftime('%m', sales.sale_date) = :month
            AND strftime('%Y', sales.sale_date) = :year
        GROUP BY
            houses.office_id,
            offices.name
        ORDER BY
            SUM(sales.sale_price) DESC
        LIMIT 5
    """)
    print(f" 🏢 5 Offices with the most sale on {month}/{year} 🏆")
    rank = 1
    queries = []

    #execute results and print statement
    with engine.connect() as conn:
        results = conn.execute(statement, {"month": month, "year": year})
    for result in results:
        print(f"Rank {rank}: Office id: {result[0]} | Office name: {result[1]} | Total month sale: {result[2]}")
        queries.append(result)
        rank +=1
    return queries

#Question 2
#Find the top 5 estate agents who have sold the most for the month 
#(include their contact details and their sales details so that it is easy contact them and congratulate them).
def query_top_agents_sales(month,year):
    #create statement to query top 5 estate agents who sell the most that month
    statement = text(f"""
        SELECT
            houses.agent_id,
            estate_agents.name,
            estate_agents.phone,
            estate_agents.email,
            SUM(sales.sale_price)
        FROM
            sales
            INNER JOIN houses ON sales.house_id = houses.id
            INNER JOIN estate_agents ON houses.agent_id = estate_agents.id
        WHERE
            strftime('%m', sales.sale_date) = :month
            AND strftime('%Y', sales.sale_date) = :year
        GROUP BY
            estate_agents.id, 
            estate_agents.name, 
            estate_agents.phone, 
            estate_agents.email
        ORDER BY
            SUM(sales.sale_price) DESC
        LIMIT 5
    """)
    print(f"🧑 5 Agents with the most sale on {month}/{year} 💼")
    queries = []
    rank = 1

    #execute results and print statement
    with engine.connect() as conn:
        results = conn.execute(statement, {"month": month, "year": year})
    for result in results:
        print(f"- Rank {rank}: Agent id: {result[0]} | Agent name: {result[1]} | Agent phone: {result[2]}  |  Agent email: {result[3]} | Total month sale: {result[4]}")
        rank +=1
        queries.append(result)
    return queries

#Question 3
#Calculate the commission that each estate agent must receive and store the results in a separate table.
def calculate_and_store_commissions():
    # create estate_agent_total_commissions table if not exists
    Base.metadata.create_all(engine)
    with engine.connect() as conn:
        # insert or replace commission values for estate agents
        statement = text("""
            INSERT OR REPLACE INTO estate_agent_total_commissions(estate_agent_id, total_commission)
            SELECT
                commissions.estate_agent_id,
                SUM(commissions.commission)
            FROM
                commissions
                INNER JOIN estate_agents ON commissions.estate_agent_id = estate_agents.id
            GROUP BY
                commissions.estate_agent_id
        """)
        conn.execute(statement)
        statement = 'SELECT * FROM estate_agent_total_commissions'
        #read the commision table to ensure if it has been inserted
        total_commission_table = pd.read_sql(statement, conn)
        total_commission_table.set_index('id', inplace=True)
        print(total_commission_table)
        #execute results and print statement
        results = conn.execute(text(statement))
        query =[]
        for row in results:
            query.append(row)
        return query

#Question 4
#For all houses that were sold that month, calculate the average number of days on the market.
def avg_house_days(month,year):
    #create statement to query how many days each house spend on the market in specific month
    statement = text(f"""
        SELECT
            sales.house_id,
            cast(julianday(sales.sale_date) - julianday(houses.date_listed) as INTEGER) AS days_on_market
        FROM
            sales
            INNER JOIN houses ON sales.house_id = houses.id
        WHERE
            strftime('%m', sales.sale_date) = :month
            AND strftime('%Y', sales.sale_date) = :year
        GROUP BY
            sales.house_id
    """)
    days = []
    #execute statement
    with engine.connect() as conn:
        results = conn.execute(statement, {"month": month, "year": year})
    for result in results:
        #print out the house id and the days they spend on the market based on the query
        print(f"- House id {result[0]} | Days on market: {int(result[1])}")
        days.append(result[1])

    #calculate average
    avg_days = sum(days)/len(days)
    print(f"🏠 The average number of days on the market houses sold on month {month} year {year} is {avg_days} 🏠 ")
    return avg_days

#Question 5
#For all houses that were sold that month, calculate the average selling price
def avg_selling_price(month,year):
    #create statement to query the house price in specific month
    statement = text(f"""
        SELECT
            sales.house_id,
            sales.sale_price
        FROM
            sales
        WHERE
            strftime('%m', sales.sale_date) = :month
            AND strftime('%Y', sales.sale_date) = :year
    """)
    prices = []
    #execute statement
    with engine.connect() as conn:
        results = conn.execute(statement, {"month": month, "year": year})
    for result in results:
        #print out the house id and their sold price
        prices.append(result[1])
        print(f"House id {result[0]} | Sold Price: {int(result[1])}")

    #calculate average
    avg_price = sum(prices)/len(prices)
    print(f"💰 The average selling prices of houses sold on month {month} year {year} is {avg_price} 💰")
    return avg_price






#printing querying for first question
print("_____________________________________________________________________________")
print("Question 1: \n")
query_top_offices_sales("03","2023")
print("_____________________________________________________________________________")
print("\n")

#printing querying for second question
print("Question 2: \n")
query_top_agents_sales("03","2023")
print("_____________________________________________________________________________")
print("\n")

#printing table for third question
print("Question 3: \n")
print("Total Agent - Commissions Table\n")
calculate_and_store_commissions()
print("_____________________________________________________________________________")
print("\n")

#printing average days on market for fourth question
print("Question 4: \n")
avg_house_days("03","2023")
print("_____________________________________________________________________________")
print("\n")

#printing average price for fifth question
print("Question 5: \n")
avg_selling_price("03","2023")
print("_____________________________________________________________________________")
print("\n")
session.close()
