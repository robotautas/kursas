# Platesnis WHERE panaudojimas
## BETWEEN ...AND

Nurodo žemiausios ir aukščiausios
reikšmių intervalą, išrenkant duomenis iš lentelės, t.y. rezultate
pateikia duomenis tam tikram reikšmių intervalui:

```sql
SELECT * FROM cars WHERE year BETWEEN 1990 AND 1993;
```

![](between.png)

BETWEEN ... AND operatorius apima ir kraštutines reikšmes.

## IN

Išrenka rezultatus pagal pateiktą sąrašą:
```sql
SELECT * FROM cars WHERE year IN (1995, 2000, 2010);
```
![](in.png)

## LIKE

Duomenų išrinkimui iš lentelės naudoja šabloną:
* % - reiškia nulį arba keletą simbolių
* _ - reiškia vieną simbolį

```sql
SELECT * FROM cars WHERE make LIKE'V%';
```

![](like1.png)

kitas pvz. - išrenka eilutes, kuriose modelis iš 2-jų simbolių:

```sql
SELECT * FROM cars WHERE model LIKE'__';
```
![](like2.png)

arba, tarkim:

```sql
SELECT * FROM cars WHERE make LIKE'__n%';
```
išrinktos eilutės, kuriose gamintojo trečia raidė n:

![](like3.png)

## IS NULL

nurodo, jog vartotoją domina tik eilutės lentelėje su
neapibrėžta lauko reikšme:

```sql
SELECT * FROM cars WHERE color IS NULL;
```
![](isnull.png)

## AND, OR, NOT

naudojami sąlygų kombinavimui, pvz:

```sql
SELECT * FROM cars WHERE make = "Ford" AND price > 40000;
```

![](andor1.png)

```sql
SELECT * FROM cars WHERE make = "Ford" OR year > 2012;
```

![](andor2.png)

prieš kiekvieną sąlygą galima naudoti NOT:

```sql
SELECT * FROM cars WHERE color NOT in ("Violet", "Turquoise", "Orange", "Crimson", "Puce");
```

![](not.png)

sudėtingesnis pavyzdys:

```sql
SELECT * FROM cars WHERE (make = "Volvo" OR make = "Ford") AND price NOT BETWEEN 10000 AND 50000;
```
![](orandnot.png)


![](sql_pirmenybes.png)

## ORDER BY, DESC

nustato, kaip turi būti išrūšiuoti duomenys užklausos rezultate. Pvz.:

```sql
SELECT * FROM cars ORDER BY price;
```
![](orderbynum.png)

Jeigu norime atvirkštinio rūšiavimo, naudojame DESC:

```sql
SELECT * FROM cars ORDER BY price DESC;
```
![](orderbynumdesc.png)

analogiškai tekstiniai įrašai rūšiuojasi pagal abėcelę:

```sql
SELECT * FROM cars ORDER BY make DESC;
```

![](orderbyabcdesc.png)

## Case insensitive paieška

```sql
SELECT * FROM cars WHERE make = "toyota" COLLATE NOCASE;
```

![](nocase.png)

## ||

Tai yra sujungimo operatorius (concatenate operator), naudojamas string reikšmių apjungimui paieškos rezultate:

```sql
SELECT "GAMINTOJAS: " || make, model FROM cars;
```
![](concat1.png)

```sql
SELECT make||" "||model AS "full_name", year FROM cars;
```
![](concat2.png)

šiuo atveju nurodėme, kaip vadinsime stulpelį t.y. 'full_name'. 
Kitose DB, pvz Postgres, šiam veiksmui galime naudoti CONCAT paragrafą, tačiau SQLITE jis neveikia. 

## Skaičiavimai

Užklausose galime nurodyti, kokius aritmetinius veiksmus norime atlikti su stulpeliu, prieš jį parodant rezultate:

```sql
SELECT make, model, 2021 - year AS "age" FROM cars;
```
![](age.png)

arba:

```sql
SELECT make, model, price, ROUND(price / 121.0 * 100, 2) AS "be PVM" FROM cars;
```
šiuo atveju naudojome funkciją ROUND gauto rezultato suapvalinimui. Nulis po kablelio (121.0) panaudotas tam, kad gautume *float* reikšmę pirmoje dalyboje.

![](be_pvm.png)

## Grupavimas

grupavimui dažniausiai naudojamos funkcijos:
* **AVG()** - nustato vidurkį grupei
* **COUNT()** - nustato eilučių, kurių išraiška yra apibrėžta, kiekį lentelėje
* **MAX()** - nustato didžiausią reikšmę
* **MIN()** - nustato mažiausią reikšmę
* **SUM()** - nustato bendrą sumą, ignoruojant neapibrėžtas reikšmes

funkcijų naudojimas be grupavimo:
```sql
SELECT MIN(price), MAX(price), AVG(price) from cars;
```
![](minmaxavg.png)

suraskime pigiausią fordą:
```sql
SELECT make, model, min(price) FROM cars WHERE make="Ford";
```

![](cheapest_ford.png)

pavyzdžiai su grupavimu:

išrinkime kiek ir kokių automobilių yra lentelėje:
```sql
SELECT make, count(*) FROM cars GROUP BY make ORDER BY count(*) DESC;
```

![](countmake.png)

padarykime lentelę, kurioje matytųsi brangiausios spalvos:

```sql
SELECT color, max(price), make, model FROM cars GROUP BY color ORDER BY price DESC;
```

![](expensivecolors.png)

Darant kompleksiškas užklausas, reikėtų laikytis tokio eiliškumo:

* SELECT stulpelis, grupinė_funkcija
* FROM lentelė
* [WHERE sąlyga]
* [GROUP BY sąrašas_grupavimui]
* [HAVING grupės sąlyga]
* [ORDER BY rūšiavimo sąlyga]

tarkime:

```sql
SELECT make, model, year, max(price)
FROM cars
WHERE make NOT IN ("Toyota", "Mercury", "Volvo")
GROUP BY price
HAVING year > 2007
ORDER BY make;
```

![](kompleksine.png)

Išrinktos brangiausios mašinos, kurių tarpe nėra toyotų, mercury ir volvo. Išfiltruotos tos, kurios senesnės už 2007m. Išrūšiuotos pagal gamintoją.
