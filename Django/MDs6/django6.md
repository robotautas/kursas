# Puslapiavimas

Programoje prisikaupus daug informacijos, darosi nepatogu naudotis, kuomet ji atvaizduojama viename naršyklės puslapyje. Įprastai tokia problema sprendžiama išskirstant turinį per keletą puslapių (*pagination*). Pamėginkime tai įgyvendinti su *BookListView*.

views.py:
```python
class BookListView(generic.ListView):
    model = Book
    template_name = "books.html"
    context_object_name = "books"
    paginate_by = 3
```

Taip pat reikia pakoreguoti šabloną, pačioje pabaigoje, prieš *endblock*:

```html
  <div class="pagination">
    <span class="step-links">
        {% if page_obj.has_previous %}
            <a href="?page=1">&laquo; pirmas</a>
            <a href="?page={{ page_obj.previous_page_number }}">atgal</a>
        {% endif %}

        <span class="current">
            {{ page_obj.number }} iš {{ page_obj.paginator.num_pages }}
        </span>

        {% if page_obj.has_next %}
            <a href="?page={{ page_obj.next_page_number }}">pirmyn</a>
            <a href="?page={{ page_obj.paginator.num_pages }}">paskutinis &raquo;</a>
        {% endif %}
    </span>
</div>
```
Logika tokia:
 1. Jeigu puslapio objektas turi puslapių prieš tai (naudojame metodą *has_previous*) - atvaizduokime nuorodą *pirmas* (kuri nukreipia į patį pirmą puslapį) ir nuorodą "atgal" - ji nukreips į puslapį, esantį prieš tai.

 2. Naudodami metodus *number* ir *paginator.num_pages* suformuojame užrašą centre(pvz. 2 iš 3)

 3. Analogiškai pirmam punktui, tik atvirkščiai, suformuojame nuorodas pirmyn ir paskutinis.  

![](knygos_pages.png)

Prireikus puslapiuoti funkcija parašytą *view'są*, darysime taip:

```python
from django.core.paginator import Paginator

def authors(request):   
    authors = Author.objects.all()
    paginator = Paginator(authors, per_page=4)
    page_number = request.GET.get('page')
    paged_authors = paginator.get_page(page_number)
    context = {
        'authors': paged_authors,
    }
    return render(request, template_name="authors.html", context=context)
```

na, o šablone galime pritaikyti taip pat kiek kitokį variantą:

```html
<div class="container">
    <nav aria-label="...">
        {% if authors.has_other_pages %}
            <ul class="pagination pagination-sm justify-content-center">
                {% for i in authors.paginator.page_range %}
                    {% if authors.number == i %}
                        <li class="page-item active">
                            <a class="page-link">{{ i }}</a>
                        </li>
                    {% else %}
                        <li class="page-item">
                            <a class="page-link" href="?page={{ i }}">{{ i }}</a>
                        </li>
                    {% endif %}
                {% endfor %}
            </ul>
        {% endif %}
    </nav>
</div>
```

vaizdas bus toks:

![](autoriai_pages.png)

# Paieška

Tai bus ir nedidelė įžanga į formas, kadangi search taip pat yra forma. 

papildykime navigaciją paieškos laukeliu:
```html
<li>
    <form action="{% url 'search' %}" method="get" class="form-inline my-2 my-md-0">
    <input name="query" class="form-control" type="text" placeholder="Paieška">
    </form>
</li>
```

papildykime *urlslist*'ą nauju endpoint'u:

```python
path('search/', views.search, name='search'),
```

sukurkime naują funkciją *search views.py*:

```python
from django.db.models import Q

def search(request):
    """
    paprasta paieška. query ima informaciją iš paieškos laukelio,
    search_results prafiltruoja pagal įvestą tekstą knygų pavadinimus ir aprašymus.
    Icontains nuo contains skiriasi tuo, kad icontains ignoruoja ar raidės 
    didžiosios/mažosios.
    """
    query = request.GET.get('query')

    book_search_results = Book.objects.filter(
        Q(title__icontains=query) | Q(summary__icontains=query) | Q(isbn__icontains=query) | Q(
            author__first_name__icontains=query) | Q(author__last_name__icontains=query))

    author_search_results = Author.objects.filter(
        Q(first_name__icontains=query) | Q(last_name__icontains=query) | Q(description__icontains=query))

    context = {
        "query": query,
        "books": book_search_results,
        "authors": author_search_results,
    }
    return render(request, template_name="search.html", context=context)
```
Apie Q daugiau informacijos rasite [dokumentacijoje](https://docs.djangoproject.com/en/3.2/topics/db/queries/#complex-lookups-with-q-objects).

Sukurkime naują šabloną *search.html*:

```html
{% extends "base.html" %}

{% block "title" %}Paieškos rezultatai{% endblock %}

{% block "content" %}
<h1>Knygos, rastos pagal paiešką "{{ query }}":</h1>
<br>
{% if books %}
{% for book in books %}
<p><a href="{% url 'book' book.pk %}">{{ book }}</a></p>
{% endfor %}
{% else %}
<p>Oops. Nieko neradome.</p>
{% endif %}
<h1>Autoriai, rasti pagal paiešką "{{ query }}":</h1>
<br>
{% if authors %}
{% for author in authors %}
<p><a href="{% url 'author' author.pk %}">{{ author }}</a></p>

{% endfor %}
{% else %}
<p>Oops. Nieko neradome.</p>
{% endif %}
{% endblock %}
```
![](paieska.png)

Paminėtina tai, jog patogumo dėlei mūsų naudojama SQLite numatytoji duomenų bazė nepalaiko kai kurių funkcijų, pvz 'šveplos' paieškos čia nepadarysite, o tarkime su Postgres - be problemų. Turėkite omeny, kad SQLite produkcijai apskritai nelabai tinkamas variantas. Pvz, esant dideliam konkuruojančių užklausų kiekiui ji mėgsta užsirakinti, programa lūžta. Tačiau ji yra puikus variantas modeliavimui ir prototipavimui.  

# Nuotraukos

Nuotraukas django gali saugoti duomenų bazėje, arba diske. Saugoti nuotraukas duomenų bazėje nerekomenduojama, kadangi ilgainiui tai apsunkina duomenų bazės greitą veikimą. Dažniausiai, ypač programai 'užaugus', mes norėsime kuo greitesnės duombazės. Todėl pamėginkime išspręsti nuotraukų klausimą teisingai. Pradėsime nuo settings.py:

```python
# media folder settings
MEDIA_ROOT = os.path.join(BASE_DIR, 'library/media')

MEDIA_URL = '/media/'
# print(MEDIA_ROOT) - nevenkite padebuginti, bus lengviau nepasiklysti django filesystem džiunglėse
```

dabar, pagrindiniame (projekto) kataloge, atidarykite *urls.py* ir pridėkite eilutę prie pagrindinio sąrašo:

```python
from django.conf.urls.static import static, settings

urlpatterns = [
    path('library/', include('library.urls')),
    path('admin/', admin.site.urls),
    path('', RedirectView.as_view(url='library/', permanent=True)),
] + (static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) +  
    static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT))
```

papildykime *Book* modelį taip, kad jis galėtų turėti paveikslėlius:

```python
cover = models.ImageField('Viršelis', upload_to='covers', null=True, blank=True)
```
nuotraukų procesavimui django naudoja pillow biblioteką, todėl:
```bash
$ pip install pillow
```

Dabar jau galime pridėti nuotraukas per *admin panel*. jeigu atkrepėte dėmesį, 
failų struktūroje atsirado naujas katalogas 'media' o jame 'covers'.

perrašėme *books.html*:

```html
{% load static %}
<h1>Mūsų knygos:</h1>
<br>
<div class="row">
    {% for book in books %}
    <div class="col-md-4 d-flex align-items-stretch">
        <div class="card mb-4 shadow-sm" style="width:300px">
            {% if book.cover %}
            <img src="{{ book.cover.url }}" class="card-img-top" alt="...">
            {% else %}
            <img src="{% static 'img/no-image.png' %}" class="card-img-top">
            {% endif %}
            <div class="card-body">
                <h6 class="card-subtitle mb-2 text-muted">{{ book.author }}</h6>
                <p class="card-text"><a href="{{ book.id }}">{{ book.title }}</a></p>
            </div>
        </div>
    </div>
    {% endfor %}
</div>
```

Tuo pačiu šiek tiek pagyvinome navigaciją, ir turime tokį vaizdą:

![](knygos_images.png)

Parodykime viršelius ir atskirų knygų aprašymuose. Prieš pavadinimo bloką tiesiog įterpkime: 

```html
{% if book.cover %}
<img class="card-img-top" style="max-width: 20%" src="{{ book.cover.url }}">
{% endif %}
```

![](knyga-png.png)


 ## Užduotis
Tęsti kurti Django užduotį – [Autoservisas](https://github.com/robotautas/kursas/wiki/Django-u%C5%BEduotis:-Autoservisas):
* Padaryti, kad įrašai užsakymų puslapyje būtų puslapiuojami (per klasę).
* Padaryti, kad įrašai automobilių puslapyje būtų puslapiuojami (per funkciją).
* Puslapyje įdėti paieškos laukelį, kuris ieškotų automobilių pagal savininką, modelį, valstybinį numerį, VIN kodą
* Padaryti, kad prie automobilio įrašo galima būtų pridėti nuotrauką (per admin puslapį) ir ji būtų atvaizduojama automobilių puslapyje. Nuotrauka būtų atvaizduojama ir vieno automobilio aprašyme.

[Atsakymas](https://github.com/DonatasNoreika/autoservisas)
