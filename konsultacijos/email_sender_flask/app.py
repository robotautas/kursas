from flask import Flask, render_template, request
import smtplib
from email.message import EmailMessage
from os import environ

app = Flask(__name__)
password = environ.get('PYTHON_EMAIL')


def send_email(address, subject, body):
    email = EmailMessage()
    email['from'] = 'Flask email sender'
    email['to'] = address
    email['subject'] = subject
    email.set_content(body)

    try:
        with smtplib.SMTP(host='smtp.gmail.com', port=587) as smtp:
            smtp.ehlo()
            smtp.starttls()
            smtp.login('testavimui2020@gmail.com', password)
            smtp.send_message(email)
            return 'Message sent!'
    except Exception as e:
        return e


@app.route('/', methods=['GET', 'POST'])
def index():
    error = ''
    if request.method == 'POST':
        address = request.form['address']
        subject = request.form['subject']
        body = request.form['body']
        error = send_email(address, subject, body)
    return render_template('index.html', error=error)

if __name__ == '__main__':
  app.run(host='127.0.0.1', port=8000, debug=True)