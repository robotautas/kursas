# Type Hinting


## Problema
* Yra 2 programavimo kalbų tipai: statinio tipavimo (C, C++, Go) ir dinaminio tipavimo (Python, JS);
* Statinio tipavimo kalbose kompiliatorius išgaudo daugumą klaidų dar prieš paleidžiant programą.
* Python'o interpretatorius skaito kodą eilutę-po-eilutės **tik paleidus programą** ir užbėgti už akių klaidoms negali.
* Todėl, kuo didesnis Python kodas, tuo sunkiau išgaudyti klaidas. 


## Sprendimas
* Nuo 3.5 versijos, Pythone prasidėjo *gradual typing* - tarpinio (laipsniško, hibridinio) tipavimo vystymas.
* Tarpinis tipavimas leidžia išgaudyti tipavimo klaidas pateikiant kodą *type checker'iui* (tokiam, kaip *mypy*);
* Mypy analizuoja kodą, kuriame naudojame *type hinting*.

## Savybės

* naudoti neprivaloma
* kodo veikimui įtakos nedaro

## Kodėl reikia tai suprasti?

* Naujausiose Python versijose sistema pilnai integruota.
* Savo type checkerius pasigamino ir Google, Microsoft, ir kt.
* Kai kurie moduliai remiasi type hinting sintakse (pydantic, dataclass)
* Perrašytos dokumentacijos
* Ir t.t.

## Privalumai

* Šalia testavimo turime dar vieną įrankį, leidžiantį greičiau pastebėti klaidas
* IDE turi daugiau galimybių mums padėti rašyti kodą
* Kodas tokiu būdu dokumentuojasi.

## Kada naudoti?

* Nykščio taisyklė - jeigu kodas vertas testavimo - jis vertas ir Type Hinting'o·


Paprastas pvz:
```python
name: str = 5
print(name)
```

leidžiant programą įprastai viskas veikia, tačiau mypy analizatorius skundžiasi:

```bash
$mypy programa.py
bandymams.py:2: error: Incompatible types in assignment (expression has type "int", variable has type "str")
Found 1 error in 1 file (checked 1 source file)
```

Kitas pvz.:
```python
name: str = input("Your name?")
age: int = input("Your age?")
print(name, age)
```

```bash
$mypy programa.py
programa.py:2: error: Incompatible types in assignment (expression has type "str", variable has type "int")
Found 1 error in 1 file (checked 1 source file)
```
todėl, kad funkcija input grąžina str.

tipų anotacijos funkcijose:
```python
def greeting(name: str, age: int) -> str:
    return f'Hi, {str}, you are {age} old.'
print(greeting('Jonas', 33))
```
```bash
$mypy programa.py
programa.py:3: error: Argument 2 to "greeting" has incompatible type "str"; expected "int"
Found 1 error in 1 file (checked 1 source file)
```
kitas pvz.:

```python
def capitalize_names(*args: str) -> None:
    for name in args:
        print(name.capitalize())

capitalize_names('jurgis', 'antanas')
```

jeigu norime nebūtinų argumentų:

```python
def multiply(first: float, second: float, absolute: bool|None = None) -> float:
    return abs(first * second) if absolute else first * second

multiply(5, -5)
multiply(5.5, -5, True)
```

kad keletas tipų tiktų vienam parametrui:

```python
def multiply_and_print(content: str|float) -> None:
    print(content * 5)

multiply_and_print(10)
```

Darbas su klasėmis:

```python
from datetime import datetime


class Address:
    def __init__(self, line_1: str, line_2: str) -> None:
        self.line_1 = line_1
        self.line_2 = line_2

    def full_address(self) -> str:
        return f'''{self.line_1}
        {self.line_2}
        '''


class Person:
    def __init__(self, fname: str, lname: str, date_of_birth: datetime, address: Address) -> None:
        self.fname = fname
        self.lname = lname
        self.date_of_birth = date_of_birth
        self.address = address

    def next_birthday(self) -> datetime:
        year = datetime.utcnow().year
        month = self.date_of_birth.month
        day = self.date_of_birth.day
        return datetime(year, month, day)


address1 = Address('Topolių 7-17', 'LT-12345 Alytus')
jonas = Person('Jonas', 'Jonaitis', datetime(1999, 5, 5), address1)
```

jeigu reikia sutipuoti list'ą:
```python
nums: list[int] = [1, 2, 3, 4, 5]
nums_and_strs: list[int|str] = [1, 2, 'three', 4, 5]
```

dict:
```python
kids: dict[str, int] = {'Jonas': 10, 'Ona': 8}
```

tuple:
```python
coords: tuple[float, float] = 54.687157, 25.279652
```

Any tipas leidžia bet kokio tipo reikšmes:

```python
from typing import Any

a: Any = None
a = []          # OK
a = 2           # OK

s: str = ''
s = a           # OK

def foo(item: Any) -> int:
    # Passes type checking; 'item' could be any type,
    # and that type might have a 'bar' method
    item.bar()
```

type aliases:
```python
Vector = list[float]

def scale(scalar: float, vector: Vector) -> Vector:
    return [scalar * num for num in vector]

# passes type checking; a list of floats qualifies as a Vector.
new_vector = scale(2.0, [1.0, -4.2, 5.4])
```

NewType:
```python
from typing import NewType

UserId = NewType('UserId', int)
some_id = UserId(524313)
```

## Užduotys

1. Sutipuokite visas funkcijas šiame faile (nuoroda)
2. Sutipuokite asmens kodo tikrinimo/generavimo funkcijas
3. Sutipuokite biudžeto programą.

**Tikrinimui naudokite sugriežtintą komandą: mypy --disallow-untyped-defs jusu_programa.py**