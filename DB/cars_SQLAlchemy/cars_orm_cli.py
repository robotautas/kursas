from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from cars_model import Car, engine

Session = sessionmaker(bind=engine)
session = Session()

def insert():
    make = input('Make: ')
    model = input('Model: ')
    color = input('Color: ')
    year = int(input('Year: '))
    price = int(input('Price: '))
    car = Car(make, model, color, int(year), int(price))
    session.add(car)
    session.commit()

def search():
    make = input('Make: ')
    model = input('Model: ')
    color = input('Color: ')
    year_from = input('Year from: ')
    year_to = input('Year to: ')
    price_from = input('Price from: ')
    price_to = input('Price to: ')
    
    cars = session.query(Car).filter(
        Car.make.ilike(make + '%' if make else '%'),
        Car.model.ilike(model + '%' if model else '%'),
        Car.color.ilike(color + '%' if color else '%'),
        Car.year >= (int(year_from) if year_from else 1900),
        Car.year <= (int(year_to) if year_to else 2100),
        Car.price >= (int(price_from) if price_from else 0),
        Car.price <= (int(price_to) if price_to else 1000000)
    )
     
    for car in cars:
        print(car)
    
while True:
    choice = input('Search, Insert or Quit? (s/i/q): ')
    if choice == 's':
        search()
    elif choice == 'i':
        insert()
    elif choice == 'q':
        exit()
    else:
        print('Input s, i ors q!')
