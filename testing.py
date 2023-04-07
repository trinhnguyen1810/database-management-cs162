import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Office, EstateAgent, House, Buyer, Sale, Commission
from insert import *
from query import *

f = Faker(["en_US"])
Faker.seed(0)
random.seed(0)
engine = create_engine('sqlite:///test_real_estate.db')
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine) 

class TestRealEstate(unittest.TestCase):
    def setUp(self):
        self.engine = engine
        self.metadata = Base.metadata
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()

    def tearDown(self):
        self.session.close()
        self.metadata.drop_all(self.engine)

    def test_office_table_created(self):
        self.assertTrue('offices' in self.metadata.tables)

    def test_estate_agent_table_created(self):
        self.assertTrue('estate_agents' in self.metadata.tables)

    def test_house_table_created(self):
        self.assertTrue('houses' in self.metadata.tables)

    def test_buyer_table_created(self):
        self.assertTrue('buyers' in self.metadata.tables)

    def test_sale_table_created(self):
        self.assertTrue('sales' in self.metadata.tables)

    def test_commission_table_created(self):
        self.assertTrue('commissions' in self.metadata.tables)

    def test_estate_agent_commissions_table_created(self):
        self.assertTrue('estate_agent_total_commissions' in self.metadata.tables)

    def insert_fake_data(self):
        insert_office()
        insert_agents()
        insert_house()
        insert_buyers()
        insert_sale()

    def test_insert_office(self):
        result = session.query(Office).filter_by(name="office1").first()
        self.assertIsNotNone(result)

    def test_insert_agent(self):
        result = session.query(EstateAgent).filter_by(name="Sara Warren").first()
        self.assertIsNotNone(result)
    
    def test_insert_buyer(self):
        result = session.query(Buyer).filter_by(name="Jacob Rush").first()
        self.assertIsNotNone(result)
    
    def test_insert_house(self):
        result = session.query(House).filter_by(list_price="2148992").first()
        self.assertIsNotNone(result)
    
    def test_insert_sale(self):
        result = session.query(Sale).filter_by(sale_price="2383733").first()
        self.assertIsNotNone(result)
    
    def test_query_one(self):
        result1 = query_top_offices_sales("03","2023")
        office_order =[4,2,5,3,1]
        office_name =["office4","office2","office5","office3","office1"]
        sales_order = [11209606,5847559,4928758,4114637,410854]
        for i in range(0,5):
            self.assertEqual(result1[i][0], office_order[i])
            self.assertEqual(result1[i][1], office_name[i])
            self.assertEqual(int(result1[i][2]), sales_order[i])
    
    def test_query_second(self):
        result2 = query_top_agents_sales("03","2023")
        agent_order =[8,6,5,3,2]
        agent_name =["Shannon Burke","Christopher Greer","Christopher Hernandez","Theresa Mays","Susan Munoz"]
        sales_order = [8150644,6324714,4833553,3869265,1332113]
        for i in range(0,5):
            self.assertEqual(result2[i][0], agent_order[i])
            self.assertEqual(result2[i][1], agent_name[i])
            self.assertEqual(int(result2[i][4]), sales_order[i])

    def test_query_fourth(self):
        result4 = avg_house_days("03","2023")
        self.assertEqual(result4,125.375)
    
    def test_query_fifth(self):
        result5= avg_selling_price("03","2023")
        self.assertEqual(result5,1656963.375)

        





if __name__ == '__main__':
    unittest.main()

#Question 1: Manual test
 #office 1 4091120 -> fourth
 #office 2 4913117 ->third
 #office 3 1841078 -> fifth
 #office 4 9165159 -> first
 #office 5 7640351 ->second

#Question 2: Manual testing
 #agent 1 948506 -> seventh
 #agent 2 1332113 -> fifth
 #agent 3 3869265 -> fourth
 #agent 4 0       -> eighth
 #agent 5 4833553 ->third
 #agent 6 6324714 ->second
 #agent 7 1052619 ->sixth
 #agent 8 8150644 ->first

 #question 4
 #all houses that are on market on march/2023
#print([132, 135, 150, 110, 119, 138, 109, 110, 164, 104, 119, 159, 109, 89, 128, 131]/16)
#result: 125.375


#question 5
#print([1052619.0, 1332113.0, 2039798.0, 2416113.0, 2720156.0, 2383733.0, 2467452.0, 1074678.0, 1633908.0, 410854.0, 1150827.0, 2651008.0, 319803.0, 2417440.0, 1492406.0, 948506.0]/16)
#result: 1656963.375