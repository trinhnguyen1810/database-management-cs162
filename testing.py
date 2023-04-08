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
    
    #testing creations of all tables 
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

    #inserting fake data to all datas to be ready for testings
    def insert_fake_data(self):
        insert_office()
        insert_agents()
        insert_house()
        insert_buyers()
        insert_sale()

    #test whether fake data has been inserted to office table
    def test_insert_office(self):
        result = session.query(Office).filter_by(name="office1").first()
        self.assertIsNotNone(result)

    def test_insert_agent(self):
        result = session.query(EstateAgent).filter_by(name="Shannon Burke").first()
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
    
    #testing first query
    def test_query_one(self):
        result1 = query_top_offices_sales("03","2023")
        office_order =[4,2,1,3,5]
        office_name =["office4","office2","office1","office3","office5"]
        sales_order = [6702356,5847559,3363291,3039959,2545025]
        for i in range(0,5):
            self.assertEqual(result1[i][0], office_order[i])
            self.assertEqual(result1[i][1], office_name[i])
            self.assertEqual(int(result1[i][2]), sales_order[i])
    
    def test_query_second(self):
        result2 = query_top_agents_sales("03","2023")
        agent_order =[8,5,6,2,7]
        agent_name =["Shannon Burke","Christopher Hernandez","Christopher Greer","Susan Munoz","John Carter"]
        sales_order = [8635629,4833553,4284916,1332113,1052619]
        for i in range(0,5):
            self.assertEqual(result2[i][0], agent_order[i])
            self.assertEqual(result2[i][1], agent_name[i])
            self.assertEqual(int(result2[i][4]), sales_order[i])

    def test_table_third(self):
        result3= calculate_and_store_commissions()
        #agent number for doesnt earn anything so there is no entry for agent 4
        agent_id =[1,2,3,5,6,7,8]
        agent_commission=[47425.3,53284.52,162987.68,193342.12,252988.56,42104.76,450519.3]
        for i in range(0,7):
            self.assertEqual(result3[i][1], agent_id[i])
            self.assertAlmostEqual(int(result3[i][2]), agent_commission[i],delta=1)

    def test_query_fourth(self):
        result4 = avg_house_days("03","2023")
        self.assertAlmostEqual(result4,39.076,delta=0.1)
    
    def test_query_fifth(self):
        result5= avg_selling_price("03","2023")
        self.assertAlmostEqual(result5,1653706.9230,delta=0.1)

        
if __name__ == '__main__':
    unittest.main()

#Question 1: Manual test
 #office 1: 3363291 -> fifth
 #office 2: 5847559 -> fourth
 #office 3: 3039959 -> fifth
 #office 4: 6702356 -> first
 #office 5: 2545025 -> second

#Question 2: Manual testing
#agent 1:948506 #6
#agent 2:1332113 #4
#agent 3:410854 #7
#agent 4:0 #8
#agent 5:4833553 #2
#agent 6:4284916 #3
#agent 7:1052619 #5
#agent 8:8635629 -> #1

#Question 3:
#agent 1:47425.3
#agent 2:53284.52
#agent3: 62987.68
#agent 4: 0
#agent 5: 193342.12
#agent 6: 252988.56
#agent 7: 42104.76
#agent 8: 450519.3

#question 4: Manual testing
#all houses that are on market on march/2023
#print(sum([29, 53, 21, 19, 22, 54, 64, 35, 26, 53, 64, 46, 22])/13)
#result: 39.076

#question 5: Manual testing
#print(sum([1052619, 1332113, 2416113, 2720156,1633908, 410854, 1150827, 2651008, 319803, 2417440, 1492406, 2952437, 948506])/13)
#result: 1653706.9230


