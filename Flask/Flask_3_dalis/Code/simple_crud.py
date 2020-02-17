from app import db, Message
from random import randint

# all_messages = Message.query.all()
# print(all_messages)
#
# #  [Jonas - jonas@mail.com, Antanas - antanas@mail.lt, Juozas - juozukas@friends.lt, Bronius - bronka@yahoo.com]
#
# message_1 = Message.query.get(1)
# print(message_1)
#
# # Jonas - jonas@mail.com
#
# message_antanas = Message.query.filter_by(name='Antanas')
# print(message_antanas.all())
#
# # [Antanas - antanas@mail.lt]
#
# antanas = Message.query.get(2)
# antanas.email = 'geras.zmogus@lrs.lt'
# db.session.add(antanas)
# db.session.commit()
# print(Message.query.all())
#
# # [Jonas - jonas@mail.com, Antanas - geras.zmogus@lrs.lt, Juozas - juozukas@friends.lt, Bronius - bronka@yahoo.com]
#
# jonas = Message.query.get(1)
# db.session.delete(jonas)
# db.session.commit()
# print(Message.query.all())
#
# # [Antanas - geras.zmogus@lrs.lt, Juozas - juozukas@friends.lt, Bronius - bronka@yahoo.com]

messages = Message.query.all()

for i in messages:
    random_phone = randint(999999, 10000000)
    i.phone = str(random_phone)
    db.session.add(i)

db.session.commit()

for x in messages:
    print (f'{x.id}, {x.name}, {x.email}, {x.phone}, {x.message}')

# 2, Antanas, geras.zmogus@lrs.lt, 9033639, Antano nuomonė labai svarbi.
# 3, Juozas, juozukas@friends.lt, 2233484, Aš labai piktas, nes blogai.
# 4, Bronius, bronka@yahoo.com, 4211290, Aš tai linksmas esu, man patinka.

# antanas.phone = '123123'
# juozas.phone = '321321'
# bronius.phone = '159915'
#
# db.session.add_all([antanas, juozas, bronius])
# db.session.commit()
#
# for i in Message.query.all():
#     print(f'{i.name}, {i.email}, {i.phone}, {i.message}')

