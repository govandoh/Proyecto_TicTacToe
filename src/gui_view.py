import tkinter as tk
from tkinter import messagebox
from game_controller import TicTacToeController


class TicTacToeGUI:
    def __init__(self, controller):
        self.controller = controller
        self.root = tk.Tk()
        self.root.title("Tic Tac Toe")

        self.buttons = []
        for i in range(3):
            row = []
            for j in range(3):
                button = tk.Button(self.root, text=" ", font=('Arial', 20), width=5, height=2,
                                   command=lambda r=i, c=j: self.on_button_click(r, c))
                button.grid(row=i, column=j, padx=5, pady=5)
                row.append(button)
            self.buttons.append(row)

    def on_button_click(self, row, col):
        self.controller.make_user_move(row, col)

    def update_board(self, board):
        for i in range(3):
            for j in range(3):
                symbol = board[i][j]
                text = "X" if symbol == 1 else "O" if symbol == -1 else " "
                self.buttons[i][j].config(text=text)

    def show_message(self, message):
        messagebox.showinfo("Tic Tac Toe", message)

    def start(self):
        self.root.mainloop()

if __name__ == "__main__":
    controller = TicTacToeController()
    gui = TicTacToeGUI(controller)
    gui.start()
