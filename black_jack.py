import os
from random import shuffle, choice
import time
from tkinter import Y


class Card:
    def __init__(self, suite, rank):
        self.suite = suite
        self.rank = rank

    @property
    def points(self):
        if self.rank.isdigit():
            return int(self.rank)
        else:
            mapping = {'A': 11, 'J': 10, 'Q': 10, 'K': 10}
            return mapping[self.rank]

    def __add__(self, other):
        return self.points + other.points

    def __radd__(self, other):
        return self.points + other

    def __repr__(self):
        return f'{self.suite}{self.rank}'


class DeckOfCards:
    suites = '♦ ♥ ♣ ♠'.split()
    ranks = '2 3 4 5 6 7 8 9 10 J Q K A'.split()
    cards = []
    for rank in ranks:
        for suite in suites:
            card = Card(suite, rank)
            cards.append(card)

    def shuffle_deck(self):
        shuffle(self.cards)

    def take_out(self):
        taken_card = self.cards[0]
        self.cards = list(self.cards[1:])
        return taken_card

    def __str__(self):
        return f'{self.cards}, {len(self.cards)}'


class Player:
    def __init__(self, deck):
        self.deck = deck
        self.cards = []

    @property
    def qty_of_aces(self):
        qty_of_aces = 0
        for card in self.cards:
            if card.rank == 'A':
                qty_of_aces += 1
        return qty_of_aces

    @property
    def points(self):
        total_points = sum(self.cards)
        if total_points > 21 and self.qty_of_aces > 0:
            for i in range(self.qty_of_aces):
                total_points -= 10
                if total_points <= 21:
                    break
        return total_points

    def check_gt_21(self):
        return self.points > 21

    def draw(self):
        self.cards.append(self.deck.take_out())


class Dealer(Player):
    def __init__(self, deck, player):
        self.deck = deck
        self.player = player
        self.cards = []

    @staticmethod
    def deicide_with_probability(percent):
        acceptable_numbers = [10, 20, 30, 40, 50, 60, 70, 80, 90]
        assert percent in acceptable_numbers
        choose_from = [True for i in range(
            int(percent/10))] + [False for i in range(int((100-percent)/10))]
        return choice(choose_from)

    def make_decision(self):
        while True:
            if self.player.points > self.points:
                self.draw()
                print(f'made decision! my cards now {self.cards}')
            else:
                break

    def deal(self):
        for i in range(2):
            self.draw()
            self.player.draw()

class Game:
    deck = DeckOfCards()
    player = Player(deck=deck)
    dealer = Dealer(deck=deck, player=player)

    def show_table(self, dealer_card_hidden):
        # os.system('clear')
        if dealer_card_hidden:
            print(f"Dealer's cards: [??, {self.dealer.cards[1]}]")
            print(f"Player's cards: {self.player.cards}, {self.player.points} points;")
        else:
            print(f"Dealer's cards: {self.dealer.cards}, {self.dealer.points} points;")
            print(f"Player's cards: {self.player.cards}, {self.player.points} points;")

    def play(self):
        self.deck.shuffle_deck()
        self.dealer.deal()
        self.show_table(dealer_card_hidden=True)
        
        while True:
            decision = input("Draw? (y/n): ")
            if decision == 'y':
                self.player.draw()
                if self.player.points > 21:
                    self.show_table(dealer_card_hidden=True)
                    print('You Lost!')
                    return
                elif self.player.points == 21:
                    self.show_table(dealer_card_hidden=True)
                    print('Black Jack!')
                    break
                self.show_table(dealer_card_hidden=True)
            else:
                break
        self.show_table(dealer_card_hidden=False)
        
        while True:
            time.sleep(1)
            self.dealer.make_decision()
            self.show_table(dealer_card_hidden=False)
            if self.dealer.points > 21:
                print('You win!')
                return
            elif self.dealer.points > self.player.points:
                print('You lost!')
                return
            elif self.dealer.points == self.player.points:
                print('Tie!')
                return


if __name__ == "__main__":
    game = Game()
    game.play()






