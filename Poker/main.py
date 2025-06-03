import os

from Poker.data.session_manager import SessionManager
from player import Player
from deck import Deck
from game_engine import GameEngine
from bot_player import BotPlayer


def load_saved_game():
    manager = SessionManager()
    save_files = [f for f in os.listdir("data") if f.startswith("session_") and f.endswith(".json")]

    if not save_files:
        print("Brak zapisanych sesji.")
        return None

    print("\n📁 Dostępne zapisy:")
    for idx, fname in enumerate(save_files):
        print(f"{idx+1}. {fname.replace('session_', '').replace('.json', '')}")

    try:
        selected = int(input("Wybierz numer sesji do wczytania: ")) - 1
        if selected < 0 or selected >= len(save_files):
            raise ValueError
    except ValueError:
        print("Nieprawidłowy wybór.")
        return None

    game_id = save_files[selected].replace("session_", "").replace(".json", "")
    session = manager.load_session(game_id)
    if not session:
        return None

    # Odtwarzanie graczy
    players = []
    for pdata in session["players"]:
        if pdata["is_bot"]:
            from bot_player import BotPlayer
            p = BotPlayer(name=pdata["name"], money=pdata["stack"])
        else:
            from player import Player
            p = Player(money=pdata["stack"], name=pdata["name"])
        players.append(p)

    # Talia i silnik
    from deck import Deck
    from game_engine import GameEngine
    deck = Deck()
    return GameEngine(players, deck)

def setup_game():
    num_players = int(input("Ilu graczy bierze udział? "))
    players = []
    marv = 1
    for i in range(num_players):
        czy_bot = input("Czy to bot? [Y/N]")
        if czy_bot.upper() == "Y":
            bot = BotPlayer(name=f"Marvin {marv}", money=500)
            marv += 1
            print(bot.is_bot)
            players.append(bot)
        else:
            name = input(f"Podaj imię gracza {i + 1}: ")
            players.append(Player(200, name))
            print(Player(200, name).is_bot)

    deck = Deck()
    return GameEngine(players, deck)

if __name__ == "__main__":
    if input("📂 Wczytać zapis gry? [T/N]: ").strip().upper() == "T":
        engine = load_saved_game()
        if engine:
            engine.play_round()
        else:
            print("❌ Nie udało się załadować gry.")
    else:
        engine = setup_game()
        engine.play_round()
