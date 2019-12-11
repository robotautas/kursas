### Dekoratoriai

Dekoratoriai priima funkcijas, prie tų funkcijų prideda papildomą funkcionalumą, 
ir grąžina rezultatą.
Dekoratorius yra šiek tiek sudėtinga perprasti, ir galbūt praktikoje patiems 
niekada neprireiks rašyti savo dekoratoriaus. 
Tačiau jų veikimo principą suprasti reikia todėl, kad
su jais nuolat susidursime įvairiuose Python framework'uose.
Tam, kad lengviau suprasti dekoratorius, pravartu susipažinti su higher order functions
(aukštesnio rango funkcijos?)

Primityvus pavyzdys:

Turime funkciją, kuri grąžina tekstą:

```pythonstub
def returns_string(some_string):
    return some_string
```

Taip pat naudojame f-ją, kuri į parametrus priima kažkokį tekstą ir šalia jo funkciją:

```python
def returns_upper_string(text, func):
    some_text = func(text)
    if type(some_text) != str:
        return 'input must be a type of string'
    return some_text.upper()
```

f-ja patikrina, ar gautas parametras yra string tipo ir grąžina rezultatą 
visomis didžiosiomis raidėmis. 

```python
print(returns_upper_string('higher order functions!', returns_string))

HIGHER ORDER FUNCTIONS!
```

Tai yra vadinamoji higher order function, jai kaip antras parametras tinka bet kokia funkcija, 
kuri grąžina tekstą. Pvz.:

```python
def returns_reversed_string(string):
    return string[::-1]

print(returns_upper_string('higher order functions!', returns_reversed_string))

#!SNOITCNUF REDRO REHGIH
```

Šiuo atveju sukūrėme dar vieną funkciją, kuri veikia analogiškai pirmąjai, 
tik tekstą grąžina atvirkščiai. Pasiūlius ją aukštesnio rango funkcijai, ji ją puikiai priėmė, bei nuo savęs pridėjo 
papildomo funkcionalumo - ALL CAPS :)

Dabar pamėginsime analogišką rezultatą išgauti rašant dekoratorių:

```python
def upper_decorator(func):
    def wrapper(our_text):
        some_text = func(our_text)
        if type(some_text) != str:
            return 'input must be a type of string'
        return some_text.upper()
    return wrapper
```

Kaip matome, dekoratorius rašomas labai panašiai, kaip ir mūsų aukštesnio rango funkcija, 
tik jos turinys "suvyniojamas" į apvalkalą (wrapper). Į dekoratoriaus parametrus dedame funkciją, kurią jis "apgaubs".
Wrapper parametruose - tos funkcijos parametrai. 

Parašius dekoratorių, python mums leidžia "apvilkti" savo funkcijas naudojant tokią sintaksę:
```python
@upper_decorator
def returns_string(some_string):
    return some_string

@upper_decorator
def returns_reversed_string(string):
    return string[::-1]
```
ir paskui ją labai paprastai iškviesti:
```python
print(returns_string('Decorator!'))
print(returns_reversed_string('Decorator!'))

# DECORATOR!
# !ROTAROCED
```

Praktikoje savo dekoratorių rašymas menkai tikėtinas, tačiau jie labai paplitę pvz. backend'o framework'uose, tokiuose, 
kaip Django arba Flask. Pvz.:

```python
from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'
```

Šiuo atveju nepasimesime ir suprasime, kad mūsų funkciją hello_world gaubia Flask'o modulyje įrašytas dekoratorius *route*.