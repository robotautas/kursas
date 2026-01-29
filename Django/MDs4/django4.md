# Šablonai

Django naudoja DjangoTemplates šablonų kūrimo kalbą. Ji panaši į Jinja2, naudojamą dirbant su Flask, bet šiek tiek ir skiriasi. Visas django puslapių veikimo mechanizmas atsispindi šiame paveikslėlyje:

![](basic-django.png)

Šioje paskaitoje susidėliosime savo modelį į svetainę. Pradėkime nuo index funkcijos perdarymo views.py:

```python
from django.shortcuts import render
from django.http import HttpResponse
from .models import Book, Author, BookInstance, Genre

def index(request):
    
    # Suskaičiuokime keletą pagrindinių objektų
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()
    
    # Laisvos knygos (tos, kurios turi statusą 'a')
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()
    
    # Kiek yra autorių    
    num_authors = Author.objects.count()
    
    # perduodame informaciją į šabloną žodyno pavidale:
    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
    }

    # renderiname index.html, su duomenimis kintamąjame context
    return render(request, template_name='index.html', context=context)
```

Kaip rašyti Django ORM (SQL) užklausas:
[https://docs.djangoproject.com/en/6.0/topics/db/queries/](https://docs.djangoproject.com/en/6.0/topics/db/queries/)

Trumpus paaiškinimus rasite komentaruose. 

Dabar reikia pasirašyti šabloną *base.html*, kurį naudosime dar daug kartų, jis saugos kiekviename šablone atsikartojančius komponentus, tokius kaip navigacijos skydelis, footer'is ir pan.:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <title>{% block title %}{% endblock %}</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js"></script>
    {% load static %}
    <link rel="stylesheet" href="{% static 'css/styles.css' %}">
</head>
<body>
<div class="p-5 bg-primary text-white text-center">
    <h1>Mūsų rajono biblioteka</h1>
    <p>Demo projektas!</p>
</div>

<nav class="navbar navbar-expand-sm bg-dark navbar-dark">
    <div class="container-fluid">
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#mynavbar">
            <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="mynavbar">
        <ul class="navbar-nav me-auto">
            <li class="nav-item">
                <a class="nav-link" href="{% url 'index' %}">HOME</a>
            </li>
        </ul>
        </div>
    </div>
</nav>

<div class="container mt-4">
    <div class="row">
        <div class="col-sm">
            {% block content %}{% endblock %}
        </div>
    </div>
</div>

<div class="mt-5 p-4 bg-dark text-white text-center">
    <p>© My Library App</p>
</div>

</body>
</html>
```

Kol kas palikime taip, eigoje kažkiek keisime. Atkreipkite dėmesį į 5 eilutę nuo apačios. Joje yra *div* blokas, kuriame talpinsis visa likusi mūsų aplikacijos logika. Pradėkime nuo index.html:

```html
{% extends "base.html" %}

{% block title %}HOME{% endblock %}

{% block content %}
  <h1>Šiuo metu turime:</h1>
  <ul>
    <li><strong>Knygų:</strong> {{ num_books }}</li>
    <li><strong>Egzempliorių:</strong> {{ num_instances }}</li>
    <li><strong>Laisvų egzempliorių:</strong> {{ num_instances_available }}</li>
    <li><strong>Autorių:</strong> {{ num_authors }}</li>
  </ul>
{% endblock %}
```

Taip veikia DjangoTemplates šablonų paveldėjimo mechanizmas. 

* *{% extends "base.html" %}* - nurodome, kad šį turinį talpinsime į base.html 'apvalkalą'.
* *{% block content %} ir {% endblock %}* - rodo, kur bus mūsų 'įterpinio' pradžia ir pabaiga.

Taip pat settings.py galime nurodyti, kur bus mūsų templates katalogas (to nenurodyti nebūtina, tada templates katalogas turi būti mūsų app'so (library) kataloge):

```python
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates'),],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
```

Dar vienas dalykas, kurio reikia nepamiršti - statinių failų susiejimas su programa. Sukurkime */library/static/css/styles.css*:

```css
h1 {
    color: red;
}
```

*/mysite/urls.py* perrašykime sekančiai:

```python
from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('library.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
```

Galbūt atkreipėte dėmesį, *base.html* buvo tokios eilutės:

```html
{% load static %}
  <link rel="stylesheet" href="{% static 'css/styles.css' %}">
```

ir dar, settings.py, pati paskutinė eilutė yra *STATIC_URL = '/static/'*. Pabandykite logiškai susieti šiuos 4 epizodus :) 

Taip Django nurodoma, kur ieškoti statinių failų. Galėsite ant Bootstrap ar kito CSS karkaso viršaus darašinėti savo stiliaus korekcijas. Static, apima ne tik CSS, tačiau ir JS skriptus, paveikslėlius. Pastaruosius aptarsime vėlesnėje eigoje. 

Dabar visų svetainėje esančių h1 tagų tekstai turėtų nusidažyti raudona spalva. Čia pat galime apsirašyti daug papildomo CSS kodo, kuris keis svetainės dizainą.

Štai taip dabar atrodo mūsų aplikacija:

![](screenshot.png)

PAPILDOMAI:

Šiuo metu mūsų veikiančio puslapio URL adresas yra *127.0.0.1:8000/library*. Jeigu neketiname prie to paties projekto rišti daugiau aplikacijų, galime padaryti nukreipimą iš */library* į /. Tam dar kartą atsidarysime /mysite/urls.py ir perrašysime taip:

```python
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView

urlpatterns = [
    path('library/', include('library.urls')),
    path('admin/', admin.site.urls),
    path('', RedirectView.as_view(url='library/', permanent=True)),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
```

# Django templates šablonų (html failų) komentavimas:

Deja Django templates neatpažįsta įprasto PyCharm komentavimo. Tad jei užkomentavote kodą html įprastu būdu - greičiausiai jis vis vien bus matomas ir gali mesti klaidas. Todėl panaudokite kitą komentavimo būdą.

Trumpam komentarui įdėti:
```html
{# some text #}
```

Kelioms eilutėms ar kitam kodui užkomentuoti:
```html
{% comment 'comment_name' %}
{% endcomment %}
```

 ## Užduotis
Tęsti kurti Django užduotį – [Autoservisas](https://github.com/robotautas/kursas/wiki/Django-u%C5%BEduotis:-Autoservisas):
* Pridėti pasirenkamą statuso lauką į užsakymų modelį
* Patobulinti index.html puslapį (ne admin), kuriame būtų matoma statistika: paslaugų kiekis, atliktų užsakymų kiekis, autoservise registruotų automobilių kiekis
* Susikurti savo puslapio stilių (base.html failą). Jei reikia, pridėkite css ir kitus failus (patartina naudoti bootstrap). Galite panaudoti paskaitoje rodytus pavyzdžius. Panaudokite frontend kurse išmoktas žinias! :)
* Padaryti, kad programa matytų static katalogą, išbandyti (įdėti į jį css failą)
* Jeigu reikia, padaryti nukreipimą iš puslapio "/" į "/autoservice" (redirect)

[Atsakymas](https://github.com/DonatasNoreika/autoservisas)
