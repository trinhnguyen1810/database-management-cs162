# database-management-cs162
## Overview
The database would keep track of all the data from a real estate company which have offices around the country. Additionally, each office would be responsible for specific zipcodes (areas) to sell houses. However, agents can work at multiple offices and sell different houses in different areas.
All the tables have been created, and data have been inserted based on the requirements.

### Execution (Python)
These are commands for macOS:
```bash
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
python3 models.py
python3 insert.py
python3 query.py
```

## Normalization
In general, tables ('offices','estate_agents','houses','buyers','sales') have been normalized to 3NF. This is because:

- Each table has a primary key that uniquely identifies each row in the table. Furthermore, each field only contains one value, and there are no repeating rows. (1NF)

- Meet 1NF requirement, and all non-key attributes depend on primary keys. (2NF)

- Meet 3NF requirement, and the tables have no transitive partial dependency (no non-key attributes have a relationship with other non-key attributes). This is true for the tables. Some might argue that the price_sold is dependent on house_id (an attribute in the sale table) and not only the sale id. However, the price of the listing is not always the price being sold (only true for some cases); the prices sold may be higher or lower than the listings, so they are not dependent on each other.

## Indexing

Certain indexes are being made based on the frequency we perform and the uniqueness of the values of the columns. If the columns exist in a lot of WHERE, JOIN (or sometimes GROUP BY, ORDER BY), they will be chosen as index columns. We also avoid unnecessary indexing to reduce the amount of disk space being used.


## Transactions
While we call functions to insert sales (making transactions) to the database, for each sale we insert, we create a new session. If an exception occurs during the transaction because of some errors, the session is rolled back with session.rollback() to ensure undo changes and ensure data consistency. 

## Unit testing
Unit testing to ensure insert and query work correctly with deterministic fictitious data.
```bash
python -m unittest testing
```
