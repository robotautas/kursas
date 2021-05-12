## Vartotojai

*Pastaba: kadangi metodikos dalys buvo kuriamos ne iš eilės, 4 dalies kodo pavyzdyje nematysime nuotraukų dalies*

Pasidarykime paprastą vartotojo registraciją. Pirmiausiai reikės serializatoriaus:

```python
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user
```

Čia buvo beveik copy-paste iš pavyzdžio dokumentacijoje :) Esminis niuansas - slaptažodis turi būti nustatytas per metodą *set_password*, o ne tiesiogiai įmestas iš užklausos. Toliau seka paprasto rodinio sukūrimas *views.py*:

```python
class UserCreate(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.AllowAny, )
```

šiuose failuose, jeigu nėra, reikia nepamiršti importuoti pačios *User* klasės:

```python
from django.contrib.auth.models import User
```

užregistruokime rodinį urls.py:

```python
path('signup', UserCreate.as_view()),
```

## Užklausos iš konsolės

*httpie* pagalba konsolėje galime tikrinti, kaip veikia užklausos į mūsų API. Diegiasi *pip install httpie*. Pamėginkime suformuoti keletą užklausų:

```bash
C:\Users\jotau>http 127.0.0.1:8000/posts
HTTP/1.1 200 OK
Allow: GET, POST, HEAD, OPTIONS
Content-Length: 1071
Content-Type: application/json
Date: Wed, 17 Feb 2021 16:02:22 GMT
Referrer-Policy: same-origin
Server: WSGIServer/0.2 CPython/3.9.1
Vary: Accept, Cookie
X-Content-Type-Options: nosniff
X-Frame-Options: DENY

[
    {
        "body": "lsajdfhgli",
        "comment_count": 0,
        "comments": [],
        "created": "2021-02-15T11:31:07.149937Z",
        "id": 6,
        "likes": 0,
        "title": "dar kazkoksw",
        "user": "juzeris",
        "user_id": 2
    },
    ...
```

Pamėginkime parašyti pranešimą:

```bash
C:\Users\jotau>http --form POST http://127.0.0.1:8000/posts title="šviečia saulė" body="Valio, vitaminas D!"
HTTP/1.1 403 Forbidden
Allow: GET, POST, HEAD, OPTIONS
Content-Length: 58
Content-Type: application/json
Date: Wed, 17 Feb 2021 16:35:27 GMT
Referrer-Policy: same-origin
Server: WSGIServer/0.2 CPython/3.9.1
Vary: Accept, Cookie
X-Content-Type-Options: nosniff
X-Frame-Options: DENY

{
    "detail": "Authentication credentials were not provided."
}
```

Prašo prisijungimo duomenų. Juos galime nurodyti:

```bash
C:\Users\jotau>http -a Antanas:Antanas POST http://127.0.0.1:8000/posts title="šviečia saulė" body="Valio, vitaminas D!"
HTTP/1.1 201 Created
Allow: GET, POST, HEAD, OPTIONS
Content-Length: 175
Content-Type: application/json
Date: Wed, 17 Feb 2021 17:16:35 GMT
Referrer-Policy: same-origin
Server: WSGIServer/0.2 CPython/3.9.1
Vary: Accept, Cookie
X-Content-Type-Options: nosniff
X-Frame-Options: DENY

{
    "body": "Valio, vitaminas D!",
    "comment_count": 0,
    "comments": [],
    "created": "2021-02-17T17:16:35.246104Z",
    "id": 9,
    "likes": 0,
    "title": "šviečia saulė",
    "user": "Antanas",
    "user_id": 3
}
```

Tai nėra labai geras būdas, kadangi su kiekviena užklausa siuntinėjami prisijungimo duomenys. Vienas iš sprendimo būdų - autorizacijos raktai (*tokens*). 

## Autorizacija per *Tokens*

Jų būna daug ir įvairaus sudėtingumo lygio, su skirtingais galiojimo laikais ir pan. Mes nagrinėsime paprasčiausią *web Token'ą*, kuris sugeneruojamas django sistemos, vėliau vartotojo perduotas *headeriuose* identifikuoja užklausos siuntėją kaip unikalų vartotoją. Galima galvoti taip - vartotojo duomenys iškeičiami į žetoną. 

*settings.py* INSTALLED_APPS sąrašą papildykime 

```python
'rest_framework.authtoken',
```

taip pat pridėkime dar vieną kintamąjį:

```python
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
}
```

Turime numigruoti pakeitimus, kadangi duomenų bazėje atsirado žetonų sistema. 

Norėdami gauti žetoną, turime užregistruoti specialų rodinį *urls.py*:

```python
from rest_framework.authtoken.views import obtain_auth_token
...
# papildome sąrašą:
path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
```

Per DRF sąsaja šio '*view'so*' nepalaiko, naudotis žetonais turėsime per konsolę ar programavimą. Saugumas turi savo kainą :)

```bash
C:\Users\jotau>http -a Antanas:Antanas POST http://127.0.0.1:8000/posts title="šviečia saulė" body="Valio, vitaminas D!"
HTTP/1.1 401 Unauthorized
Allow: GET, POST, HEAD, OPTIONS
Content-Length: 58
Content-Type: application/json
Date: Wed, 17 Feb 2021 18:02:28 GMT
Referrer-Policy: same-origin
Server: WSGIServer/0.2 CPython/3.9.1
Vary: Accept
WWW-Authenticate: Token
X-Content-Type-Options: nosniff
X-Frame-Options: DENY

{
    "detail": "Authentication credentials were not provided."
}
```

Kadangi įprasti prisijungimai neveikia, pamėginkime iš pradžių gauti žetoną:

```bash
C:\Users\jotau>http POST http://127.0.0.1:8000/api-token-auth/ username=Antanas password=Antanas
HTTP/1.1 200 OK
Allow: POST, OPTIONS
Content-Length: 52
Content-Type: application/json
Date: Wed, 17 Feb 2021 18:16:57 GMT
Referrer-Policy: same-origin
Server: WSGIServer/0.2 CPython/3.9.1
X-Content-Type-Options: nosniff
X-Frame-Options: DENY

{
    "token": "761fee26e056d4fc065dc4edf7c2b1b9482d6f40"
}
```

Kaip *client* sistema išsaugo žetoną, jau nebe *backender'io* galvos skausmas:) labai priklauso nuo to, kokiomis technologijomis programuojamas front-end'as. Naršyklė turi savo *LocalStorage*, *mobile* ar *desktop* aplikacijos dar kitaip. Nuo šiol visas užklausas, kurios leidimuose nurodytos kaip *IsAuthenticatedOrReadOnly* ar *IsAuthenticated* turėsime pateikti su *headeriuose* nurodytu žetonu. Pvz.:

```bash
C:\Users\jotau>http POST http://127.0.0.1:8000/posts/8/like "Authorization: Token 761fee26e056d4fc065dc4edf7c2b1b9482d6f40"
HTTP/1.1 201 Created
Allow: POST, DELETE, OPTIONS
Content-Length: 8
Content-Type: application/json
Date: Wed, 17 Feb 2021 18:24:52 GMT
Referrer-Policy: same-origin
Server: WSGIServer/0.2 CPython/3.9.1
Vary: Accept
X-Content-Type-Options: nosniff
X-Frame-Options: DENY

{
    "id": 8
}
```

Jeigu užklausą daryti reikėtų per python:

```python
import requests

url = 'http://127.0.0.1:8000/posts/8/like'
headers = {'Authorization': 'Token 761fee26e056d4fc065dc4edf7c2b1b9482d6f40'}
r = requests.post(url, headers=headers)

print(r.json())

# ['Jūs jau palikote patiktuką šiam pranešimui!']
```

# Vartotojų paskyrų šalinimas

pabaigai sukurkime galimybę vartotojui pašalinti savo paskyrą, prie *UserCreate* klasės pridėdami metodą delete():

```python
    def delete(self, request, *args, **kwargs):
        user = User.objects.filter(pk=self.request.user.pk)
        if user.exists():
            user.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            raise ValidationError('User doesn\'t exist.')
```

sutikrinome, ar vartotojas, kurį norime ištrinti egzistuoja (kitaip galima būtų vykdyti post užklausas neprisijungus, kad ir nerezultatyviai), ir delete() metodo pagalba jį šaliname. 

```bash
PS C:\Users\jotau> http DELETE http://127.0.0.1:8000/signup/ "Authorization: Token 8f67be08970bee4fe766bd586a2a8cb719224fc1"
HTTP/1.1 204 No Content
Allow: POST, DELETE, OPTIONS
Content-Length: 0
Date: Thu, 18 Feb 2021 07:24:12 GMT
Referrer-Policy: same-origin
Server: WSGIServer/0.2 CPython/3.9.1
Vary: Accept
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
```
