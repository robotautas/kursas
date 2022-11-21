# Užduotis
sukurkite black jack žaidimą konsolėje. Galima veiksmų eiga:
1. Reikės 4-ių klasių - Card, Deck, Player, Dealer, Game.
2. Card turi turėti savybes:
 * suite (♦ ♥ ♣ ♠)
 * rank  (2 3 4 5 6 7 8 9 10 J Q K A)
 * points - kiek taškų turi kokia korta (nuo 2 iki 10 pagal skaičių, J Q K po 10 taškų, A - 11)
 * __repr__
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
