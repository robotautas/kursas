# Aplinkos kintamieji (Environment Variables)

Dažnai mūsų programos turės jungtis prie tam tikrų paskyrų su slaptažodžiais. Savo kode galime nurodyti *password = 'koks_nors_slaptazodis'*, tačiau tai nėra gera praktika, kadangi saugant programą versijavimo sistemose, ar kažkaip kitaip dalinantis kodu, konfidenciali informacija bus matoma visiems, kas gali perskaityti kodą. Vienas iš gerų būdų spręsti šiai problemai yra slaptos informacijos saugojimas aplinkos kintamuosiuose (environment variables). Skirtingose OS šių kintamųjų nustatymo procesas skiriasi.

## Windows

Windows paieškos langelyje suveskime *advanced system settings* ir iššokusiame langelyje paspauskime mygtuką *Environment Variables*. Paspaudę pirmą *New...* mygtuką įveskime kintamojo pavadinimą ir jo reikšmę.

![](C:\Users\jotau\Desktop\CA\lvl2\envvars\windows_envvars.png)

## Linux (Ubuntu ir derivatyvai)

Su teksto redaktoriumi atidarome /etc/environments ir papildome savo kintamaisiais:
```bash
PATH="/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin" #šitas jau buvo čia
SECRET="123456" # Mūsų naujas kintamasis
```
išsaugojus failą, reikės iš naujo prisiloginti prie savo linux paskyros. 

## MacOS ir kiti linux'ai (jei neveikia aukščiau nurodytas variantas)

[Trumpas filmukas](https://www.youtube.com/watch?v=5iWhQWVXosU)

## Aplinkos kitamųjų pasiekimas per Python

Iš os modulio importuokime environ ir panaudokime metodą *get*:

```python
from os import environ

pswd = environ.get('SECRET')
print(pswd)

# niekas_nesuzinos
```


