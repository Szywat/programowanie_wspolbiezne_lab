import socket
import threading
import pickle
import pygame
import sys
from gui import SudokuRenderer  # Importujemy GUI

class NetworkClient:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.renderer = SudokuRenderer()
        self.state = None
        self.player_id = None
        self.running = True
        self.selected = None

    def connect(self, host='127.0.0.1', port=5555):
        try:
            self.client.connect((host, port))
            init_data = pickle.loads(self.client.recv(4096))
            self.player_id = init_data["id"]
            self.state = init_data["state"]
        except ConnectionError:
            print("Błąd połączenia")
            sys.exit(1)

    def listen(self):
        while self.running:
            try:
                data = self.client.recv(4096 * 4)
                if not data: break
                packet = pickle.loads(data)
                self.state = packet["state"]
            except:
                break

    def send_move(self, r, c, val):
        move = {"r": r, "c": c, "val": val}
        self.client.send(pickle.dumps(move))

    def run(self):
        self.connect()
        threading.Thread(target=self.listen, daemon=True).start()

        close_timer_start = None

        while self.running:
            self.renderer.draw_all(self.state, self.player_id, self.selected)

            if self.state and self.state["game_over"]:
                current_time = pygame.time.get_ticks()

                if close_timer_start is None:
                    close_timer_start = current_time
                    print("Gra zakończona. Zamykanie...")

                if current_time - close_timer_start > 5000:
                    self.running = False

            elif self.state and not self.state["game_over"]:
                close_timer_start = None

            # 2. Obsługa zdarzeń
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                if self.state and self.state["game_over"]:
                    continue

                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    col = int(pos[0] // (self.renderer.width / 9))
                    row = int(pos[1] // (self.renderer.width / 9))
                    if row < 9: self.selected = (row, col)

                if event.type == pygame.KEYDOWN and self.selected:
                    key_map = {pygame.K_1: 1, pygame.K_2: 2, pygame.K_3: 3,
                               pygame.K_4: 4, pygame.K_5: 5, pygame.K_6: 6,
                               pygame.K_7: 7, pygame.K_8: 8, pygame.K_9: 9}

                    if event.key in key_map:
                        r, c = self.selected
                        if self.state and self.state["board"][r][c] == 0:
                            self.send_move(r, c, key_map[event.key])
                            self.selected = None

        pygame.quit()
        sys.exit(1)


if __name__ == "__main__":
    NetworkClient().run()