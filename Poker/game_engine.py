# elements/game_engine.py
from Poker.data.session_manager import SessionManager
from deck import *
from datetime import datetime
from player import *
from game_logic import *
from typing import List
from bot_player import *

class GameEngine:
    def __init__(self, players, deck, small_blind=25, big_blind=50):
        self.players = players
        self.deck = deck
        self.small_blind = small_blind
        self.big_blind = big_blind
        self.pot = 0
        self.active_players = players.copy()
        self.session_manager = SessionManager()

    def play_round(self):
        while True:
            self.deck = Deck()
            self.deck.shuffle()
            self.collect_blinds()
            self.deal_cards()
            self.betting_round()
            self.exchange_phase()
            self.showdown()

            play_again = input("czy chcesz kontynuowac [Y/N]")
            if play_again.upper() == "Y":
                continue
            else:
                save_game = input("czy chcesz zapisać [Y/N]")
                if save_game.upper() == "Y":
                    session_data = {
                        "game_id": str(datetime.now().timestamp()),
                        "players": [
                            {"name": p.name, "stack": p.stack, "is_bot": p.is_bot}
                            for p in self.players
                        ],
                        "pot": self.pot,
                        "stage": "showdown"
                    }
                    self.session_manager.save_session(session_data)
                break

    def collect_blinds(self):
        sb_player = self.players[0]
        bb_player = self.players[1 % len(self.players)]
        sb_player.stack -= self.small_blind
        bb_player.stack -= self.big_blind
        self.pot += self.small_blind + self.big_blind
        print(f"{sb_player.name} pays small blind: {self.small_blind}")
        print(f"{bb_player.name} pays big blind: {self.big_blind}")
        for player in self.players:
            print(f"aktualna stawka{player.name}: {player.stack}")

    def deal_cards(self):
        for player in self.players:
            if getattr(player, 'is_bot', False):
                player.hand = self.deck.deal(5)
            else:
                player.hand = self.deck.deal(5)
                print(f"\nKarty gracza {player.name}: {player.cards_to_str()}")




    def betting_round(self):
        current_bet = self.big_blind
        for player in self.active_players:
            if getattr(player, "is_bot", False):
                action = player.decide_action(current_bet)
                print(f"Bot {player.name} wybiera: {action}")
            else:
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
                        player.folded = True  # oznacz gracza jako spasowanego
                        if player in self.active_players:
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
        for player in self.active_players:
            if getattr(player, "is_bot", False):
                indices = player.choose_discard_indices()
                print(f"{player.name} (bot) wymienia karty na pozycjach: {indices}")
            else:
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

        if len(active_players) == 1:
            winner = active_players[0]
            print(f"{winner.name} wygrywa, pozostali gracze spasowali!")
            return winner

        # Przechowujemy: (gracz, siła ręki, opis)
        ranked_players = []
        for player in active_players:
            hand = player.get_player_hand()
            description, strength = hand_rank(hand)
            ranked_players.append((player, strength, description))
            print(f"{player.name} pokazuje: {player.cards_to_str()} — {description}")

        if not ranked_players:
            print("Brak ważnych rąk do oceny.")
            return None

        # Sortujemy po sile ręki (descending)
        ranked_players.sort(key=lambda x: x[1], reverse=True)

        best_strength = ranked_players[0][1]
        winners = [p for p in ranked_players if p[1] == best_strength]
        if len(winners) == 1:
            winner = winners[0][0]
            best_desc = winners[0][2]
            print(f"\nZwycięzca: {winner.name} z układem: {best_desc}")
            print(f"{winner.name} otrzymuje pulę: {self.pot}")
            winner.stack += self.pot
            self.pot = 0
            return winner
        else:
            print("\nRemis pomiędzy: " + ", ".join(p[0].name for p in winners))
            print(f"Układ: {winners[0][2]}")

            share = self.pot // len(winners)
            for p in winners:
                p[0].stack += share
                print(f"{p[0].name} otrzymuje {share} żetonów z puli.")

            self.pot = 0
            return [p[0] for p in winners]
