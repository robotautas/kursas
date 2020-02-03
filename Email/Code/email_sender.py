# import smtplib # biblioteka susikalbėjimui su pašto serveriu
# from email.message import EmailMessage
# from slaptazodis import password # importuoju slaptažodį, 
#                                  # (galima nurodyti ir tiesiai į parametrus)

# # elementarios email žinutės sukūrimas:
# email = EmailMessage()
# email['from'] = 'Antanas Šampanas'
# email['to'] = 'adresatas@gmail.com'
# email['subject'] = 'email from python'

# email.set_content('Sveiki adresate,\n\nČia yra laiško turinys\n\npagarbiai, siuntėjas')

# with smtplib.SMTP(host='smtp.gmail.com', port=587) as smtp:
#     smtp.ehlo() # žiūrėkite, kaip į pasisveikinimą su serveriu
#     smtp.starttls() # inicijuojame šifruotą kanalą
#     smtp.login('testavimui2020@gmail.com', password) # nurodome prisijungimo duomenis
#     smtp.send_message(email) # išsiunčiame žinutę




import smtplib
from email.message import EmailMessage
from slaptazodis import password
from string import Template
import mimetypes

# with open('index.html', 'r') as f:
#     html = f.read()

# sablonas = Template(html)

# email = EmailMessage()
# email['from'] = 'Antanas Šampanas'
# email['to'] = 'adresatas@gmail.com'
# email['subject'] = 'email from python'

# email.set_content(sablonas.substitute({'vardas': 'Donatas'}), 'html')

# files = ['elephant.png', 'hippo.jpg']

# for file in files:
#     mimetype = mimetypes.guess_type(file)[0]
#     subtype = mimetype.split('/')[1]
#     with open(file, 'rb') as img:
#         content = img.read()
#         email.add_attachment(
#             content, 
#             maintype=mimetype,
#             subtype=subtype, 
#             filename=file)

        

# with smtplib.SMTP(host='smtp.gmail.com', port=587) as smtp:
#     smtp.ehlo()
#     smtp.starttls()
#     smtp.login('testavimui2020@gmail.com', password)
#     smtp.send_message(email)


mimetype = mimetypes.guess_type('elephant.png')[0]
print(mimetype)
subtype = mimetype.split('/')[1]
print(subtype)