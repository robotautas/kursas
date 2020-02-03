from flask import Flask, render_template, request, redirect, url_for, flash
from dictionary import data
from forms import ContactForm
app = Flask(__name__)

app.config['SECRET_KEY'] = 'bet kokia simbolių eilutė'

@app.route('/', methods=['GET', 'POST'])
def index(): 
    if request.method == 'POST':
        date = request.form['date']
        autorius = request.form['autorius']
        tekstas = request.form['tekstas']
        pavadinimas = request.form['pavadinimas']
        data.append({
            'data': date,
            'autorius': autorius,
            'pavadinimas': pavadinimas,
            'tekstas': tekstas,
            'status': 'published'
        })   
    return render_template('index.html', data=data)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/<string:title>')
def article(title):
    return render_template('article.html', title=title, data=data)

@app.route('/add_article')
def add_article():
    return render_template('add_article.html')

@app.route('/contact_us', methods=['GET', 'POST'])
def contact_us():
    form = ContactForm()
    if form.validate_on_submit():
        return render_template('contact_success.html', form=form)
    return render_template('contact_us.html', form=form)


if __name__ == '__main__':
  app.run(host='127.0.0.1', port=8000, debug=True)

