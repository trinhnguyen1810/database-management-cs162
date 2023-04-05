from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, Index,DateTime,Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

engine = create_engine('sqlite:///real_estate.db', echo=True)
Base = declarative_base()

class Office(Base):
    __tablename__ = 'offices'
    id = Column(Integer, primary_key=True)
    name = Column(String, index = True)
    address=Column(String)
    #__table_args__ = (
    #    Index('idx_name_office', name),
    #)

class EstateAgent(Base):
    __tablename__ = 'estate_agents'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)
    phone = Column(String)
    office_id = Column(Integer, ForeignKey(Office.id))
    #__table_args__ = (
     #   Index('idx_name_agent',name),
    #)

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
    #__table_args__ = (
    #    Index('idx_date',date_listed),
    #)

class Buyer(Base):
    __tablename__ = 'buyers'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)
    phone = Column(String)

class Sale(Base):
    __tablename__ = 'sales'
    id = Column(Integer, primary_key=True)
    sale_price = Column(Float)
    sale_date = Column(DateTime,index=True)
    buyer_id = Column(Integer, ForeignKey(Buyer.id))
    estate_agent_id = Column(Integer, ForeignKey(EstateAgent.id),index = True)
    house_id = Column(Integer, ForeignKey(House.id),index = True)
    #__table_args__ = (
    #Index('idx_agent_id_date', estate_agent_id, sale_date),
    #Index('idx_house_id_date', house_id, sale_date),
    #)
    
class Commission(Base):
    __tablename__ = 'commissions'
    id = Column(Integer, primary_key=True)
    estate_agent_id = Column(Integer, ForeignKey(EstateAgent.id),index = True)
    buyer_id = Column(Integer, ForeignKey(Buyer.id))
    sale_id = Column(Integer, ForeignKey(Sale.id))
    commission = Column(Float)
    #__table_args__ = (
    #    Index('idx_agent',estate_agent_id),
    #)

class EstateAgentCommissions(Base):
    __tablename__ = 'estate_agent_total_commissions'
    id = Column(Integer, primary_key=True)
    estate_agent_id = Column(Integer, primary_key=True)
    total_commission = Column(Float)

Base.metadata.create_all(engine)

