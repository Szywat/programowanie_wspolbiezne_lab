import socket
import threading
import pickle
from game_logic import SudokuGame

class SudokuServer:
    def __init__(self, host='127.0.0.1', port=5555):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((host, port))
        self.server.listen()
        self.players = [None, None]
        self.game = SudokuGame()
        self.game_active = False

    def handle_client(self, conn, player_id):
        print(f"Gracz {player_id} połączony.")

        if not self.game_active:
            waiting_state = self.game.get_state()
            waiting_state["status_msg"] = "Czekanie na przeciwnika..."
            conn.send(pickle.dumps({"id": player_id, "state": waiting_state}))
        else:
            conn.send(pickle.dumps({"id": player_id, "state": self.game.get_state()}))

        if self.players[0] and self.players[1]:
            print("Obaj graczej dołączyli. Rozpoczynam rozgrywkę.")
            self.game.generate_board()
            self.game_active = True
            self.broadcast_state()

        try:
            while True:
                data = conn.recv(2048)
                if not data: break
                if not self.game_active: continue

                move = pickle.loads(data)

                success, info = self.game.make_move(player_id, move['r'], move['c'], move['val'])

                if success:
                    print(f"Ruch gracza {player_id}: {info}")
                    self.broadcast_state()

        except Exception as e:
            print(f"Błąd połączenia z graczem {player_id}: {e}")

        finally:
            print(f"Gracz {player_id} rozłączył się.")
            self.players[player_id] = None
            self.game_active = False
            conn.close()

            self.handle_disconnect(player_id)

    def handle_disconnect(self, disconnected_id):
        other_id = 1 - disconnected_id
        other_conn = self.players[other_id]

        if other_conn:
            print(f"Resetowanie gry dla gracza {other_id}...")
            self.game = SudokuGame()

            state = self.game.get_state()
            state["status_msg"] = "Przeciwnik rozłączony. Czekanie..."
            state["scores"] = [0, 0]
            state["board"] = [[0]*9 for _ in range(9)]

            try:
                other_conn.send(pickle.dumps({"state": state}))
            except:
                pass

    def broadcast_state(self):
        state = self.game.get_state()
        state["status_msg"] = ""
        msg = pickle.dumps({"state": state})

        for conn in self.players:
            if conn:
                try: conn.send(msg)
                except: pass

    def start(self):
        print("Serwer nasłuchuje...")
        while True:
            conn, addr = self.server.accept()

            new_player_id = -1
            if self.players[0] is None:
                new_player_id = 0
            elif self.players[1] is None:
                new_player_id = 1

            if new_player_id != -1:
                self.players[new_player_id] = conn
                thread = threading.Thread(target=self.handle_client, args=(conn, new_player_id))
                thread.start()
            else:
                print("Serwer pełny. Odrzucanie połączenia.")
                conn.close()


if __name__ == "__main__":
    SudokuServer().start()