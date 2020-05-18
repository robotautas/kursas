# Modeliai

Duomenų bazės modeliui imsime paprastą bibliotekos pavyzdį, kuris turi visus reliacinius ryšius:

KNYGA:

* Pavadinimas
* Autorius(One2many) ----> Vardas, knygos(ryšys)
* Aprašymas
* ISBN
* Žanras(Many2many) ---> Pavadinimas, knygos(ryšys)

Knyga turės ne tik aukščiau aprašytus teorinius duomenis, bet ir fizinių kopijų statusą atspindinčią lentelę:

* unikalus ID
* statusas (paskolinta, rezervuota, laisva)
* kada galima pasiskolinti (data)
* ryšys su aprašymu

Django turi nuosavą ORM sistemą, kuri skiriasi nuo SQLAlchemy. Savo aplikacijos modelius kursime models.py faile. Pradėkime nuo pačio paprasčiausio - Žanras:

```python
from django.db import models

class Genre(models.Model):
    name = models.CharField('Pavadinimas', max_length=200, help_text='Įveskite knygos žanrą (pvz. detektyvas)')
    
    def __str__(self):
        return self.name
```
* Importavome modelių paketą
* Sukūrėme klasę *(models.Model)*
* Nurodėme, kad žanro pavadinimas bus iki 200 eilučių string'as, pagalbinį tekstą, kuris matysis administratoriaus svetainėje.
* def __str__ nurodėme, kaip reprezentuosis modelis. 

pridėkime knygos modelį:
```python
from django.urls import reverse #Papildome imports

class Book(models.Model):
    """Modelis reprezentuoja knygą (bet ne specifinę knygos kopiją)"""
    title = models.CharField('Pavadinimas', max_length=200)
    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)
    summary = models.TextField('Aprašymas', max_length=1000, help_text='Trumpas knygos aprašymas')
    isbn = models.CharField('ISBN', max_length=13, help_text='13 Simbolių <a href="https://www.isbn-international.org/content/what-isbn">ISBN kodas</a>')
    genre = models.ManyToManyField(Genre, help_text='Išrinkite žanrą(us) šiai knygai')

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        """Nurodo konkretaus aprašymo galinį adresą"""
        return reverse('book-detail', args=[str(self.id)])
```

Modelis iš esmės pats save aprašantis. Į ką reikėtų atkreipti dėmesį:

* author lauko parametruose *on_delete=models.SET_NULL* reiškia, kad ištrynus autorių, knygą neišsitrins, tiesiog vietoje autoriaus bus nustatytas NULL laukas.
* *null=True* - leidžia duomenų bazėje nurodyti *NULL* reikšmę. Plačiau apie parametro naudojimą [čia](https://i.stack.imgur.com/TMMej.png) ir [čia](https://i.stack.imgur.com/gUanA.png).

Sukurkime dar vieną modelį:

```python
import uuid

class BookInstance(models.Model):
    """Modelis, aprašantis konkrečios knygos kopijos būseną"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='Unikalus ID knygos kopijai')
    book = models.ForeignKey('Book', on_delete=models.SET_NULL, null=True) 
    due_back = models.DateField('Bus prieinama', null=True, blank=True)

    LOAN_STATUS = (
        ('a', 'Administruojama'),
        ('p', 'Paimta'),
        ('g', 'Galima paimti'),
        ('r', 'Rezervuota'),
    )

    status = models.CharField(
        max_length=1,
        choices=LOAN_STATUS,
        blank=True,
        default='a',
        help_text='Statusas',
    )

    class Meta:
        ordering = ['due_back']

    def __str__(self):
        return f'{self.id} ({self.book.title})'
```

UUIDField generuos unikalų identifikacinį numerį, pvz. 81afcd8c-7544-4c0e-b2df-838c0c8c3446. Tai yra alternatyva įprasto id naudojimui. Vėliau pamatysime, kaip tai atrodo praktikoje. Meta klasėje nurodėme, kaip rūšiuosime atvejus.

Pridėkime modelį Author: 

```python
class Author(models.Model):
    """Model representing an author."""
    first_name = models.CharField('Vardas', max_length=100)
    last_name = models.CharField('Pavardė', max_length=100)

    class Meta:
        ordering = ['last_name', 'first_name']

    def get_absolute_url(self):
        """Returns the url to access a particular author instance."""
        return reverse('author-detail', args=[str(self.id)])

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.last_name} {self.first_name}'
```

Modeliai paruošti, dabar paleisime migracijas.

```bash
$ python manage.py makemigrations
Migrations for 'library':
  library/migrations/0001_initial.py
    - Create model Author
    - Create model Book
    - Create model Genre
    - Create model BookInstance
    - Add field genre to book
```

```bash
$ python manage.py migrate
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, library, sessions
Running migrations:
  Applying library.0001_initial... OK
```

gavome štai tokią schemą:
![](schema.png)

# Administratoriaus svetainė

Dabar, kai jau numigravome mūsų ilgai ruoštus duomenų bazės modelius, užregistruokime juos administratoriaus svetainėje. Atsidarykime admin.py ir pridėkime:

```python
from .models import Author, Genre, Book, BookInstance

admin.site.register(Book)
admin.site.register(Author)
admin.site.register(Genre)
admin.site.register(BookInstance)
```

Susikurkime supervartotoją (prisijungimas administratoriui):

```bash
$ python manage.py createsuperuser
Username (leave blank to use 'your_current_linux_user'): admin
Email address: 
Password: 
Password (again): 
This password is too short. It must contain at least 8 characters.
Bypass password validation and create user anyway? [y/N]: y
Superuser created successfully.
```

Prisijunkime prie 127.0.0.1:8000/admin ir susiveskime po keletą objektų!

## Užduotis
Pradėti kurti Django užduotį – [Autoservisas](https://github.com/robotautas/kursas/wiki/Django-u%C5%BEduotis:-Autoservisas):
* Sukurti naują Django projektą su appsu Autoservice
* Sukurti visus modelius pagal nurodytą programos DB struktūrą
* Sukurti meniu punktus visiems sukurtiems modeliams
* Susikurti superuser vartotoją, prisijungti ir išbandyti įrašyti visų modelių įrašus


