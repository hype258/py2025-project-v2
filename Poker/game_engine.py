# elements/game_engine.py
from deck import *
from player import *
from game_logic import *
from typing import List
class GameEngine:
    def __init__(self, players, deck, small_blind=25, big_blind=50):
        self.players = players
        self.deck = deck
        self.small_blind = small_blind
        self.big_blind = big_blind
        self.pot = 0
        self.active_players = players.copy()

    def play_round(self):
        self.deck.shuffle()
        self.collect_blinds()
        self.deal_cards()
        self.betting_round()
        self.exchange_phase()
        self.showdown()

    def collect_blinds(self):
        sb_player = self.players[0]
        bb_player = self.players[1 % len(self.players)]
        sb_player.stack -= self.small_blind
        bb_player.stack -= self.big_blind
        self.pot += self.small_blind + self.big_blind
        print(f"{sb_player.name} pays small blind: {self.small_blind}")
        print(f"{bb_player.name} pays big blind: {self.big_blind}")

    def deal_cards(self):
        for player in self.players:
            player.hand = self.deck.deal(5)
            print(f"\nKarty gracza {player.name}: {player.cards_to_str()}")




    def betting_round(self):
        current_bet = self.big_blind
        for player in self.active_players:
            print(f"\n{player.name}, aktualna stawka: {current_bet}, twój stack: {player.stack}")
            while True:
                action = input("Wybierz akcję (call, raise, fold): ").strip().lower()
                if action == "call":
                    bet = current_bet
                    break
                elif action == "raise":
                    try:
                        raise_amount = int(input("Podaj kwotę podbicia: "))
                        bet = current_bet + raise_amount
                        current_bet = bet
                        break
                    except ValueError:
                        print("Nieprawidłowa kwota.")
                elif action == "fold":
                    self.active_players.remove(player)
                    print(f"{player.name} spasował.")
                    return
                else:
                    print("Nieprawidłowa akcja.")
            player.stack -= bet
            self.pot += bet
            print(f"{player.name} betuje {bet}.")

    def exchange_phase(self):
        """Faza wymiany kart: każdy gracz wymienia karty"""
        for player in self.players:
            print(f"{player.name}, Twoja ręka: {player.cards_to_str()}")
            indices = input("Wybierz karty do wymiany (np. 0 1 3): ").strip().split()
            indices = [int(i) for i in indices]

            try:
                player.hand = self.exchange_cards(player.hand, indices)
            except IndexError:
                print("Błąd: indeksy poza zakresem. Wybierz wartości od 0 do 4.")
                continue

    def exchange_cards(self, hand: List[Card], indices: List[int]) -> List[Card]:
        """Wymienia wskazane karty z ręki gracza"""
        new_cards = self.deck.deal(len(indices))
        for i, index in enumerate(indices):
            self.deck.cards.append(hand[index])  # stare karty trafiają na spód talii
            hand[index] = new_cards[i]
        return hand

    def showdown(self):
        # Lista aktywnych graczy (nie spasowali)
        active_players = [p for p in self.players if not p.folded]

        if not active_players:
            print("Wszyscy spasowali. Brak zwycięzcy.")
            return None

        # Przechowujemy: (gracz, siła ręki, opis)
        ranked_players = []
        for player in active_players:
            hand = player.get_player_hand()
            description, strength = hand_rank(hand)
            ranked_players.append((player, strength, description))
            print(f"{player.name} pokazuje: {player.cards_to_str()} — {description}")

        # Sortujemy po sile ręki (descending)
        ranked_players.sort(key=lambda x: x[1], reverse=True)

        # Najlepszy gracz
        winner = ranked_players[0][0]
        best_desc = ranked_players[0][2]

        print(f"\nZwycięzca: {winner.name} z układem: {best_desc}")
        return winner