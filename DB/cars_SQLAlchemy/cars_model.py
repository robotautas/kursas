import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, Table, create_engine
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///carsSA.db')
Base = declarative_base()

class Car(Base):
    __tablename__ = 'car'
    id = Column(Integer, primary_key=True)
    make = Column("make", String)
    model = Column("model", String)
    color = Column("color", String)
    year = Column("year", Integer)
    price = Column("price", Integer)

    def __init__(self, make, model, color, year, price):
        self.make = make 
        self.model = model
        self.color = color
        self.year = year
        self.price = price

    def __repr__(self):
        return f'{self.id}\t{self.make}\t{self.model}\t{self.color}\t{self.year}\t{self.price}'



if __name__ == "__main__":
    Base.metadata.create_all(engine)