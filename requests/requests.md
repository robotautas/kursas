# Requests

*Requests* yra Python biblioteka darbui su HTTP užklausomis. \
Norint pradėti darbą, reikia importuoti requests:
```python
import requests
```
Dabar susikurkime objektą, kuris bus atsakas į mūsų užklausą:
```python
r = requests.get('http://google.com')
```
Turime *response* objektą *r*, kuris turi savo metodus:
```python

print(dir(r))
#[..... '_content', '_content_consumed', '_next', 'apparent_encoding', 'close', 'connection', 'content', 'cookies', 
# 'elapsed', 'encoding', 'headers', 'history', 'is_permanent_redirect', 'is_redirect', 'iter_content', 'iter_lines', 
# 'json', 'links', 'next', 'ok', 'raise_for_status', 'raw', 'reason', 'request', 'status_code', 'text', 'url']
#
``` 
Panagrinėkim keletą svarbesnių: \
#.text
```python
print(r.text)

# <!doctype html><html itemscope="" itemtype="http://schema.org/WebPage" lang="lt"><head><meta content="text/html; charset=UTF-8" http-equiv="Content-Type"><meta content="/images/branding/googleg/1x/googleg_standard_color_128dp.png" itemprop="image"><title>Google</title><script nonce="YrKfNw5dLy3agp25jtREsA==">(function(){window.google={kEI:'m1sIXqSJGI6Kk74Py7So0A0',kEXPI:'0,1353746,5663,731,223,4727,378,206,467,777,1710,250,10,169,544,338,175,354,10,672,482,3,209,69,4,60,315,426,10,199,10,400,193,1128875,143,1197782,367,38,329080,1294,12383,4855,32692,15247,867,28684,369,3314,5505,8384,1700,3159,1361,283,4040,4968,773,2249,4751,3113,6195,1719,1808,1978,10951,1909,3388,2054,918,875,1216,5712,3694,11306,2883,19,319,4148,1,368,2778,520,399,992,1285,8,2796,967,612,14,1279,390,1822,202,328,149,1103,840,517,318,195,953,8,48,820,3438,108,152,52,1137,2,2063,606,1839,184,544,51,1182,522,255,1690,244,503,429,44,1009,93,328,1284,16,84,417,2426,1639,608,473,1339,748,1039,3093,134,773,1216,332,524,8,727,592,1574,3394,1345,3,6510,2244,588,257,215,367,1040,1043,2458,1226,1462,840,1157,73,1864,1275,108,1246,4,21,1002,653,481,809,99,2,315,118,1222,376,638,520,366,127,626,132,989,258,265,358,1157,9,276,2,54,95,507,78,457,231,72,1715,47,88,273,63,162,282,714,1623,43,4,59,1,115,13,2,13,146,138,333,109,373,959,487,10,256,781,189,6,15,198,78,477,91,251,15,65,383,483,217,760,103,1641,326,3,22,5858786,3214,1802680,4194851,2801171,549,333,444,1,2,80,1,900,896,1,8,1,2,2551,1,948,736,2,2,559,1,4265,1,1,1,1,137,1,781,5,5,11,77,8,1,14,5,2,3,3,1,3,5,3,3,3,3,3,1,3,3,3,3,25,6,5,2,2,1,1,6,4,3,1,1,3,10,2,2,4,4,26,2,2,2,2,13,2,2,2,2,19,17,12,2,23964458',authuser:0,kscs:'c9c918f0_m1sIXqSJGI6Kk74Py7So0A0',kGL:'LT',kBL:'v77x'};google.sn='webhp';google.kHL='lt';google.jsfs='Ffpdje';})();(function(){google.lc=[];google.li=0;google.getEI=function(a){for(var b;a&&(!a.getAttribute||!(b=a.getAttribute("eid")));)a=a.parentNode;return b||google.kEI};google.getLEI=function(a){for(var b=null;a&&(!a.getAttribute||!(b=a.getAttribute("leid")));)a=a.parentNode;return b};google.https=function(){return"https:"==window.location.protocol};google.ml=function(){return null};google.time=function(){return(new Date).getTime()};google.log=function(a,b,e,c,g){if(a=google.logUrl(a,b,e,c,g)){b=new Image;var d=google.lc,f=google.li;d[f]=b;b.onerror=b.onload=b.onabort=function(){delete d[f]};google.vel&&google.vel.lu&&google.vel.lu(a);b.src=a;google.li=f+1}};google.logUrl=function(a,b,e,c,g){var d="",f=google.ls||"";e||-1!=b.search("&ei=")||(d="&ei="+google.getEI(c),-1==b.search("&lei=")&&(c=google.getLEI(c))&&(d+="&lei="+c));c="";!e&&google.cshid&&-1==b.search("&cshid=")&&"slh"!=a&&(c="&cshid="+google.cshid);a=e||"/"+(g||"gen_204")+"?atyp=i&ct="+a+"&cad="+b+d+f+"&zx="+google.time()+c;/^http:/i.test(a)&&google.https()&&(google.ml(Error("a"),!1,{src:a,glmm:1}),a="");return a};}).call(this);(function(){google.y={};google.x=function(a,b){if(a)var c=a.id;else{do c=Math.random();while(google.y[c])}google.y[c]=[a,b];return!1};google.lm=[];google.plm=function(a){google.lm.push.apply(google.lm,a)};google.lq=[];google.load=function(a,b,c){google.lq.push([[a],b,c])};google.loadAll=function(a,b){google.lq.push([a,b])};}).call(this);google.f={};(function(){document.documentElement.addEventListener("submit",function(b){var a;if(a=b.target){var c=a.getAttribute("data-submitfalse");a="1"==c||"q"==c&&!a.elements.q.value?!0:!1}else a=!1;a&&(b.preventDefault(),b.stopPropagation())},!0);}).call(this);var a=window.location,b=a.href.indexOf("#");if(0<=b){var c=a.href.substring(b+1);/(^|&)q=/.test(c)&&-1==c.indexOf("#")&&a.replace("/search?"+c.replace(/(^|&)fp=[^&]*/g,"")+"&cad=h")};</script><style>#gbar,#guser{font-size:13px;padding-top:1px !important;}#gbar{height:22px}#guser{padding-bottom:7px !important;text-align:right}.gbh,.gbd{border-top:1px solid #c9d7f1;font-size:1px}.gbh{height:0;position:absolute;top:24px;width:100%}@media all{.gb1{height:22px;margin-right:.5em;vertical-align:top}#gbar{float:left}}a.gb1,a.gb4{text-decoration:underline !important}a.gb1,a.gb4{color:#00c !important}.gbi .gb4{color:#dd8e27 !important}.gbf .gb4{color:#900 !important}
# </style><style>body,td,a,p,.h{font-family:arial,sans-serif}body{margin:0;overflow-y:scroll}#gog{padding:3px 8px 0}td{line-height:.8em}.gac_m td{line-height:17px}form{margin-bottom:20px}.h{color:#36c}.q{color:#00c}.ts td{padding:0}.ts{border-collapse:collapse}em{font-weight:bold;font-style:normal}.lst{height:25px;width:496px}.gsfi,.lst{font:18px arial,sans-serif}.gsfs{font:17px arial,sans-serif}.ds{display:inline-box;display:inline-block;margin:3px 0 4px;margin-left:4px}input{font-family:inherit}a.gb1,a.gb2,a.gb3,a.gb4{color:#11c !important}body{background:#fff;color:black}a{color:#11c;text-decoration:none}a:hover,a:active{text-decoration:underline}.fl a{color:#36c}a:visited{color:#551a8b}a.gb1,a.gb4{text-decoration:underline}a.gb3:hover{text-decoration:none}#ghead a.gb2:hover{color:#fff !important}.sblc{padding-top:5px}.sblc a{display:block;margin:2px 0;margin-left:13px;font-size:11px}.lsbb{background:#eee;border:solid 1px;border-color:#ccc #999 #999 #ccc;height:30px}.lsbb{display:block}.ftl,#fll a{display:inline-block;margin:0 12px}.lsb{background:url(/images/nav_logo229.png) 0 -261px repeat-x;border:none;color:#000;cursor:pointer;height:30px;margin:0;outline:0;font:15px arial,sans-serif;vertical-align:top}.lsb:active{background:#ccc}.lst:focus{outline:none}.tiah{width:458px}</style><script nonce="YrKfNw5dLy3agp25jtREsA=="></script></head><body bgcolor="#fff"><script nonce="YrKfNw5dLy3agp25jtREsA==">(function(){var src='/images/nav_logo229.png';var iesg=false;document.body.onload = function(){window.n && window.n();if (document.images){new Image().src=src;}
# if (!iesg){document.f&&document.f.q.focus();document.gbqf&&document.gbqf.q.focus();}

# ir t.t. (iškirpta)
```
*.text* mums grąžina puslapio turinį numatytuoju formatu (šiuo atveju HTML). \

#.content

*.content* metodas mums grąžina turinį *binary* formatu. pvz.:
```python
r = requests.get('https://www.python.org/static/img/python-logo.png')
print(r.content)
# b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x01"\x00\x00\x00R\x08\x06\x00\x00\x00\xf0\xeb\xd9\xc3\x00\x00\x00\tpHYs\x00\x00\x0b\x13......
```
Iš url eilutės matome, kad turime reikalų su paveikslėliu, greičiausiai kažkokiu logo. Taigi atsispausdinome tą 
paveikslėlį *binary* formate tiesiog į mūsų konsolę. Tokį formatą galime nesunkiai įrašyti į failą:
```python
with open('logo.png', 'wb') as f:
    f.write(r.content)
```
Kataloge, kuriame dirbame pastebėsime naujai atsiradusį logo.png.

 #.status_code
 
*.status_code* mums atspausdina atsako kodą: 
 ```python
r = requests.get('http://python.org')
print(r.status_code)
# 200
```
Pvz. 200 yra OK, 404 - Not Found, 500 - Internal server error ir pan.
daugiau apie šiuos kodus pasiskaitykite [čia](https://httpstatuses.com/).

Šie kodai mums naudingi, jeigu tikriname ar pavyko prisijungimas, Tarkime:
```python
r = requests.get('http://python.org/blabla')
if r.status_code not in range(400, 600):
    print('Pavyko prisijungti! Dirbame toliau...')
else:
    print(f'Kažkas ne taip.. Kodas {r.status_code}')
# Kažkas ne taip.. Kodas 404
``` 

#.ok
prieš tai nagrinėtas pavyzdys gali būti supaprastintas *.ok* metodo pagalba. Jeigu mus tenkina visi kodai, 
mažesni už 400, galime tiesiog:
```python
r = requests.get('http://python.org/blabla')
if r.ok:
    print('važiuojam toliau!')
else:
    print(f'Klaida! kodas {r.status_code}')
# Klaida! kodas 404
```
ok grąžina True ir False reikšmes. 
#.headers
*.headers* grąžina mums papildomus duomenis apie atsaką (*response*):
```python
r = requests.get('http://python.org/')
print(r.headers)
# {'Connection': 'keep-alive', 'Content-Length': '48981', 'Server': 'nginx', 'Content-Type': 'text/html; charset=utf-8',
# 'X-Frame-Options': 'DENY', 'Via': '1.1 vegur, 1.1 varnish, 1.1 varnish', 'Accept-Ranges': 'bytes', 
# 'Date': 'Sun, 29 Dec 2019 10:30:44 GMT', 'Age': '1447', 'X-Served-By': 'cache-iad2131-IAD, cache-bma1647-BMA', 
# 'X-Cache': 'HIT, HIT', 'X-Cache-Hits': '1, 8', 'X-Timer': 'S1577615444.011509,VS0,VE0', 'Vary': 'Cookie', 
# 'Strict-Transport-Security': 'max-age=63072000; includeSubDomains'}
```
iš šio sąrašo ateityje mums gali būti naudingi kai kurie iš jų, pvz:
```python
print(r.headers['content-type'])
# text/html; charset=utf-8
```
Jeigu įdomu, kokie *headers* duomenys ką reiškia, galite pasinagrinėti [čia](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers)
#.url

Kartais, ypač dirbant su daug adresų, naudinga žinoti su kokiu adresu turime reikąlą:
```python
print(r.url)
# https://www.python.org/
```

 
# URL parametrai

Jeigu, tarkime python.org paieškoje suvestumėm *pep* ir paspaustumėm paieškos mygtuką, adresas paieškos laukelyje 
pasikeistų į tokį - *https://www.python.org/search/?q=pep*

tokį laukelį galime panaudoti ir formuodami request'ą:

```python
r = requests.get('https://www.python.org/search/?q=pep')
print(r.text)
```

HTML kode galime atsekti, kad gauname žodžio 'pep' paieškos rezultatus. 
Rankiniu būdu modifikuojant URL eilutę lengva suklysti, todėl requests mums leidžia parametrus nurodyti atskirai *dict* 
formate:
```python
payload = {'q': 'pep', 'page': '2'}
r = requests.get('https://www.python.org/search/', params=payload)
print(r.url)
# https://www.python.org/search/?q=pep&page=2
```

#Kiti HTTP metodai

iki šiol dirbome su .get() metodu, kuris yra bene dažniausiai naudojamas. Tačiau yra ir kiti, tokie kaip *post, put, 
delete, patch*. Labai geras resursas jų visų ištestavimui yra www.httpbin.org . 
pvz.:

```python
r = requests.get('http://httpbin.org/ip')
print(r.text)
# {
#   "origin": "78.63.103.114, 78.63.103.114"
# }
```
Grąžina mums mūsų IP adresą, JSON formate (JSON plačiau panagrinėsime kitose temose).

Panagrinėkime, kaip dirbti su **post** metodu:
```python
data = {'name': 'Jonas', 'lastname': 'Jonaitis'}
r = requests.post('http://httpbin.org/post', data=data)
print(r.text)
# ... 
# "form": {
#     "lastname": "Jonaitis", 
#     "name": "Jonas"
#   }, 
#  ...
```
esminis skirtumas - vietoje *requests.get*, naudojame *requests.post*, vietoje *params* - *data*.







