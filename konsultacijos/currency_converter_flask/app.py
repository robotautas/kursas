from flask import Flask, render_template, request
from funkcijos import get_currencies, get_data

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    res = ''
    if request.method == 'POST':
        from_ = request.form['from']
        to_ = request.form['to']
        amount = request.form['amount']
        res = get_data(amount, from_, to_)
    return render_template('index.html', res=res, currencies=get_currencies())


if __name__ == '__main__':
  app.run(host='127.0.0.1', port=8000, debug=True)