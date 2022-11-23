# Užduotis
sukurkite black jack žaidimą konsolėje. Galima veiksmų eiga:
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
* @property points
* metodas draw (arba hit) - žaidėjas pasirenka traukti papildomą kortą
5. class Dealer(Player):
* savybės - deck, player (surišam su kitų klasių objektais)
* savybė cards
* metodas make_decision - kompiuteris nusprendžia nusprendžia ar traukti dar vieną kortą
* metodas deal - padalina sau ir žaidėjui po 2 kortas
---TO BE CONTINUED---
