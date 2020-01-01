# JSON

JSON (JavaScript Object Notation) - yra atviro standarto duomenų perdavimo ir saugojimo formatas.
Su JSON nuolat susidursime traukdami duomenis iš įvairių API, jis taip pat naudojamas įvairiems programų nustatymams 
saugoti, ar tiesiog kažkokiems duomenims. 
Panagrinėkime pavyzdį iš wikipedia'os:

```json
{
  "firstName": "John",
  "lastName": "Smith",
  "isAlive": true,
  "age": 25,
  "address": {
    "streetAddress": "21 2nd Street",
    "city": "New York",
    "state": "NY",
    "postalCode": "10021-3100"
  },
  "phoneNumbers": [
    {
      "type": "home",
      "number": "212 555-1234"
    },
    {
      "type": "office",
      "number": "646 555-4567"
    }
  ],
  "children": [],
  "spouse": null
}
```
Kaip matome, formatas labai primena Python žodynus. 
Jį sudaro objektai su atributo - reikšmės poromis (*key - value pairs*) ir masyvai. 
JSON, kaip standartas, paplito dėl lengvo skaitomumo.
Lentelėje matyti, kaip vadinasi Python objektų ekvivalentai JSON formate.

|Python|JSON|
|--- |--- |
|dict|Object|
|list|Array|
|tuple|Array|
|str|String|
|int|Number|
|float|Number|
|True|true|
|False|false|
|None|null|


Python'e galima atlikti įvairias manipuliacijas su JSON objektais. 
Norint pradėti, reikia importuoti biblioteką:

```python
import json
```

# .loads()
pirmas dalykas, ką galime padaryti tai susikurti string tipo kintamąjį ir perkelti į jį JSON duomenis.

```python
data = '''{
  "student": [ 

     { 
        "id":"01", 
        "name": "Tom", 
        "lastname": "Price" 
     }, 

     { 
        "id":"02", 
        "name": "Nick", 
        "lastname": "Thameson" 
     } 
  ]   
}'''

data_dict = json.loads(data)
print(data_dict)
print(type(data_dict))
```
JSON šiuo atveju buvo iš 'str' paverstas "gimtuoju" Python'o žodynu, pasitelkiant *.loads* metodą.
dabar galime atlikti įvairias manipuliacijas. pvz.:
```python
data_dict['student'][1]['name'] = 'Kyle'
for student in data_dict['student']:
    student.update({'gender':'male'})
print(data_dict)

# {'student': [{'id': '01', 'name': 'Tom', 'lastname': 'Price', 'gender': 'male'}, 
# {'id': '02', 'name': 'Kyle', 'lastname': 'Thameson', 'gender': 'male'}]}
```
ir pan.

# .dumps()

Dabar galime mūsų žodyną vėl perkelti į JSON formatą:

```python
new_json = json.dumps(data_dict, indent=2)
print(new_json)

# {
#   "student": [
#     {
#       "id": "01",
#       "name": "Tom",
#       "lastname": "Price",
#       "gender": "male"
#     },
#     {
#       "id": "02",
#       "name": "Kyle",
#       "lastname": "Thameson",
#       "gender": "male"
#     }
#   ]
# }
```

*indent=2* reiškia, kad norėsime rezultato gražiai atspausdinto, su dviejų tarpų indentacija.

# .load()

norėdami užkrauti JSON objektą iš failo, darome taip:
```python
with open('example.json', 'r') as file:
    data = json.load(file)

print(data)

# [{'id': '0001', 'type': 'donut', 'name': 'Cake', 'ppu': 0.55, 'batters': {'batter': [{'id': '1001', 'type': 'Regular'}, {'id': '1002', 'type': 'Chocolate'}, {'id': '1003', 'type': 'Blueberry'}, {'id': '1004', 'type': "Devil's Food"}]}, 'topping': [{'id': '5001', 'type': 'None'}, {'id': '5002', 'type': 'Glazed'}, {'id': '5005', 'type': 'Sugar'}, {'id': '5007', 'type': 'Powdered Sugar'}, {'id': '5006', 'type': 'Chocolate with Sprinkles'}, {'id': '5003', 'type': 'Chocolate'}, {'id': '5004', 'type': 'Maple'}]}, {'id': '0002', 'type': 'donut', 'name': 'Raised', 'ppu': 0.55, 'batters': {'batter': [{'id': '1001', 'type': 'Regular'}]}, 'topping': [{'id': '5001', 'type': 'None'}, {'id': '5002', 'type': 'Glazed'}, {'id': '5005', 'type': 'Sugar'}, {'id': '5003', 'type': 'Chocolate'}, {'id': '5004', 'type': 'Maple'}]}, {'id': '0003', 'type': 'donut', 'name': 'Old Fashioned', 'ppu': 0.55, 'batters': {'batter': [{'id': '1001', 'type': 'Regular'}, {'id': '1002', 'type': 'Chocolate'}]}, 'topping': [{'id': '5001', 'type': 'None'}, {'id': '5002', 'type': 'Glazed'}, {'id': '5003', 'type': 'Chocolate'}, {'id': '5004', 'type': 'Maple'}]}]
```

# .dump()

.dump() leidžia įrašyti python žodyną į failą:
```python
with open('example2.json', 'w') as file:
    json.dump(data, file, indent=2, sort_keys=True)
```
*sort_keys* išrūšiuoja atributus (keys) pagal abėcelę