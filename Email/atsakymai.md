### 1

Atsakymas paskaitos kode.

### 2

Python:
```python
import smtplib
from email.message import EmailMessage
from string import Template
from slaptazodis import password

def apmokek(kreipinys, elpastas, suma):
    
    with open('skola.html', 'r') as f:
        html = f.read()

    sablonas = Template(html)
    
    email = EmailMessage()
    email['from'] = 'Skolos administratorius'
    email['to'] = elpastas
    email['subject'] = 'Pranešimas apie įsiskolinimą'

    email.set_content(sablonas.substitute(
        {'kreipinys': kreipinys, 
        'skola': suma, 
        'mail': elpastas}), 
        'html')

    with smtplib.SMTP(host='smtp.gmail.com', port=587) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.login('testavimui2020@gmail.com', password)
        smtp.send_message(email)

apmokek('Antanai', 'adresatas@gmail.com', 25.25)
```

HTML:
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title>Skola</title>
</head>
<body>
    <h2>Gerbiamas $kreipinys,</h2>
    <br>
    <p>Pranešame, kad turite $skola įsiskolinimą. Prašome kuo skubiau padengti.</p>
    <img src="https://res-1.cloudinary.com/crunchbase-production/image/upload/c_lpad,h_256,w_256,f_auto,q_auto:eco/v1500381573/du8m1cvef3vju4vlm6p4.png" alt="logo"/>
    <p>Pagarbiai,</p>
    <p>Skolų administatorius</p>
    <p>tel. 123123123</p>
    <p>el. paštas $mail</p> 
</body>
</html>
```

### 3
```python
import requests
from time import sleep
import smtplib
from email.message import EmailMessage
from slaptazodis import password
from string import Template


def send_mail(error):
    message = '''
    Dėmesio!
    
    Pranešame, kad negautas atsakas iš jūsų serverio. Klaidos žinutė tokia:
    
    $error
    '''
    sablonas = Template(message)
    
    email = EmailMessage()
    email['from'] = 'Vardas Pavardė'
    email['to'] = 'adresatas@gmail.com'
    email['subject'] = 'email from python'

    email.set_content(sablonas.substitute({'error': e}), 'plain')

    with smtplib.SMTP(host='smtp.gmail.com', port=587) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.login('testavimui2020@gmail.com', password)
        smtp.send_message(email)

while True:
    try:
        res = requests.get('http://0.0.0.0:8000')
        print(res.status_code)
        sleep(5)
    except requests.ConnectionError as e:
        send_mail(e)
        break
```

### 4

```python
import requests
from time import sleep
import smtplib
from email.message import EmailMessage
from slaptazodis import password
from datetime import datetime

def send_mail(file):
    message = '''
    Dėmesio!
    
    Pranešame, kad negautas atsakas iš jūsų serverio. Prisegame log.txt
    '''
        
    email = EmailMessage()
    email['from'] = 'Vardas Pavardė'
    email['to'] = 'adresatas@gmail.com'
    email['subject'] = 'email from python'
    
    email.set_content(message)

    with open(file, 'rb') as f:
        content = f.read()
        filename = f.name
        email.add_attachment(
            content, 
            maintype='text/plain', 
            subtype='plain', 
            filename=filename)

    with smtplib.SMTP(host='smtp.gmail.com', port=587) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.login('testavimui2020@gmail.com', password)
        smtp.send_message(email)

while True:
    try:
        res = requests.get('http://0.0.0.0:8000')
        with open('log.txt', 'a') as log:
            log.write(f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} {res.status_code} OK\n')
            sleep(5)
    except requests.ConnectionError as e:
        with open('log.txt', 'a') as log:
            log.write(str(e))
            send_mail('log.txt')
        break
```