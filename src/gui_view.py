import tkinter as tk
from tkinter import messagebox, simpledialog
from game_controller import TicTacToeController


class TicTacToeGUI:
    def __init__(self, controller):
        self.controller = controller
        self.root = tk.Tk()
        self.root.title("Tic Tac Toe")
        self.user_symbol = "O"
        
        messagebox.showinfo("Simbolos", "Maquina = X \n Usuario = O")
        self.controller.select_user_symbol(self.user_symbol)
            

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
        if self.controller.board[row][col] == 0:  # Verificar si la casilla está vacía
            self.controller.make_user_move(row, col)  # Realizar la jugada del usuario
            self.update_board(self.controller.board)  # Actualizar el tablero después del movimiento del usuario
            self.controller.make_computer_move()  # Realizar el movimiento de la computadora
            self.update_board(self.controller.board)  # Actualizar el tablero después del movimiento de la computadora
        else:
            messagebox.showwarning("Casilla Ocupada", "¡La casilla ya está ocupada! Intenta de nuevo.")

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
