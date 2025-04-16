from deck import Deck
from player import Player

deck = Deck()
deck.shuffle()

player1 = Player("Mariusz")
player2 = Player("Bogdan")

player1.receive_cards(deck.deal(5))
player2.receive_cards(deck.deal(5))

print(player1.name, ":", player1.show_hand())
print(player2.name, ":", player2.show_hand())
