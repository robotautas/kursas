from flask import Flask, render_template, request, redirect, url_for, flash
from form import ContactForm


app = Flask(__name__)
app.config['SECRET_KEY'] = 'bet kokia simbolių eilutė'

@app.route('/', methods=['GET', 'POST'])
def form():
    form = ContactForm()
    if form.validate_on_submit():
        return render_template('success.html', form=form)
    return render_template('form.html', form=form)


if __name__ == '__main__':
  app.run(host='127.0.0.1', port=8000, debug=True)

