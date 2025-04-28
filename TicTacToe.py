import tkinter as tk
from tkinter import messagebox
import random

class TicTacToe:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Tic Tac Toe - Player vs Computer")
        self.buttons = [[None for _ in range(3)] for _ in range(3)]
        self.computer_first_move = True  # Track if computer is making its first move

        self.create_buttons()

        self.reset_button = tk.Button(self.window, text="Reset", font=('Arial', 20), command=self.reset_board)
        self.reset_button.grid(row=3, column=0, columnspan=3, sticky="nsew")

        self.start_game()
        self.window.mainloop()

    def start_game(self):
        self.current_player = random.choice(["Player", "Computer"])
        if self.current_player == "Computer":
            self.window.after(500, self.computer_move)

    def create_buttons(self):
        for row in range(3):
            for col in range(3):
                button = tk.Button(
                    self.window, text="", font=('Arial', 40), width=5, height=2,
                    command=lambda r=row, c=col: self.player_move(r, c),
                    bg="white"
                )
                button.grid(row=row, column=col)
                self.buttons[row][col] = button

    def player_move(self, row, col):
        if self.current_player == "Player" and self.buttons[row][col]["text"] == "" and not self.check_winner():
            self.buttons[row][col]["text"] = "X"
            self.buttons[row][col]["fg"] = "red"
            self.buttons[row][col]["bg"] = "#FFF8DC"  # Cornsilk for X
            if self.check_winner():
                messagebox.showinfo("Game Over", "You win!")
                self.reset_board()
            elif self.is_draw():
                messagebox.showinfo("Game Over", "It's a Draw!")
                self.reset_board()
            else:
                self.current_player = "Computer"
                self.window.after(500, self.computer_move)

    def computer_move(self):
        if self.computer_first_move:
            # Random move for the very first computer turn
            available_moves = [(r, c) for r in range(3) for c in range(3) if self.buttons[r][c]["text"] == ""]
            if available_moves:
                row, col = random.choice(available_moves)
                self.buttons[row][col]["text"] = "O"
                self.buttons[row][col]["fg"] = "green"
                self.buttons[row][col]["bg"] = "#F0F8FF"  # AliceBlue for O
                self.computer_first_move = False
                if self.check_winner():
                    messagebox.showinfo("Game Over", "Computer wins!")
                    self.reset_board()
                elif self.is_draw():
                    messagebox.showinfo("Game Over", "It's a Draw!")
                    self.reset_board()
                else:
                    self.current_player = "Player"
            return

        # Normal smart move (Minimax) after first move
        best_score = -float('inf')
        best_move = None

        for row in range(3):
            for col in range(3):
                if self.buttons[row][col]["text"] == "":
                    self.buttons[row][col]["text"] = "O"
                    score = self.minimax(False)
                    self.buttons[row][col]["text"] = ""
                    if score > best_score:
                        best_score = score
                        best_move = (row, col)

        if best_move:
            row, col = best_move
            self.buttons[row][col]["text"] = "O"
            self.buttons[row][col]["fg"] = "green"
            self.buttons[row][col]["bg"] = "#F0F8FF"  # AliceBlue for O
            if self.check_winner():
                messagebox.showinfo("Game Over", "Computer wins!")
                self.reset_board()
            elif self.is_draw():
                messagebox.showinfo("Game Over", "It's a Draw!")
                self.reset_board()
            else:
                self.current_player = "Player"

    def minimax(self, is_maximizing):
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
                        score = self.minimax(False)
                        self.buttons[row][col]["text"] = ""
                        best_score = max(score, best_score)
            return best_score
        else:
            best_score = float('inf')
            for row in range(3):
                for col in range(3):
                    if self.buttons[row][col]["text"] == "":
                        self.buttons[row][col]["text"] = "X"
                        score = self.minimax(True)
                        self.buttons[row][col]["text"] = ""
                        best_score = min(score, best_score)
            return best_score

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

    def reset_board(self):
        for row in range(3):
            for col in range(3):
                self.buttons[row][col]["text"] = ""
                self.buttons[row][col]["fg"] = "black"
                self.buttons[row][col]["bg"] = "white"
        self.computer_first_move = True
        self.start_game()

if __name__ == "__main__":
    TicTacToe()
