import tkinter as tk
from tkinter import messagebox
from deck import Deck
from player import Player
from bot_player import BotPlayer
from game_engine import GameEngine
from data.session_manager import SessionManager
from datetime import *
import os

class PokerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Poker 5-card Draw")
        self.root.geometry("600x400")
        self.root.resizable(False, False)

        self.players = []
        self.deck = Deck()
        self.engine = None
        self.selected_indices = []
        self.current_bet = 50
        self.pot = 0

        self.main_menu()

    def main_menu(self):
        self.clear_window()
        tk.Label(self.root, text="\U0001F3B2 Poker 5-card Draw", font=("Helvetica", 16)).pack(pady=10)
        tk.Button(self.root, text="\U0001F195 Nowa gra", command=self.setup_game).pack(pady=5)
        tk.Button(self.root, text="\U0001F4C2 Wczytaj zapis", command=self.load_game).pack(pady=5)
        tk.Button(self.root, text="❌ Wyjście", command=self.root.quit).pack(pady=5)

    def setup_game(self):
        self.clear_window()
        tk.Label(self.root, text="Podaj liczbę botów:").pack()
        self.num_entry = tk.Entry(self.root)
        self.num_entry.pack()
        tk.Button(self.root, text="Dalej", command=self.create_players).pack(pady=10)

    def create_players(self):
        try:
            num_bots = int(self.num_entry.get())
        except ValueError:
            messagebox.showerror("Błąd", "Podaj poprawną liczbę botów.")
            return

        self.players.clear()
        self.players.append(Player(name="Gracz", money=500))
        for i in range(num_bots):
            self.players.append(BotPlayer(name=f"Bot {i+1}", money=500))

        self.deck = Deck()
        self.engine = GameEngine(self.players, self.deck)
        self.play_round_gui()

    def load_game(self):
        manager = SessionManager()
        saves = [f for f in os.listdir("data") if f.startswith("session_") and f.endswith(".json")]
        if not saves:
            messagebox.showinfo("Info", "Brak zapisanych gier.")
            return

        self.clear_window()
        tk.Label(self.root, text="Wybierz zapis do wczytania:", font=("Helvetica", 12)).pack(pady=10)

        for save_file in sorted(saves, reverse=True):
            game_id = save_file.replace("session_", "").replace(".json", "")
            btn = tk.Button(self.root, text=save_file, command=lambda gid=game_id: self.load_session_by_id(gid))
            btn.pack(pady=2)

        tk.Button(self.root, text="↩️ Powrót do menu", command=self.main_menu).pack(pady=10)

    def load_session_by_id(self, game_id):
        manager = SessionManager()
        session = manager.load_session(game_id)

        if "players" not in session:
            messagebox.showerror("Błąd", "Zapis gry jest uszkodzony.")
            return

        self.players.clear()
        session_players = []
        for pdata in session["players"]:
            if pdata["is_bot"]:
                player = BotPlayer(name=pdata["name"], money=pdata["stack"])
            else:
                player = Player(name=pdata["name"], money=pdata["stack"])
            session_players.append(player)

        # gracz ludzki jako pierwszy
        self.players = [p for p in session_players if not p.is_bot] + [p for p in session_players if p.is_bot]

        self.deck = Deck()
        self.engine = GameEngine(self.players, self.deck)
        self.play_round_gui()

    def play_round_gui(self):
        self.clear_window()
        self.engine.deck.shuffle()
        self.engine.deal_cards()
        self.pot = 0
        self.current_bet = 50
        self.show_betting_gui()

    def show_betting_gui(self):
        self.clear_window()
        human = self.players[0]

        tk.Label(self.root, text=f"Twoje karty: {' '.join(map(str, human.hand))}").pack(pady=10)
        tk.Label(self.root, text=f"Pula: {self.pot}   Aktualny zakład: {self.current_bet}").pack(pady=5)

        self.bet_entry = tk.Entry(self.root)
        self.bet_entry.pack(pady=5)

        tk.Button(self.root, text="Call", command=self.call_action).pack(pady=5)
        tk.Button(self.root, text="Raise", command=self.raise_action).pack(pady=5)
        tk.Button(self.root, text="Fold", command=self.fold_action).pack(pady=5)

    def call_action(self):
        player = self.players[0]
        player.stack -= self.current_bet
        self.pot += self.current_bet
        self.show_human_hand()

    def raise_action(self):
        try:
            amount = int(self.bet_entry.get())
            self.current_bet += amount
            player = self.players[0]
            player.stack -= self.current_bet
            self.pot += self.current_bet
        except ValueError:
            messagebox.showerror("Błąd", "Podaj poprawną kwotę.")
            return
        self.show_human_hand()

    def fold_action(self):
        self.players[0].folded = True
        self.showdown()

    def show_human_hand(self):
        self.clear_window()
        human = self.players[0]

        tk.Label(self.root, text=f"Twoje karty ({human.name}):").pack(pady=10)
        self.cards_frame = tk.Frame(self.root)
        self.cards_frame.pack(pady=10)

        self.card_buttons = []
        self.selected_indices = []
        for idx, card in enumerate(human.hand):
            btn = tk.Button(self.cards_frame, text=str(card), width=5,
                            relief="raised", bg="lightgray")
            btn.grid(row=0, column=idx, padx=5)
            btn.config(command=lambda i=idx, b=btn: self.toggle_card(i, b))
            self.card_buttons.append(btn)

        tk.Button(self.root, text="Wymień zaznaczone", command=self.exchange_selected).pack(pady=10)

    def toggle_card(self, index, button):
        if index in self.selected_indices:
            self.selected_indices.remove(index)
            button.config(relief="raised", bg="lightgray")
        else:
            self.selected_indices.append(index)
            button.config(relief="sunken", bg="lightblue")

    def exchange_selected(self):
        human = self.players[0]
        human.hand = self.engine.exchange_cards(human.hand, self.selected_indices)
        self.selected_indices = []
        self.showdown()

    def showdown(self):
        self.clear_window()
        winner = self.engine.showdown()

        tk.Label(self.root, text="Showdown:", font=("Helvetica", 14)).pack(pady=10)
        for player in self.players:
            if not getattr(player, 'folded', False):
                tk.Label(self.root, text=f"{player.name}: {' '.join(map(str, player.hand))} ({player.stack} żetonów)").pack()

        if isinstance(winner, list):
            result = "Remis: " + ", ".join([w.name for w in winner])
        else:
            result = f"Zwycięzca: {winner.name}"

        tk.Label(self.root, text=result, font=("Helvetica", 14), fg="green").pack(pady=20)
        tk.Button(self.root, text="Zapisz sesję", command=self.save_session).pack(pady=5)
        tk.Button(self.root, text="Kontynuuj następną rundę", command=self.play_round_gui).pack(pady=5)
        tk.Button(self.root, text="Powrót do menu", command=self.main_menu).pack(pady=5)

    def save_session(self):
        session_data = {
            "game_id": str(int(datetime.now().timestamp())),
            "players": [
                {"name": p.name, "stack": p.stack, "is_bot": p.is_bot} for p in self.players
            ],
            "pot": self.pot,
            "stage": "showdown"
        }
        SessionManager().save_session(session_data)
        messagebox.showinfo("Zapisano", "Sesja została zapisana.")

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = PokerApp(root)
    root.mainloop()
