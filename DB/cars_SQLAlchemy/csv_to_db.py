from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from cars_model import Car, engine

Session = sessionmaker(bind=engine)
session = Session()

with open('auto.csv', 'r') as f:
    lines = f.readlines()

for line in lines[1:]:
    splitted_line = line[:-1].split(',')
    print(splitted_line)
    car = Car(*splitted_line)
    session.add(car)
    session.commit()
