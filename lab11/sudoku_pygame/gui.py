import pygame

class SudokuRenderer:
    def __init__(self, width=540, height=600):
        self.width = width
        self.height = height
        self.white = (255, 255, 255)
        self.black = (0, 0, 0)
        self.blue = (0, 0, 255)
        self.red = (255, 0, 0)
        self.green = (0, 200, 0)

        pygame.init()
        self.win = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Sudoku")
        self.font = pygame.font.SysFont('comicsans', 40)
        self.ui_font = pygame.font.SysFont('comicsans', 20)

    def draw_all(self, game_state, player_id, selected):
        self.win.fill(self.white)
        self.draw_grid()
        if game_state:
            self.draw_numbers(game_state["board"])
            self.draw_ui(game_state, player_id)
        if selected:
            self.draw_selection(selected)
        pygame.display.update()

    def draw_grid(self):
        gap = self.width / 9
        for i in range(10):
            thickness = 4 if i % 3 == 0 else 1
            pygame.draw.line(self.win, self.black, (0, i * gap), (self.width, i * gap), thickness)
            pygame.draw.line(self.win, self.black, (i * gap, 0), (i * gap, self.width), thickness)

    def draw_numbers(self, board):
        gap = self.width / 9
        for i in range(len(board)):
            for j in range(len(board)):
                if board[i][j] != 0:
                    text = self.font.render(str(board[i][j]), 1, self.blue)
                    x = j * gap + (gap / 2 - text.get_width() / 2)
                    y = i * gap + (gap / 2 - text.get_height() / 2)
                    self.win.blit(text, (x, y))

    def draw_selection(self, selected):
        row, col = selected
        gap = self.width / 9
        x, y = col * gap, row * gap
        pygame.draw.rect(self.win, self.red, (x, y, gap, gap), 3)

    def draw_ui(self, game_state, player_id):
        score_text = f"Ty: {game_state['scores'][player_id]} | Przeciwnik: {game_state['scores'][1 - player_id]}"
        text_img = self.ui_font.render(score_text, 1, self.black)
        self.win.blit(text_img, (10, self.height - 40))

        if "status_msg" in game_state and game_state["status_msg"]:
            msg = game_state["status_msg"]
            text = self.font.render(msg, 1, self.red)
            x = self.width / 2 - text.get_width() / 2
            y = self.height / 2 - text.get_height() / 2

            pygame.draw.rect(self.win, self.white, (x - 10, y - 10, text.get_width() + 20, text.get_height() + 20))
            self.win.blit(text, (x, y))
            return

        if game_state["game_over"]:
            winner = game_state["winner"]
            if winner == player_id:
                status = "WYGRAŁEŚ!"
                color = self.green
            elif winner == -1:
                status = "REMIS"
                color = self.blue
            else:
                status = "PRZEGRAŁEŚ"
                color = self.red

        elif "status_msg" in game_state and game_state["status_msg"]:
            status = game_state["status_msg"]
            color = self.red
        elif game_state["turn"] == player_id:
            status = "TWOJA TURA"
            color = self.green
        else:
            status = "TURA PRZECIWNIKA"
            color = self.red

        text_img = self.ui_font.render(status, 1 , color)
        x = self.width - text_img.get_width() - 10
        self.win.blit(text_img, (x, self.height - 40))
