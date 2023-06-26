# Brėžiniai Django aplinkoje

Pavyzdžiui naudosime index puslapį iš Django metodinės medžiagos ir plotly braižymo biblioteką. Virtualioje aplinkoje reikės susidiegti pandas ir plotly (*pip install plotly pandas*).

Kokie galimi plotly brėžinių tipai galima pažiūrėti [čia](https://plotly.com/python/).

Pateiksiu minimalų pavyzdį, o išplėtosite pagal poreikį naudodamiesi dokumentacija :)

index.html:

```python
# reikalingi papildomi importai
import plotly.express as px
import plotly.offline as po 
import pandas as pd

# index rodinys pakoreguotas atitinkamai:
def index(request):
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()
    num_instances_available = BookInstance.objects.filter(status__exact="g").count()
    num_authors = Author.objects.count()

    # susidedame norimus atvaizuoti duomenis į pandas dataframe
    df = pd.DataFrame(
        dict(
            x=["books", "instances", "available", "authors"],
            y=[num_books, num_instances, num_instances_available, num_authors],
        )
    )

    # pasigaminame stulpelinę diagramą
    fig = px.bar(df, x='x', y='y')
    # suformatuojame taip, kad į šabloną įsikeltų kaip <div> blokas
    bars  = po.plot(fig, output_type='div')

    context = {
        "num_books": num_books,
        "num_instances": num_instances,
        "num_instances_available": num_instances_available,
        "num_authors": num_authors,
        # Įdedame į kontekstq
        "bars": bars
    }

    return render(request, "index.html", context=context)
```

Grafiko tipą, išvaizdą ir kitus parametrus galima koreguoti px.bar parametruose (žr. docs)

index.html norimoje atvaizduoti vietoje:

```
{{ bars|safe }}
```

rezultatas:

![](image/plotly_django/1687756980662.png)
