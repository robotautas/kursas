
from flask import Flask, request, render_template
import pandas as pd
from sqlalchemy import create_engine

engine = create_engine('sqlite:///darbuotojai3.db')
df = pd.read_sql_table("DARBUOTOJAS", engine)
app = Flask(__name__)

@app.route('/', methods=("POST", "GET"))
def html_table():
    return render_template('dataframe.html', tables=[df.to_html(classes='data')], titles=df.columns.values)

if __name__ == '__main__':
    app.run()
