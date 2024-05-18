import tkinter as tk
from tkinter import messagebox, ttk, simpledialog
from PIL import Image, ImageTk
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
        
        # Agregar el botón "Salir" al tablero
        self.quit_button = ttk.Button(self.root, text="Salir", command=self.quit_game, style="Rounded.TButton")
        self.quit_button.grid(row=3, column=1, columnspan=3, pady=10)

    def on_button_click(self, row, col):
        if self.controller.board[row][col] == 0:  
            self.controller.make_user_move(row, col)  
            self.update_board(self.controller.board)  
            self.controller.make_computer_move()  
            self.update_board(self.controller.board)
            result = self.check_game_status()  # Verificar el estado del juego después de cada movimiento
            if result:
                self.show_message(result)

        else:
            messagebox.showwarning("Casilla Ocupada", "¡La casilla ya está ocupada! Intenta de nuevo.")

    def update_board(self, board):
        for i in range(3):
            for j in range(3):
                symbol = board[i][j]
                text = "X" if symbol == 1 else "O" if symbol == -1 else " "
                self.buttons[i][j].config(text=text)

    def show_message(self, message):
        messagebox.showinfo("Tic Tac Toe - Resultado", message)

    def start(self):
        self.root.mainloop()

    def check_game_status(self):
    # Método para verificar si el juego ha terminado
        score = self.controller.check_game_status()
        if score is not None:
           if score == 10:
             self.show_message("¡La computadora ha ganado!")
        elif score == -10:
            self.show_message("¡Has ganado Usuario!")
        elif score == 0:
            self.show_message("¡Empate!")

    # Función para salir del juego y regresar al menú principal
    def quit_game(self):
        self.root.destroy()  # Cerrar la ventana del juego

class MainMenu:
    def __init__(self, root):
        self.root = root
        self.root.title("Menú Principal")
        self.root.configure(bg="#0E4D92")  
        self.create_menu()
        
    def create_menu(self):
        style = ttk.Style()
        style.theme_use('clam')

        button_color = "#2980B9"

        self.background_image = Image.open("background.jpg")
        self.background_photo = ImageTk.PhotoImage(self.background_image)
        self.background_label = tk.Label(self.root, image=self.background_photo)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)

        self.menu_frame = ttk.Frame(self.root, padding="20", style="Dark.TFrame")  
        self.menu_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        self.new_game_button = ttk.Button(self.menu_frame, text="Nueva Partida", command=self.start_game, style="Rounded.TButton")
        self.new_game_button.pack(pady=10)

        self.winning_history_button = ttk.Button(self.menu_frame, text="Historial de Partidas Ganadas", command=self.show_winning_history, style="Rounded.TButton")
        self.winning_history_button.pack(pady=10)

        self.losing_history_button = ttk.Button(self.menu_frame, text="Historial de Partidas Perdidas", command=self.show_losing_history, style="Rounded.TButton")
        self.losing_history_button.pack(pady=10)

        self.team_members_button = ttk.Button(self.menu_frame, text="Integrantes del Proyecto", command=self.show_team_members, style="Rounded.TButton")
        self.team_members_button.pack(pady=10)

        self.quit_button = ttk.Button(self.menu_frame, text="Salir", command=self.root.destroy, style="Rounded.TButton")
        self.quit_button.pack(pady=10)

        style.configure("Rounded.TButton", padding=10, relief="flat", background=button_color, foreground="white", font=('Arial', 12, 'bold'))
        style.configure("Dark.TFrame", background="#0E4D92")  

        width = self.background_image.width
        height = self.background_image.height

        self.root.geometry(f"{width}x{height}")

    def start_game(self):
        choice = messagebox.askyesno("Nueva Partida", "¿Deseas iniciar una nueva partida?")
        if choice:
            self.root.withdraw()  
            controller = TicTacToeController()  
            gui = TicTacToeGUI(controller)  
            gui.start()  

    def show_winning_history(self):
        try:
            with open("historial_ganadas.txt", "r") as file:
                messagebox.showinfo("Historial de Partidas Ganadas", file.read())
        except FileNotFoundError:
            messagebox.showinfo("Historial de Partidas Ganadas", "No hay partidas ganadas registradas.")

    def show_losing_history(self):
        try:
            with open("historial_perdidas.txt", "r") as file:
                messagebox.showinfo("Historial de Partidas Perdidas", file.read())
        except FileNotFoundError:
            messagebox.showinfo("Historial de Partidas Perdidas", "No hay partidas perdidas registradas.")

    def show_team_members(self):
        team_members = """
        Integrantes del Proyecto:
        Nombre: Gerardo Ovando
        Nombre: Nery Colorado
        Nombre: Javier Pirir
        Nombre: Jaqueline 
        """
        messagebox.showinfo("Integrantes del Proyecto", team_members)


def start_menu():
    root = tk.Tk()
    MainMenu(root)
    root.mainloop()

if __name__ == "__main__":
    start_menu()
