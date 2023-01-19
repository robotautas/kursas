# Views

Toliau dirbsime su views. Django turi du views įgyvendinimo mechanizmus, vienas iš jų yra *function based*, kitas - *class based views*. Plačiau apie privalumus ir trūkumus ir kodėl apskritai taip yra, jeigu įdomu, pasiskaitykite [čia](https://simpleisbetterthancomplex.com/article/2017/03/21/class-based-views-vs-function-based-views.html), arba django dokumentacijoje. Mūsų pavyzdys leidžia pademonstruoti abu būdus, tad tą ir padarysime. Pradėsime nuo intuityvesnio, function based.

papildykime */library/urls.py*:

```python
urlpatterns = [
    path('', views.index, name='index'),
    path('authors/', views.authors, name='authors'),
]
```

atsidarykime *views.py* ir sukurkime funkciją autorių sąrašui:

```python
def authors(request):
    
    authors = Author.objects.all()
    context = {
        'authors': authors
    }
    print(authors)
    return render(request, 'authors.html', context=context)
```

Sukurkime šabloną:

```html
{% extends "base.html" %}

{% block content %}
  <h1>Autoriai</h1>
  <p>Mūsų knygų autorių sąrašas.</p>
  {% for a in authors %}
    <li>{{a.first_name}} {{a.last_name}}</li>
    {% endfor %}
{% endblock %}
```

Tiesiog banaliai išvardinome autorius, rezultatas atrodo štai taip:

![](autoriai.png)

Sekantis logiškas žingsnis būtų, kad paspaudus ant autoriaus vardo-pavardės mus nuvestų į jo aprašymą. Kadangi mūsų autoriai turi labai mažai laukų, kad jų anketos nebūtų labai nykios, sukurkime jiems tekstinį lauką 'description', ir praleiskime migracijas. 

```python
description = models.TextField('Aprašymas', max_length=2000, default='')
```

Po to reikia sukurti dinaminį URL maršrutą pavieniams autoriams. Įterpkime eilutę į urlpatterns sąrašą faile /library/urls.py:

```python
path('authors/<int:author_id>', views.author, name='author'),
```

kaip sufleruoja šios elutės parametrai, reikia sukurti funkciją *author* faile *views.py*:

```python
from django.shortcuts import render, get_object_or_404

def author(request, author_id):
    single_author = get_object_or_404(Author, pk=author_id)
    return render(request, 'author.html', {'author': single_author})
```

* importuojame funkciją, kuri pagal nurodytą *primary key* traukia konkretų objektą iš modelio *Author*.
* funkcijos parametruose įrašome *author_id*. Jį funkcija pasigaus iš naršyklės, priklausomai, ant kurio autoriaus paspausite.

pakoreguokime *authors.html* taip, kad kiekvienas autorius būtų nuoroda į savo paties aprašymą:

```html
  {% for a in authors %}
    <li><a href="{% url 'author' a.id %}">{{a.first_name}} {{a.last_name}}</a></li>
  {% endfor %}
```

* *{% url 'author' a.id %}* perduoda skaičiuką į *views.py* funkciją. Kuri savo ruožtu pasidalina tuo numeriuku su *urls.py*, todėl URL adrese matysima kažką panašaus į 127.0.0.1:8000/authors/2

belieka sukurti *author.html*:

```html
{% extends "base.html" %}

{% block content %}
    <div class="container author">
    <h4>{{ author.first_name }} {{ author.last_name }}</h4>
    <hr/>
    <p>{{ author.description }}</p>
    </hr>
    </br>
    <h5>Mes turime šias {{ author.first_name }} {{ author.last_name }} knygas:</h5>
    {% for i in author.books.all %}
       <li>{{ i.title }}</li> 
    {% endfor %}
    </div>
{% endblock %}
```

Turime tokį rezultatą:

![](single_author.png)

# Class Based Views

Dabar pamėginkime knygas views'uose išdėlioti per klases. 
Pirmiausiai papildykime urlpatterns sąrašą:

```python
  path('books/', views.BookListView.as_view(), name='books'),
```

Sukurkime klasę views.py:

```python
from django.views import generic

class BookListView(generic.ListView):
    model = Book
    template_name = 'book_list.html'
```

...ir book_list.html:

```html
{% extends "base.html" %}

{% block content %}
  <h1>Knygų sąrašas</h1>
  {% if book_list %}
  <ul>
    {% for book in book_list %}
      <li>
        <a href="{{ book.id }}">{{ book.title }}</a> ({{book.author}})
      </li>
    {% endfor %}
  </ul>
  {% else %}
    <p>Bibliotekoje knygų nėra.</p>
  {% endif %}
{% endblock %}
```

Atrodo ganėtinai paprasta ir mažiau kodo. Viską sugeneruoja automatiškai, pagal tam tikras taisykles. Tačiau, jei prireiktų nestandartinių dalykų, tektų pakeitimus nurodyti klasės atributuose. Tarkime:

```python
class BookListView(generic.ListView):
    model = Book
    # patys galite nustatyti šablonui kintamojo vardą
    context_object_name = 'my_book_list'
    # gauti sąrašą 3 knygų su žodžiu pavadinime 'ir'
    queryset = Book.objects.filter(title__icontains='ir')[:3] 
    # šitą jau panaudojome. Neįsivaizduojate, kokį default kelią sukuria :)
    template_name = 'books/my_arbitrary_template_name_list.html'  
```

Taip pat yra galimybė koreguoti modelio metodus per paveldėjimą:

```python
class BookListView(generic.ListView):
    model = Book

    def get_queryset(self):
        return Book.objects.filter(title__icontains='ir')[:3] 
```

Jei, tarkime, į kontekstą prireiktų pridėti kintamąjį, nesusijusį su pačiu modeliu, galėtume daryti taip:

```python
class BookListView(generic.ListView):
    model = Book

    def get_context_data(self, **kwargs):
        context = super(BookListView, self).get_context_data(**kwargs)
        context['duomenys'] = 'eilutė iš lempos'
        return context
```

Taigi, views'ai per klases yra šiek tiek greičiau rašomi (kai gerai žinote, ką rašyti), tačiau mažiau intuityvūs, nepanašūs į kitų web karkasų metodus. Jeigu modelis turi potencialą darytis sudėtingas, ateityje gali kilti sunkumų, todėl mėgstantiems tiesiog rezultatą, būtų pasiūlymas - iš pradžių CVB view'sų privengti.  

Dabar sukursime klasę pavienių knygų aprašymams:

```python
class BookDetailView(generic.DetailView):
    model = Book
    template_name = 'book_detail.html'
```

Papildykime urlpatterns sąrašą (urls.py):
```python
path('books/<int:pk>', views.BookDetailView.as_view(), name='book-detail'),
```

...ir book_detail.html:

```html
{% extends "base.html" %}

{% block content %}
  <h1>{{ book.title }}</h1>

  <p><strong>Autorius:</strong> <a href="{% url 'author' book.author.pk %}">{{ book.author }}</a></p>
  <p><strong>Aprašymas:</strong> {{ book.summary }}</p>
  <p><strong>ISBN:</strong> {{ book.isbn }}</p> 
  <p><strong>Žanras:</strong> {{ book.genre.all|join:", " }}</p>  

  <div style="margin-left:20px;margin-top:20px">
    <h4>Kopijos:</h4>

    {% for copy in book.bookinstance_set.all %}
      <hr>
      <p class="{% if copy.status == 'a' %}text-success{% elif copy.status == 'm' %}text-danger{% else %}text-warning{% endif %}">
        {{ copy.get_status_display }}
      </p>
      {% if copy.status != 'a' %}
        <p><strong>Bus grąžinta:</strong> {{ copy.due_back }}</p>
      {% endif %}
      <p class="text-muted"><strong>Id:</strong> {{ copy.id }}</p>
    {% endfor %}
  </div>
{% endblock %}
```
Rezultatas:

![](book.png)

Paskutinis dalykas - tai nesujinginėta navigacija. Sutvarkykime base.html:

```html
{% block sidebar %}
        <ul class="sidebar-nav">
          <li><a href="{% url 'index' %}">Pradžia</a></li>
          <li><a href="{% url 'books' %}">Visos knygos</a></li>
          <li><a href="{% url 'authors' %}">Visi autoriai</a></li>
        </ul>
{% endblock %}
```

 ## Užduotis
Tęsti kurti Django užduotį – [Autoservisas](https://github.com/robotautas/kursas/wiki/Django-u%C5%BEduotis:-Autoservisas):
* Sukurti puslapį (per funkciją views faile), pvz. autoservice/automobiliai, kuriame būtų atvaizduoti visi servise užregistruoti automobiliai. 
* Paspaudus ant automobilio nuorodos, būtų rodoma detali informacija apie automobilį (savininkas, automobilio modelis, valstybinis numeris, VIN kodas)
* Sukurti puslapį (per klasę views faile), pvz. autoservice/uzsakymai, kuriame būtų atvaizduoti visi serviso užsakymai.
* Paspaudus ant užsakymo nuorodos, būtų rodoma detali informacija apie užsakymą. Čia pat būtų matomos ir užsakymo eilučių informacija.

[Atsakymas](https://github.com/DonatasNoreika/autoservisas)
