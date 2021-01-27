# Darbas su SQL Python aplinkoje

Python aplinkoje darbas su duomenų bazėmis vyksta importavus atitinkamos duomenų bazės tvarkyklę, pvz:

* Postrgres - psycopg2
* MySQL - mysql-connector-python
* SQLite - sqlite3

Pythone SQLite tvarkyklės papildomai diegti nereikia, ji ateina jau integruota kartu su Python.

Darbas atrodo daugmaž taip:

```python
import sqlite3

conn = sqlite3.connect('zmones.db')
c = conn.cursor()

query = '''
CREATE TABLE draugai (
    f_name VARCHAR(50),
    l_name VARCHAR(50),
    email VARCHAR(100)
);
'''

c.execute(query)
conn.commit()
conn.close()
```
Panagrinėkime detaliau:
* importavome tvarkylę *sqlite3*
* sukūrėme prisijungimo objektą *conn*. Jeigu prieš tai neturėjome failo zmones.db, jis sukuriamas automatiškai.
* jo pagrindu sukūrėme kursoriaus objektą *c*. Su jo metodais vykdomos SQL užklausos.
* *query* yra mūsų SQL užklausa.
* į kursoriaus metodo *excecute* parametrus dedame savo užklausą vykdymui.
* *conn.commit()* - išsaugo pakeitimus duomenų bazėje.
* *conn.close()* - uždarome atidarytą prisijungimą.

Jeigu dar kartą leistumėm tą pačią programą, gautumėm klaidą, kadangi tokia lentelė jau sukurta. Todėl programose kuriant lenteles, pravartu papildyti sąlyga:

```SQL
CREATE TABLE IF NOT EXISTS lentelė (
    ....
```

## Įrašymas 

Vyksta lygiai taip pat, skiriasi tik užklausa:

```python
query = '''
INSERT INTO draugai (f_name, l_name, email) 
VALUES ("Jonas", "Viršaitis", "ponasjonas@gmail.com");
'''
```

Tam, kad po kiekvienos užklausos nereikėtų uždarinėti prisijungimo, galime naudoti *context manager'į*:

```python
import sqlite3

conn = sqlite3.connect("duomenu_baze.db")
c = conn.cursor()

with conn:
    c.execute("INSERT INTO draugai VALUES ('Domantas', 'Rutkauskas', 'd.rutkauskas@imone.lt')")
    c.execute("INSERT INTO draugai VALUES ('Rimas', 'Radzevičius', 'RR@gmail.com')")
```

## Įrašų paieška

*.fetchone()*:
```python
with conn:
    c.execute("SELECT * From darbuotojai WHERE pavarde='Rutkauskas'")
    print(c.fetchall())

# ('Domantas', 'Rutkauskas', 'd.rutkauskas@imone.lt')
```
kitas pvz.:

```python
with conn:
    c.execute("SELECT * From draugai WHERE l_name LIKE 'R%'")
    print(c.fetchone())
# ('Domantas', 'Rutkauskas', 'd.rutkauskas@imone.lt')
```

Jeigu rezultatų daugiau, negu vienas, *.fetchone()* mums spausdina pirmą rezultatą. Norint gauti juos visus, turėtumem naudoti *.fetchall()*:

```python
with conn:
    c.execute("SELECT * From draugai WHERE l_name LIKE 'R%'")
    print(c.fetchall())
```

## Įrašų keitimas ir trynimas

```python
with conn:
    c.execute("UPDATE draugai SET email='naujas.email@aol.com' WHERE l_name='Radzevičius'")
```
```python
with conn:
    c.execute("DELETE from draugai WHERE l_name='Rutkauskas'")
```
Įrašų atnaujinimui ir trynimui nereikia naudoti jokių specifinių metodų.

## Dinaminės užklausos

Jeigu norėtumėm užklausoje panaudoti kintamuosius iš kodo, vienas iš galimų variantų būtų:

```python
import sqlite3

conn = sqlite3.connect("zmones.db")
c = conn.cursor()

vardas = input('Įveskite vardą: ')
with conn:
    c.execute(f"SELECT * From draugai WHERE f_name = '{vardas}'")
    res = c.fetchall()
if res:
    print(res)
else:
    print('nėra tokio vardo!')
```
```bash
Įveskite vardą: Domantas
[('Domantas', 'Rutkauskas', 'd.rutkauskas@imone.lt')]
```
Tarkime, vardas suveikia kaip slaptažodis ir vartotojas gali matyti savo duomenis (labai primityvus pavyzdys :) ).

pamėginkime dar kartą:
```bash
Įveskite vardą: 'OR 1=1--
[('Jonas', 'Viršaitis', 'ponasjonas@gmail.com'), ('Jurgis', 'Vagelis', 'ponasjurgis@gmail.com'), ('Domantas', 'Rutkauskas', 'd.rutkauskas@imone.lt'), ('Rimas', 'Radzevičius', 'RR@gmail.com')]
```

Atsitiko taip, kad mes pratęsėme SQL užklausą ir ji tapo tokia:
```sql
SELECT * From draugai WHERE f_name = '' OR 1=1--'
```

Tai yra vadinama SQL Injection ataka, kuri veikia, kuomet vartotojui yra palikta galimybė pratęsti SQL užklausą. Niekada nekelkite savo kintamųjų tiesiai į užklausas! :)

## Saugus būdas

sqlite3 (kaip ir kitos DB tvarkyklės) turi integruotą sistemą, saugiam kintamųjų naudojimui užklausose:

```python
with conn:
    c.execute("SELECT * From draugai WHERE f_name =?", (vardas,))
    res = c.fetchall()
```
Šiuo atveju klaustukas užklausoje yra pakeičiamas antrame parametre nurodytomis vertėmis. Jis turi būti pateiktas *tuple* formatu. Dabar viskas veikia, kaip priklauso:

```bash
Įveskite vardą: Domantas
[('Domantas', 'Rutkauskas', 'd.rutkauskas@imone.lt')]
```
```bash
Įveskite vardą: OR 1=1--
nėra tokio vardo!
```

Užklausoje galime naudoti ir daugiau klaustukų:

```python
vardas = 'Algimantas'
pavarde = 'Guobys'
email = 'AGuobys@gmail.com'

with conn:
    c.execute("INSERT INTO draugai VALUES(?,?,?)", (vardas, pavarde, email))
```

## *excecutemany()*

Galime įterpti daug įrašų į lentelę vienu kartu, svarbu jas paduoti tinkamu formatu (*list of tuples*):

```python
draugai = [
    ('Jonas', 'Jonaitis', 'jjonaitis@mail.lt'),
    ('Petras', 'Miltelis', 'petras@pastas.lt'),
    ('Inga', 'Guobytė', 'ingag@koksskirtumas.lt')
]

with conn:
    c.executemany("INSERT INTO draugai VALUES(?,?,?)", draugai)
```

## Rowid

*SQLite turi ypatumą - ID stulpelį sukuria automatiškai, todėl kuriant lentelę nebūtina tuo rūpintis. Stulpelis vadinasi **rowid***:

```python
ids = (1, 3, 5)

with conn:
    c.execute("SELECT * FROM draugai WHERE rowid IN (?,?,?)", ids)
    print(c.fetchall())
```

Kitose duomenų bazėse reikėtų kurti atskirą ID, PostgreSQL pvz:

```sql
CREATE TABLE lentele(
    id SERIAL NOT NULL PRIMARY KEY
....
```




