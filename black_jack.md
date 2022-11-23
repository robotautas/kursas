# Užduotis
sukurkite black jack žaidimą konsolėje. Žaidžia žaidėjas(Player) prieš kompiuterį(Dealer). Žaidimo eiga (taisyklės supaprastintos): 
1. Kompiuteris padalija sau ir žaidėjui po 2 kortas.
* Žaidėjo tikslas surinkti kuo daugiau taškų iki 21, tačiau viršijus pralaimima.
3. Žaidėjui duodama galimybė traukti papildomas kortas, kol jis nuspręs kad gana, arba perrinks ir pralaimės.
4. Kompiuteris sprendžia ar jam reikia papildomų kortų, kad surinktų daugiau už žaidėją. Jeigu reikia - traukia. 
Tikslas - surinkti daugiau už žaidėją, bet neperrinkti.
* Tūzas yra "minkšta" korta - gali turėti 11 arba 1 tašką - kaip naudingiau žaidėjams.

*Supaprastintos taisyklės reiškia, kad atsisakoma statymų, double, split, pasidavimo ir draudimo pirkimo veiksmų. Dyleris tiesiog bando įveikti žaidėją, surinkdamas daugiau taškų.*
 
Galima veiksmų eiga:
1. Reikės 4-ių klasių - Card, Deck, Player, Dealer, Game.
2. Card turi turėti savybes:
 * suite (kortos rūšis)
 * rank  (kortos rangas)
 * points (metodas, kaip savybė) - kiek taškų turi korta (nuo 2 iki 10 pagal skaičių, J Q K po 10 taškų, A - 11)
 * metodą __repr__
 * metodus __add__, __radd__ - entuziastams :)
3. Deck - turi turėti visas kortas (kaip objektus) klasės kintamąjame cards, taip pat:
* metodą shuffle_deck
* metodą take_out (vienos kortos išėmimas iš kaladės)
* __repr___
4. Player:
* savybės - cards (listas)
* deck - rišam žaidėją prie kaladės
* @property qty_of_aces(taškų skaičiavimui)
* @property points - su visa tūzų, kaip "minkštos" kortos logika.
* metodas draw (arba hit) - žaidėjas pasirenka traukti papildomą kortą
5. class Dealer(Player):
* savybės - deck, player (surišam su kitų klasių objektais)
* savybė cards
* metodas make_decision - kompiuteris nusprendžia nusprendžia ar traukti dar vieną kortą
* metodas deal - padalina sau ir žaidėjui po 2 kortas
6. Klasė Game gali prasidėti taip:
```python
class Game:
    deck = Deck()
    player = Player(deck=deck)
    dealer = Dealer(deck=deck, player=player)
```
* metodas show_table (rodo dylerio ir žaidėjo kortas)
* metodas play - jame visa žaidimo logika, while ciklai ir t.t.

##[Atsakymas](https://github.com/robotautas/kursas/blob/master/black_jack.py)
