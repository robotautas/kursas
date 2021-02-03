from flask import Flask, render_template, request
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from cars_model import Car, engine

def search(make, model, color, year_from, year_to, price_from, price_to):    
    Session = sessionmaker(bind=engine)
    session = Session()
    cars = session.query(Car).filter(
        Car.make.ilike(make + '%' if make else '%'),
        Car.model.ilike(model + '%' if model else '%'),
        Car.color.ilike(color + '%' if color else '%'),
        Car.year >= (int(year_from) if year_from else 1900),
        Car.year <= (int(year_to) if year_to else 2100),
        Car.price >= (int(price_from) if price_from else 0),
        Car.price <= (int(price_to) if price_to else 1000000)
    )
    res = [(i.make, i.model, i.color, i.year, i.price) for i in cars]
    session.close()
    return res

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    res = ''
    if request.method == 'POST':
        make = request.form['make']
        model = request.form['model']
        color = request.form['color']
        year_from = request.form['year_from']
        year_to = request.form['year_to']
        price_from = request.form['price_from']
        price_to = request.form['price_to']
        res = search(make, model, color, year_from, year_to, price_from, price_to)
    return render_template('index.html', res=res)

if __name__ == '__main__':
  app.run(host='127.0.0.1', port=8000, debug=True)