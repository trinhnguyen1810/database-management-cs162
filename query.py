from models import *
from insert import  *
from sqlalchemy.orm import sessionmaker
from sqlalchemy import func,text
import numpy as np

#Find the top 5 offices with the most sales for that month.
#Find the top 5 estate agents who have sold the most for the month (include their contact details and their sales details so that it is easy contact them and congratulate them).
#Calculate the commission that each estate agent must receive and store the results in a separate table.
#For all houses that were sold that month, calculate the average number of days on the market.
#For all houses that were sold that month, calculate the average selling price

# Create engine and session
engine = create_engine('sqlite:///real_estate.db')
Session = sessionmaker(bind=engine)
session = Session()

#Question 1
def query_top_offices_sales(month,year):
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
    queries = []
    with engine.connect() as conn:
        results = conn.execute(statement, {"month": month, "year": year})
    for result in results:
        print(result)
        queries.append(result)
    return queries
query_top_offices_sales("03","2023")

#Question 2
def query_top_agents_sales(month,year):
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
    queries = []
    with engine.connect() as conn:
        results = conn.execute(statement, {"month": month, "year": year})
    for result in results:
        print(result)
        queries.append(result)
    return queries
query_top_agents_sales("03","2023")

def find_total_commision():
    print("Marker")
    statement = text("""
        SELECT
            commissions.estate_agent_id,
            SUM(commissions.commission)
        FROM
            commissions
            INNER JOIN estate_agents ON commissions.estate_agent_id = estate_agents.id
        GROUP BY
            commissions.estate_agent_id
        ORDER BY
            SUM(commissions.commission) DESC

    """)
    with engine.connect() as conn:
        results = conn.execute(statement)
    for row in results:
        print(row)
find_total_commision()

#Question 3 (LOTS OF BUGS)
def calculate_and_store_commissions():
    # create estate_agent_total_commissions table if not exists
    Base.metadata.create_all(engine)
    with engine.connect() as conn:
        # insert or replace commission values for estate agents
        statement = text("""
            INSERT OR REPLACE INTO estate_agent_total_commissions(estate_agent_id,total_commission)
            SELECT
                commissions.estate_agent_id,
                SUM(commissions.commission)
            FROM
                commissions
                INNER JOIN estate_agents ON commissions.estate_agent_id = estate_agents.id
            GROUP BY
                commissions.estate_agent_id
            ORDER BY
                SUM(commissions.commission) DESC

        """)
        conn.execute(statement)

        # print out estate_agent_total_commissions table
        results = conn.execute(text("SELECT * FROM estate_agent_total_commissions"))
        for row in results:
            print(row)
calculate_and_store_commissions()

#Question 4
def avg_house_days(month,year):
    statement = text(f"""
        SELECT
            sales.house_id,
            julianday(sales.sale_date) - julianday(houses.date_listed) AS days_on_market
        FROM
            sales
            INNER JOIN houses ON sales.house_id = houses.id
        WHERE
            strftime('%m', sales.sale_date) = :month
            AND strftime('%Y', sales.sale_date) = :year
        GROUP BY
            sales.house_id
    """)
    with engine.connect() as conn:
        results = conn.execute(statement, {"month": month, "year": year})
    days = []
    for row in results:
        print(row)
        days.append(row[1])
    avg_days = sum(days)/len(days)
    print(f"The average number of days on the market houses sold on month {month} year {year} is {avg_days}")
avg_house_days("03","2023")

#Question 5
def avg_selling_price(month,year):
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

    with engine.connect() as conn:
        results = conn.execute(statement, {"month": month, "year": year})
    prices = []
    for row in results:
        print(row)
        prices.append(row[1])
    avg_price = sum(prices)/len(prices)
    print(f"The average selling prices of houses sold on month {month} year {year} is {avg_price}")
avg_selling_price("03","2023")



print("Total Agent - Commissions Table\n")
agent_commision_table = pd.read_sql_table(table_name="estate_agent_total_commissions", con=engine)
agent_commision_table.set_index('id', inplace=True)
print(agent_commision_table.to_markdown(floatfmt='.0f'))