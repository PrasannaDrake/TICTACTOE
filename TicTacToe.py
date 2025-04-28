import tkinter as tk
import random

class TicTacToe:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Tic Tac Toe - Player vs Computer")
        self.buttons = [[None for _ in range(3)] for _ in range(3)]
        self.create_buttons()

        self.reset_button = tk.Button(self.window, text="Reset", font=('Arial', 20), command=self.reset_board)
        self.reset_button.grid(row=3, column=0, columnspan=3, sticky="nsew")

        self.start_new_game()

        self.window.mainloop()

    def create_buttons(self):
        for row in range(3):
            for col in range(3):
                button = tk.Button(
                    self.window, text="", font=('Arial', 40), width=5, height=2,
                    command=lambda r=row, c=col: self.player_move(r, c)
                )
                button.grid(row=row, column=col)
                self.buttons[row][col] = button

    def start_new_game(self):
        self.current_player = random.choice(["X", "O"])
        self.computer_first_move_done = False
        if self.current_player == "O":
            self.window.after(500, self.computer_move)

    def player_move(self, row, col):
        if self.buttons[row][col]["text"] == "" and not self.check_winner():
            self.make_move(row, col, "X")
            if self.check_winner():
                self.show_game_over_popup("You win!")
            elif self.is_draw():
                self.show_game_over_popup("It's a Draw!")
            else:
                self.current_player = "O"
                self.window.after(500, self.computer_move)

    def computer_move(self):
        if not self.computer_first_move_done:
            available_moves = [(r, c) for r in range(3) for c in range(3) if self.buttons[r][c]["text"] == ""]
            if available_moves:
                row, col = random.choice(available_moves)
                self.make_move(row, col, "O")
                self.computer_first_move_done = True
                if self.check_winner():
                    self.show_game_over_popup("Computer wins!")
                elif self.is_draw():
                    self.show_game_over_popup("It's a Draw!")
                else:
                    self.current_player = "X"
            return

        move = self.find_best_move_minimax()

        if move:
            row, col = move
            self.make_move(row, col, "O")
            if self.check_winner():
                self.show_game_over_popup("Computer wins!")
            elif self.is_draw():
                self.show_game_over_popup("It's a Draw!")
            else:
                self.current_player = "X"

    def find_best_move_minimax(self):
        best_score = -float('inf')
        best_move = None

        for row in range(3):
            for col in range(3):
                if self.buttons[row][col]["text"] == "":
                    self.buttons[row][col]["text"] = "O"
                    score = self.minimax(0, False)
                    self.buttons[row][col]["text"] = ""
                    if score > best_score:
                        best_score = score
                        best_move = (row, col)

        return best_move

    def minimax(self, depth, is_maximizing):
        if self.check_specific_winner("O"):
            return 1
        if self.check_specific_winner("X"):
            return -1
        if self.is_draw():
            return 0

        if is_maximizing:
            best_score = -float('inf')
            for row in range(3):
                for col in range(3):
                    if self.buttons[row][col]["text"] == "":
                        self.buttons[row][col]["text"] = "O"
                        score = self.minimax(depth + 1, False)
                        self.buttons[row][col]["text"] = ""
                        best_score = max(score, best_score)
            return best_score
        else:
            best_score = float('inf')
            for row in range(3):
                for col in range(3):
                    if self.buttons[row][col]["text"] == "":
                        self.buttons[row][col]["text"] = "X"
                        score = self.minimax(depth + 1, True)
                        self.buttons[row][col]["text"] = ""
                        best_score = min(score, best_score)
            return best_score

    def make_move(self, row, col, player):
        self.buttons[row][col]["text"] = player
        if player == "X":
            self.buttons[row][col]["fg"] = "red"
            self.buttons[row][col]["bg"] = "#FFF8DC"  # Cornsilk
        else:
            self.buttons[row][col]["fg"] = "green"
            self.buttons[row][col]["bg"] = "#F0F8FF"  # AliceBlue

    def check_winner(self):
        for i in range(3):
            if (self.buttons[i][0]["text"] == self.buttons[i][1]["text"] == self.buttons[i][2]["text"] != "") or \
               (self.buttons[0][i]["text"] == self.buttons[1][i]["text"] == self.buttons[2][i]["text"] != ""):
                return True

        if (self.buttons[0][0]["text"] == self.buttons[1][1]["text"] == self.buttons[2][2]["text"] != "") or \
           (self.buttons[0][2]["text"] == self.buttons[1][1]["text"] == self.buttons[2][0]["text"] != ""):
            return True

        return False

    def check_specific_winner(self, player):
        for i in range(3):
            if (self.buttons[i][0]["text"] == self.buttons[i][1]["text"] == self.buttons[i][2]["text"] == player) or \
               (self.buttons[0][i]["text"] == self.buttons[1][i]["text"] == self.buttons[2][i]["text"] == player):
                return True

        if (self.buttons[0][0]["text"] == self.buttons[1][1]["text"] == self.buttons[2][2]["text"] == player) or \
           (self.buttons[0][2]["text"] == self.buttons[1][1]["text"] == self.buttons[2][0]["text"] == player):
            return True

        return False

    def is_draw(self):
        for row in range(3):
            for col in range(3):
                if self.buttons[row][col]["text"] == "":
                    return False
        return True

    def show_game_over_popup(self, message):
        popup = tk.Toplevel()
        popup.title("Game Over")
        popup.geometry("300x150")
        popup.resizable(False, False)

        popup.update_idletasks()
        width = 300
        height = 150
        x = (popup.winfo_screenwidth() // 2) - (width // 2)
        y = (popup.winfo_screenheight() // 2) - (height // 2)
        popup.geometry(f"{width}x{height}+{x}+{y}")

        label = tk.Label(popup, text=message, font=('Arial', 16))
        label.pack(pady=20)

        new_game_button = tk.Button(popup, text="New Game", font=('Arial', 14), command=lambda: [self.reset_board(), popup.destroy()])
        new_game_button.pack()

        popup.grab_set()

    def reset_board(self):
        for row in range(3):
            for col in range(3):
                self.buttons[row][col]["text"] = ""
                self.buttons[row][col]["fg"] = "black"
                self.buttons[row][col]["bg"] = "SystemButtonFace"
        self.start_new_game()

if __name__ == "__main__":
    TicTacToe()
