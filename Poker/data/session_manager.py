import json
import os
from typing import Dict


class SessionManager:
    def __init__(self, data_dir: str = "data"):
        """
        Inicjalizuje manager sesji i tworzy folder na dane, jeśli nie istnieje.
        """
        self.data_dir = data_dir
        os.makedirs(self.data_dir, exist_ok=True)

    def save_session(self, session: Dict) -> None:
        """
        Zapisuje dane sesji (słownik) do pliku JSON.
        Plik nazwany na podstawie game_id, np. session_123456.json
        """
        game_id = session.get("game_id")
        if not game_id:
            raise ValueError("Brakuje 'game_id' w sesji.")

        path = os.path.join(self.data_dir, f"session_{game_id}.json")
        try:
            with open(path, "w", encoding="utf-8") as f:
                json.dump(session, f, indent=2, ensure_ascii=False)
            print(f"✔ Sesja zapisana: {path}")
        except IOError as e:
            print(f"❌ Błąd zapisu sesji: {e}")

    def load_session(self, game_id: str) -> Dict:
        """
        Ładuje sesję z pliku JSON.
        Zwraca słownik z danymi sesji lub pusty słownik, jeśli błąd.
        """
        path = os.path.join(self.data_dir, f"session_{game_id}.json")
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
            print(f"📥 Sesja {game_id} załadowana.")
            return data
        except FileNotFoundError:
            print(f"⚠ Plik sesji {game_id} nie istnieje.")
            return {}
        except json.JSONDecodeError:
            print(f"⚠ Błąd formatu JSON w sesji {game_id}.")
            return {}
