from app import db, Message

db.create_all()  # sukurs mūsų lentelę DB

# Iš karto inicijuosime testams keletą įrašų:
jonas = Message('Jonas', 'jonas@mail.com', 'Kažkoks labai rimtas atsiliepimas.')
antanas = Message('Antanas', 'antanas@mail.lt', 'Antano nuomonė labai svarbi.')
juozas = Message('Juozas', 'juozukas@friends.lt', 'Aš labai piktas, nes blogai.')
bronius = Message('Bronius', 'bronka@yahoo.com', 'Aš tai linksmas esu, man patinka.')

# Pridėsime šiuos veikėjus į mūsų DB
db.session.add_all([jonas, antanas, juozas, bronius])
# .commit išsaugo pakeitimus
db.session.commit()

print(jonas.id)
print(antanas.id)
print(bronius.id)
print(juozas.id)

# 1
# 2
# 4
# 3