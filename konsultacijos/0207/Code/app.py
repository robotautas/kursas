from flask import Flask, render_template, request
from logika import get_table

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        number = request.form['number']
        print(number)
        return render_template('index.html', table=get_table(number))
    return render_template('index.html', table=get_table())

if __name__ == "__main__":
    app.run(debug=True)