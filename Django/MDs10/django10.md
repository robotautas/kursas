# Diegimas į serverį

Čia bus diegimo į serverį instrukcija. Serveryje naudosime Ubuntu linux distribuciją, apache web serverį, mod_wsgi interfeisą (tarpininkas tarp web serverio ir python aplikacijos). 

Šiame pavyzdyje diegsime Django projektą mysite, kuriame yra program myblog (mysite/myblog).

Taigi pradėkime:

prisijunkime per ssh:

```bash
$ ssh jūsų_vartotojas@jūsų_adresas_arba_IP
```
Jei jungsitės per root vartotoją, sudo komandų niekur vesti nereikės.

atnaujinkime mūsų linux paketus:

```bash
sudo apt update && apt upgrade
```

patikrinkime python3 versiją:

```bash
python3 -V
Python 3.6.9
```

Stenkitės, jeigu įmanoma, naudoti kuo naujesnę distribucijos versiją, todėl, kad python3 yra esminė linux sudedamoji, ją atnaujinti į sau pageidaujamą versiją gali būti sudėtinga, nes nuo jos priklauso pačios OS veikimas. Atrodytų galimas variantas atnaujinti į naują distribuciją, tačiau su VPS greičiausiai to padaryti nepavyks. 

patikrinkime, ar turime pip3:

```bash
pip3 -V
-bash: pip3: command not found
```

neturime, todėl: 

```bash
sudo apt install python3-pip
```

įdiekime apache2 serverį ir mod_wsgi:

```bash
sudo apt-get install -y apache2 libapache2-mod-wsgi-py3
```

susikurkime katalogą (jei nėra) savo aplikacijai:

```bash
mkdir /var/www
```

Dabar savo priemonėmis (ftp) nukopijuokime mūsų aplikaciją į /var/www katalogą serveryje (gali tekti pakeisti teises, kad leistų kopijuoti failus į www), galutinis rezultatas bus toks:

```bash
pwd
/var/www/mysite
```

```bash
ls -l
total 216

-rwxrwxr-x 1 root root 208896 May 16 09:09 db.sqlite3
drwxrwxr-x 7 root root   4096 May 13 16:32 myblog
-rwxrwxr-x 1 root root    626 May 16 09:09 manage.py
drwxrwxr-x 3 root root   4096 May 13 16:32 mysite
```

### Susikuriame virtualią aplinką:

Įdiegiame venv:
```bash
sudo apt install python3-venv
```
Sukuriame venv:
```bash
python3 -m venv mysite/venv
```
Aktyvuojame sukurtą aplinką:
```bash
cd mysite/
~/mysite$ source venv/bin/activate
```
Įdiegiame programas iš requirements.txt failo (turime būti aktyvavę sukurtą venv):
```bash
~/mysite$ pip install -r requirements.txt
```

### Konfiguruojame Apache2 serverį:

dabar reikės sukonfigūruoti apache serverį. Mūsų aplikacijai reikės sukurti konfigūracinį failą, *nano /etc/apache2/sites-enabled/django_app.conf*:

```apache
<VirtualHost *:80><VirtualHost *:80>
    ServerName 192.168.1.2

    ErrorLog ${APACHE_LOG_DIR}/django-err.log
    CustomLog ${APACHE_LOG_DIR}/django-acc.log combined

    WSGIDaemonProcess mysite processes=1 threads=15 python-path=/var/www/mysite python-home=/var/www/mysite/venv
    WSGIProcessGroup mysite
    WSGIScriptAlias / /var/www/mysite/mysite/wsgi.py


    Alias /media /var/www/mysite/library/media
    Alias /static /var/www/mysite/static

    <Directory /var/www/mysite/mysite>
        <Files wsgi.py>
            Require all granted
        </Files>
    </Directory>

    <Directory /var/www/mysite/static>
        Require all granted
    </Directory>

    <Directory /var/www/mysite/library/media>
        Require all granted
    </Directory>


</VirtualHost>

```
* <VirtualHost *:80> - reiškia, kad norėsime prieiti prie savo aplikacijos per 80 prievadą. Visus puslapius taip prieiname, galite galite patinkrinti, pvz. http://google.com:80. Tiesiog jeigu nerašome jokio prievado adreso gale, visi serveriai automatiškai nukreipia per :80.

* ServerName nurodome savo serverio adresą arba IP

* error ir access logai - nurodėme, kur iesškosime log'ų.

* alias - logiškai susieja URL adresus su mūsų katalogais. Tarkime jei nukopijuosime kokio nors paveikslėlio adresą ir turėsime http://127.0.0.1:8000/media/covers/paprastos-beprotybes-istorijos.jpg tokią eilutę, Alias užtikrins loginį šio adreso ryšį su adresu failų sistemoje.

* WSGIDaemonProcess ir WSGIProcessGroup mysite -> Sukuriame WSGI procesą, kuris vadinasi mysite ir priklausys procesų grupei mysite, nurodome, kad šiam procesui priklausanti aplikacija yra /var/www/mysite kataloge, virtuali aplinka - /var/www/mysite/venv, taip pat, kad leisime 1 procesą ir 15 threads'ų. Tai yra standartinis nustatymas, jo turėtų pakakti paprastam puslapiui su 10000 apsilankymų per dieną. 

* WSGIScriptAlias / /var/www/mysite/mysite/wsgi.py - nurodome, kur yra mūsų wsgi skriptas. 

* likusioji dalis - nurodome, kad nurodyti katalogai ir failai bus pasiekiami be jokių apribojimų. 

Šiuo metu, užėję į savo puslapį matysime standartinį apache welcome puslapį, nes :80 prievadas kraunasi iš kito failo, kuris yra greta mūsų django_app.conf. Reikia jį tiesiog pervadinti.

```bash
mv 000-default.conf 000-default.conf.backup
```

perkraukime apache:

```bash
sudo systemctl restart apache2
```

užeikime į puslapį:
![](django_error.png)


Pirmas dalykas, ką reikia pataisyti - mūsų settings.py:

```python
...
DEBUG = False

ALLOWED_HOSTS = ["j4sq.l.dedikuoti.lt"]
...

```

Toliau - reikia leisti vartotojui www-data pasiekti visus resusrsus mūsų aplikacijoje, pvz duomenų bazė iki šio momento yra read-only visiems, išskyrus root. www-data yra specialus apache serverio sukurtas vartotojas.

```bash
sudo chown www-data /var/www/mysite
sudo chown www-data /var/www/mysite/db.sqlite3 
```

visada, norėdami matyti pasikeitimus, perkraudinėkime serverį (systemctl restart apache2). Dabar viskas iš pažiūros veikia, tačiau užėjus į administratoriaus puslapį, matome 'nuogą' html'ą:

![](admin_html.png)

virš eilutės *STATIC_URL = '/static/'* faile settings.py įrašykime:

```python
STATICFILES_DIRS = ['/var/www/mysite/library/media']

STATIC_ROOT = '/var/www/mysite/static'

STATIC_URL = '/static/'
```

Nuėję į savo programos katalogą:

```bash
python3 manage.py collectstatic
```

Programa turi veikti. 
https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/


Būtinai perskaitykite šitą, nepalikite savo kode secret key, slaptažodžių ir t.t., yra botai kurie skanuoja visą githubą ieškodami būtent šitų eilučių. 
