from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, Index,DateTime,Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

engine = create_engine('sqlite:///real_estate.db', echo=True)
Base = declarative_base()

#normalized tables to 3NF form
#creating an office object to insert to the office table
class Office(Base):
    __tablename__ = 'offices'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    address=Column(String)

    def __repr__(self):
        return(f'Office {self.id}, name={self.name}, address={self.address}')

#creating an office object to insert to the office table
class EstateAgent(Base):
    __tablename__ = 'estate_agents'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)
    phone = Column(String)
    def __repr__(self):
        return(f'Office {self.id}, name={self.name}, email ={self.email}, phone={self.phone}')

#creating an office object to insert to the office table
#using foreign key to join tables and ensure consistency across data tables 
#add index on date_listed due to the frequency have to query and uniqueness
class House(Base):
    __tablename__ = 'houses'
    id = Column(Integer, primary_key=True)
    num_bedrooms = Column(Integer)
    num_bathrooms = Column(Integer)
    zipcode = Column(Integer)
    sold = Column(Boolean)
    list_price = Column(Float)
    date_listed = Column(DateTime, index = True)
    office_id = Column(Integer, ForeignKey(Office.id))
    agent_id = Column(Integer, ForeignKey(EstateAgent.id))

    def __repr__(self):
        return (f"House {self.id}, Num bedrooms: {self.num_bedrooms}, "
                f"Num bathrooms: {self.num_bathrooms}, Zipcode: {self.zipcode}, "
                f"Sold: {self.sold}, List price: {self.list_price}, "
                f"Date listed: {self.date_listed}, Office id: {self.office_id}, "
                f"Agent id: {self.agent_id}")

class Buyer(Base):
    __tablename__ = 'buyers'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)
    phone = Column(String)
    def __repr__(self):
        return(f'Office {self.id}, name={self.name}, email ={self.email}, phone={self.phone}')

#creating a sale object to insert to the sale table
#using foreign key to join tables and ensure consistency across data tables 
#add index on relevant columns based on frequency we would query and uniqueness
class Sale(Base):
    __tablename__ = 'sales'
    id = Column(Integer, primary_key=True)
    sale_price = Column(Float)
    estate_agent_id = Column(Integer, ForeignKey(EstateAgent.id),index = True)
    house_id = Column(Integer, ForeignKey(House.id),index=True)
    sale_date = Column(DateTime,index=True)
    buyer_id = Column(Integer, ForeignKey(Buyer.id))
    estate_agent_id = Column(Integer, ForeignKey(EstateAgent.id),index = True)
    house_id = Column(Integer, ForeignKey(House.id),index=True)
    def __repr__(self):
        return (f"Sale {self.id}, Sale price: {self.sale_price}, Sale date: {self.sale_date}, "
                f"Buyer id: {self.buyer_id}, Estate agent id: {self.estate_agent_id}, House id: {self.house_id}")


#creating a commission object to insert to the commission table
#using foreign key to join tables and ensure consistency across data tables 
#add index on relevant columns based on frequency we would query and uniqueness

class Commission(Base):
    __tablename__ = 'commissions'
    id = Column(Integer, primary_key=True)
    sale_id = Column(Integer, ForeignKey(Sale.id))
    estate_agent_id = Column(Integer, ForeignKey(EstateAgent.id),index = True)
    buyer_id = Column(Integer, ForeignKey(Buyer.id))
    commission = Column(Float)
    def __repr__(self):
        return (f"Commission {self.id}, Estate agent id: {self.estate_agent_id}, "
                f"Buyer id: {self.buyer_id}, Sale id: {self.sale_id}, Commission: {self.commission}")

class EstateAgentCommissions(Base):
    __tablename__ = 'estate_agent_total_commissions'
    id = Column(Integer, primary_key=True)
    estate_agent_id = Column(Integer)
    total_commission = Column(Float)
    def __repr__(self):
        return f"EstateAgentCommissions {self.id}, Estate agent id: {self.estate_agent_id}, Total commission: {self.total_commission}"

Base.metadata.create_all(engine)

