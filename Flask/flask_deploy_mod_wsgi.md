## Flask diegimas su Apache

diegsime paprastą testų [programėlę](https://github.com/robotautas/kursas/blob/master/konsultacijos/testu_programa.zip).

prisijungę prie serverio, /var kataloge sukurkime katalogą www.

```
sudo mkdir /var/www
```

padarykime save katalogo savininku:

```
sudo chown -R vartotojas:vartotojas /var/www
```

nukopijuokime iš windows'ų savo projektą į www katalogą:

```
scp -r .\testai\ jt@192.168.1.99:/var/www
```

atnaujinkime sistemą:
```
sudo apt update && sudo apt upgrade
```

įsidiekime pip:

```
sudo apt install python3-pip
```

įdiekime apache2 serverį ir mod_wsgi:
```
sudo apt-get install -y apache2 libapache2-mod-wsgi-py3
```

įsidiekime venv:
```
sudo apt install python3-venv
```

sukurkime virtualią aplinką savo projekto katloge:
```
/var/www/testai$ python3 -m venv testai_env
```

aktyvuokime virtualią aplinką:
```
source testai_env/bin/activate
```

sudiekime paketus iš requirements.txt:

```
/var/www/testai$ pip install -r requirements.txt
```

sukonfigūruokime apache - sudo nano /etc/apache2/sites-enabled/flask.conf

```
<VirtualHost *:80>
                ServerName 192.168.1.99
                ServerAdmin youremail@email.com
                WSGIDaemonProcess testai processes=1 threads=15 python-path=/var/www/testai python-home=/var/www/testai/testai_env
                WSGIProcessGroup testai

                WSGIScriptAlias / /var/www/testai/testai.wsgi
                <Directory /var/www/testai>
                        Require all granted
                </Directory>
                ErrorLog ${APACHE_LOG_DIR}/flask-error.log
                LogLevel warn
                CustomLog ${APACHE_LOG_DIR}/flask-access.log combined
</VirtualHost>
```

* 80 - mūsų standartinis prievadas
* ServerName nurodome serverio IP
* WSGIDaemonProcess ir WSGIProcessGroup testai -> Sukuriame WSGI procesą, kuris vadinasi testai ir priklausys procesų grupei testai, nurodome, kad šiam procesui priklausanti aplikacija yra /var/www/testai kataloge, virtuali aplinka - /var/www/testai/testai_env, taip pat, kad leisime 1 procesą ir 15 threads'ų. Tai yra standartinis nustatymas, jo turėtų pakakti paprastam puslapiui su 10000 apsilankymų per dieną.
* WSGIScriptAlias - nurodome, kur guli wsgi failas
* Directory /var/www/testai nurodome kad projekto katalogą apache pasieks be apribojimų
* nustatome, kur ieškosime log'ų


/etc/apache2/sites-enabled kataloge pakeiskime numatytosios konfigūracijos failo pavadinimą:

```
sudo mv 000-default.conf 000-default.conf.backup
```

susikurkime testai.wsgi savo projekto kataloge:

```
import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/var/www/testai/")

from app import app as application
```

leiskime pakeiskime projekto katalogo ir failų savininką į www-data:
```
sudo chown -R www-data:www-data /var/www/testai
```

perkraukime apache serverį:
```
sudo systemctl restart apache2
```

programa turi veikti :)
