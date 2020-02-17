# Flask 3 dalis

### Duomenų bazės sukūrimas

Flask leidžia mums dirbti su duomenų bazėmis, praktiškai nesitepant rankų į SQL 
užklausas. Viskuo pasirūpina modulis Flask-SQLAlchemy. Iš principo tai yra 
SQLAlchemy, optimizuota flaskui. Diegiasi *pip install Flask-SQLAlchemy*.

Susikurkime pirmą duomenų bazę:
```python
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

basedir = os.path.abspath(os.path.dirname(__file__))
# pilnas kelias iki šio failo.
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(basedir, 'data.sqlite')
# nustatėme, kad mūsų duomenų bazė bus šalia šio failo esants data.sqlite failas
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# neseksime kiekvienos modifikacijos
db = SQLAlchemy(app)
# sukuriame duomenų bazės objektą
# sukurkime modelį užklausos formai, kuris sukurs duomenų bazėje lentelę


class Query(db.Model):
    # DB lentelei priskiria pavadinimą, jei nenurodysite, priskirs automatiškai pagal klasės pavadinimą.
    __tablename__ = 'messages'
    id = db.Column(db.Integer, primary_key=True)  # stulpelis, kurio reikšmės integer. Taip pat jis bus primary_key.
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    message = db.Column(db.Text, nullable=False)

    def __init__(self, name, email, message):
        self.name = name
        self.email = email
        self.message = message

    def __repr__(self):
        return f'{self.name} - {self.email}'
```
*class Query* yra aprašyta mūsų duomenų bazės lentelė. Paleidus šį failą, duomenų bazė nesusikurs, reikia inicijuoti šį 
veiksmą iš išorės (konsolės arba kito .py skripto). Susikurkime dar vieną python failą:

```python
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
```
*.create_all()* įrašė lentelę į DB, inicijuoti testiniai duomenys taip pat sėkmingai nukeliavo į lentelę, 
atsispausdinome jų ID, kurie buvo sugeneruoti automatiškai.

## Paprastos CRUD operacijos

Susikurkime dar vieną failą, crud operacijų demonstracijai. Atsispausdinkime visus lentelėje esančius objektus:
```python
from app import db, Message

all_messages = Message.query.all()
print(all_messages)

#  [Jonas - jonas@mail.com, Antanas - antanas@mail.lt, Juozas - juozukas@friends.lt, Bronius - bronka@yahoo.com]
```
Atsispausdinkime vieną iš objektų:
```python
message_1 = Message.query.get(1)
print(message_1)

# Jonas - jonas@mail.com
```
Išfiltruokime objektą pagal nurodytą požymį:
```python
message_antanas = Message.query.filter_by(name='Antanas')
print(message_antanas.all())

# [Antanas - antanas@mail.lt]
```
*filter_by* išrinks mums visus įrašus, kuriuose *name='Antanas'*

Pakeiskime Antano el. paštą:
```python
antanas = Message.query.get(2)
antanas.email = 'geras.zmogus@lrs.lt'
db.session.add(antanas)
db.session.commit()
print(Message.query.all())

# [Jonas - jonas@mail.com, Antanas - geras.zmogus@lrs.lt, Juozas - juozukas@friends.lt, Bronius - bronka@yahoo.com]
```

Ištrinkime Joną:
```python
jonas = Message.query.get(1)
db.session.delete(jonas)
db.session.commit()
print(Message.query.all())

# [Antanas - geras.zmogus@lrs.lt, Juozas - juozukas@friends.lt, Bronius - bronka@yahoo.com]
```

## Migracija

Jeigu mums prireiktų papildyti savo lentelę papildomu stulpeliu, tiesiog papildžius klasę Message nauja eilute mums 
nepavyktų, kadangi duomenų bazė jau inicijuota tokia, kokią nurodėme pirmą kartą. Tą reikia turėti omenyje, 
kas kartą, kuriant duomenų bazę stengtis pasidaryti ją kuo išbaigtesnę. Tuomet ateityje, norint ją papildyti naujais 
stulpeliais, ar pakeisti esamų nustatymus, reikės mažiau migracijos procesų. Susitvarkykime savo projektą taip, 
kad galėtumėm vykdyti migracijas:

* nustatykime FLASK-APP aplinkos kintamąjį (*environment variable*). Tą reikės padaryti Windows komandinėje eilutėje, 
arba Linux/MacOS terminale:

* windows - set FLASK_APP=failas_kuriame_musu_db_modelis.py
* linux/macOS - export FLASK_APP=failas_kuriame_musu_db_modelis.py

* įsitikinkite, kad komandą leidžiate iš to paties katalogo, kuriame failas su jūsų DB modeliu.

* įdiekime Flask-Migrate paketą (*pip install Flask-Migrate*)

* pertvarkykime savo .py failą:

```python
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate  # importuojame migracijas

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

Migrate(app, db)  # Susiejame app ir db.


class Message(db.Model):
    __tablename__ = 'messages'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(40), unique=True)  # Papildome duomenų bazės modelį nauju stulpeliu.
    message = db.Column(db.Text, nullable=False)
    
# prie konstruktoriaus irgi nepamirštame pridėti:
    def __init__(self, name, email, message, phone):
        self.name = name
        self.email = email
        self.message = message
        self.phone = phone

    def __repr__(self):
        return f'{self.name} - {self.email}'
```

* Importus papildėme migracijos 'tarnyba':) Jai nurodėme, kokią aplikaciją susieti su kokia duomenų baze. 
Papildėme duomenų bazės modelį nauju stulpeliu (*phone*).

* Inicijuokime migracijas mūsų projektui su komanda **flask db init**:
```bash
(flask-kursui) robotautas@robotautas-MS-7A34:~/Dropbox/Flask 3 dalis/Code$ flask db init
  Creating directory /home/robotautas/Dropbox/Flask 3 dalis/Code/migrations ...  done
  Creating directory /home/robotautas/Dropbox/Flask 3 dalis/Code/migrations/versions ...  done
  Generating /home/robotautas/Dropbox/Flask 3 dalis/Code/migrations/alembic.ini ...  done
  Generating /home/robotautas/Dropbox/Flask 3 dalis/Code/migrations/README ...  done
  Generating /home/robotautas/Dropbox/Flask 3 dalis/Code/migrations/env.py ...  done
  Generating /home/robotautas/Dropbox/Flask 3 dalis/Code/migrations/script.py.mako ...  done
  Please edit configuration/connection/logging settings in '/home/robotautas/Dropbox/Flask 3 dalis/Code/migrations/alembic.ini' before proceeding.
(flask-kursui) robotautas@robotautas-MS-7A34:~/Dropbox/Flask 3 dalis/Code$ ls
app.py  data.sqlite  migrations  __pycache__  setupdb.py  simple_crud.py  test.py
```

* matome, kad sukurtas migracijų katalogas. Dabar paruoškime savo pirmą migraciją, **flask db migrate -m "žinutė atminčiai"** :

```bash
(flask-kursui) robotautas@robotautas-MS-7A34:~/Dropbox/Flask 3 dalis/Code$ flask db migrate -m "pridėtas stulpelis phone"
INFO  [alembic.runtime.migration] Context impl SQLiteImpl.
INFO  [alembic.runtime.migration] Will assume non-transactional DDL.
INFO  [alembic.autogenerate.compare] Detected added column 'messages.phone'
INFO  [alembic.autogenerate.compare] Detected added unique constraint 'None' on '['phone']'
  Generating /home/robotautas/Dropbox/Flask 3 dalis/Code/migrations/versions/d31d8cda085d_pridėtas_stulpelis_phone.py ...  done
```

* matome, kad aptikti pakeitimai. Dabar įvykdykime pačią migraciją, **flask db upgrade**:

```bash
(flask-kursui) robotautas@robotautas-MS-7A34:~/Dropbox/Flask 3 dalis/Code$ flask db upgrade
INFO  [alembic.runtime.migration] Context impl SQLiteImpl.
INFO  [alembic.runtime.migration] Will assume non-transactional DDL.
INFO  [alembic.runtime.migration] Running upgrade  -> d31d8cda085d, pridėtas stulpelis phone
ERROR [root] Error: No support for ALTER of constraints in SQLite dialect

# klaidelę galime ignoruoti, ne visiškas dialekto palaikymas..
```

* patikrinkime, ar suveikė:

```python
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
```

Jeigu atkreipėte dėmesį, migracijų procesas labai panašus į GIT procesus.

# Duomenų bazių ryšiai

