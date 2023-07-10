# Django aplikacijų testavimas

Django turi testavimo sistemą, sukurtą *unittest* bibliotekos pagrindu. Paveldėję *TestCase* klasę, galime rašyti testus. Jų struktūra maždaug tokia:

```python
from django.test import TestCase

class YourTestClass(TestCase):
    @classmethod
    def setUpTestData(cls):
        print("""Metodas leidžiasi vieną kartą, sukuria nemodifikuojamus duomenis visiems likusiems testavimo metodams""")
        pass

    def setUp(self):
        print("""sukuria modifikuojamus duomenis kiekvienam testavimo metodui iš naujo""")
        pass

    def test_false_is_false(self):
        print("Method: test_false_is_false.")
        self.assertFalse(False)

    def test_false_is_true(self):
        print("Method: test_false_is_true.")
        self.assertTrue(False)

    def test_one_plus_one_equals_two(self):
        print("Method: test_one_plus_one_equals_two.")
        self.assertEqual(1 + 1, 2)
```

*TestCase* naujoje duomenų bazėje sukuria testinę aplinką, praleidžia testus, ir tą aplinką panaikina. Testuojant Django aplinkoje, mums bus prieinami jau pažįstami *unittest* metodai, taip pat ir Django specifiniai - tokie kaip *assertRedirects, assertTemplateUsed* ir pan.

Library kataloge susikurkime katalogą tests, o jame __init__.py, test_models.py, test_views.py failus.

Programos kataloge esantį *test.py* ištrinkime. Jis tinka testavimui, tačiau per greitai užauga ir tampa nepatogus naudoti.

Į kurį nors iš testavimo failų nukopijuokime aukščiau nagrinėtą struktūros pavyzdį.

iš library katalogo leiskime:

```bash
python manage.py test


Found 3 test(s).
Creating test database for alias 'default'...
System check identified no issues (0 silenced).
Metodas leidžiasi vieną kartą, sukuria nemodifikuojamus duomenis visiems likusiems testavimo metodams
sukuria modifikuojamus duomenis kiekvienam testavimo metodui iš naujo
Method: test_false_is_false.
.sukuria modifikuojamus duomenis kiekvienam testavimo metodui iš naujo
Method: test_false_is_true.
Fsukuria modifikuojamus duomenis kiekvienam testavimo metodui iš naujo
Method: test_one_plus_one_equals_two.
.
======================================================================
FAIL: test_false_is_true (library.tests.test_views.YourTestClass)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "C:\Users\jotau\Desktop\djdjdjdj\mysite\library\tests\test_views.py", line 19, in test_false_is_true
    self.assertTrue(False)
AssertionError: False is not true

----------------------------------------------------------------------
Ran 3 tests in 0.002s

FAILED (failures=1)
Destroying test database for alias 'default'...
```

testus galima leisti atskirai, pvz.:

```bash
python .\manage.py test library.tests.test_views
```

 arba:

```bash
 python .\manage.py test library.tests.test_views.YourTestClass
```

arba netgi atskirą vieną metodą:

```bash
python .\manage.py test library.tests.test_views.YourTestClass.test_one_plus_one_equals_two
```

# Modelių Testavimas

Patestuokime **BookInstance** modelį:

```python
import datetime
from django.test import TestCase
from library.models import Book, BookInstance


class TestBookInstance(TestCase):
    @classmethod
    def setUpTestData(cls):
        BookInstance.objects.create(
            due_back=datetime.date.today() + datetime.timedelta(days=-1)
        )

    # ar teisingai veikia property metodas is_overdue
    def test_overdue(self):
        instance = BookInstance.objects.all()[0]
        self.assertTrue(instance.is_overdue)

    # ar gerai parenkamas numatytas statusas
    def test_default_status(self):
        instance = BookInstance.objects.all()[0]
        self.assertEqual(instance.status, "a")
```

Patestuokime modelį **Book**:

```python
class TestBook(TestCase):
    @classmethod
    def setUpTestData(cls):
        for g in ['genre 1', 'genre 2', 'genre 3', 'genre 4']:
            Genre.objects.create(name=g)

        book = Book.objects.create(title="Test Book")
        book.genre.set(Genre.objects.all())

    # ar teisingas maksimalaus isbn ilgio nustatymas
    def test_isbn_length(self):
        book = Book.objects.get(id=1)
        max_length = book._meta.get_field('isbn').max_length
        self.assertEqual(max_length, 13)

    # ar teisingai atvaizduoja žanrus f-ja display_gere
    def test_display_genre(self):
        book = Book.objects.get(id=1)
        self.assertEqual(book.display_genre(), 'genre 1, genre 2, genre 3')

    # ar nustatomas numatytas paveikslėlis naujai sukurtai knygai
    def test_cover_image_filename(self):
        book = Book.objects.get(id=1)
        self.assertEqual(book.cover.name, 'covers/default.jpg')
  
    # ar knygos paveikslėlio ilgis arba plotis neviršija 300px
    def test_cover_image_size(self):
        book = Book.objects.get(id=1)
        file = book.cover.file
        image = Image.open(file)
        image_shape = image.height, image.width
        self.assertFalse(any([size > 300 for size in image_shape]))
```

# Rodinių testavimas

faile *test_views.py*:

```python
class TestBookListView(TestCase):
    @classmethod
    def setUpTestData(cls):
        for book_id in range(14):
            Book.objects.create(title=f"Book {book_id}")

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get("/books/")
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse("books"))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse("books"))
        self.assertTemplateUsed(response, "book_list.html")

    def test_pagination_is_three(self):
        response = self.client.get(reverse("books"))
        self.assertEqual(response.status_code, 200)
        self.assertTrue("is_paginated" in response.context)
        self.assertTrue(response.context["is_paginated"] == True)
        self.assertEqual(len(response.context["books"]), 3)
```

paprastas generinio rodinio testavimas. Metodų pavadinimai patys save aprašantys. Šiek tiek sudėtingesnis:

```python
class TestLoanedBooksByUserListView(TestCase):
    @classmethod
    def setUpTestData(cls):
        test_user = User.objects.create_user(
            username="Antanas", password="1X<ISRUkw+tuK"
        )
        book = Book.objects.create(title="Fluent Python")
        BookInstance.objects.create(
            due_back=datetime.date.today(), book=book, reader=test_user, status="p"
        )

    # kuomet užeiname neprisijungę, ar redirektina į prisijungimo puslapį
    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse("my-borrowed"))
        self.assertRedirects(response, "/accounts/login/?next=/mybooks/")

    def test_logged_in_uses_correct_template(self):
        login = self.client.login(username="Antanas", password="1X<ISRUkw+tuK")
        response = self.client.get(reverse("my-borrowed"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(str(response.context["user"]), "Antanas")
        self.assertTemplateUsed(response, "user_books.html")

    # Patikriname, ar rodoma knyga atitinka tą, kuri priskirta skaitytojui
    def test_borrowed_books_in_list(self):
        login = self.client.login(username="Antanas", password="1X<ISRUkw+tuK")
        response = self.client.get(reverse("my-borrowed"))
        self.assertEqual(str(response.context["user"]), "Antanas")
        self.assertTrue("bookinstance_list" in response.context)
        self.assertEqual(len(response.context["bookinstance_list"]), 1)
        self.assertEqual(
            response.context["bookinstance_list"][0].book.title, "Fluent Python"
        )
```

Čia jau tikriname prisijungdami kaip vartotojas. Tai, ką rodinys perduoda į šabloną, perimame per response.context metodą.

# URL patterns testavimas

```python
from django.test import TestCase
from django.urls import reverse, resolve
from library.views import BookListView, author_list, author


class TestUrls(TestCase):
    # CBV
    def test_books_url_is_resolved(self):
        url = reverse("books")
        self.assertEqual(resolve(url).func.view_class, BookListView)

    # FBV
    def test_authors_url_is_resolved(self):
        url = reverse("authors")
        self.assertEqual(resolve(url).func, author_list)

    # Detail view
    def test_author_url_is_resolved(self):
        url = reverse("author", args=[1])
        self.assertEqual(resolve(url).func, author)

```

Šiuo atveju testuojame, ar url eilutė veda į jai parašytą funkciją.

<!-- TODO: Formų testavimas. -->
