# Užduotis
sukurkite black jack žaidimą konsolėje. Galima veiksmų eiga:
1. Reikės 4-ių klasių - Card, Deck, Player, Dealer, Game.
2. Card turi turėti savybes:
 * suite (kortos rūšis)
 * rank  (kortos rangas)
 * points - kiek taškų turi korta (nuo 2 iki 10 pagal skaičių, J Q K po 10 taškų, A - 11)
 * __repr__
 * __add__, __radd__ - entuziastams :)
3. Deck - turi turėti visas kortas klasės kintamąjame cards, taip pat:
* metodą shuffle_deck
* metodą take_out (vienos kortos išėmimas iš kaladės)
* __repr___
4. Player:
* savybės - cards (listas)
* deck - rišam žaidėją prie kaladės
* property qty_of_aces(taškų skaičiavimui)
* property points
* metodas check_gt_21 (check if greater than 21)
* metodas draw (kuomet žaidėjas pasirenka traukti dar vieną kortą)
5. class Dealer(Player):
* savybės - deck, player (surišam su kitų klasių objektais)
* savybė cards
* metodas make_decision (nusprendžia ar traukti dar vieną kortą)
* metodas deal (padalina sau ir playeriui)
---TO BE CONTINUED---
