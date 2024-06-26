import tkinter as tk
from tkinter import messagebox, ttk, simpledialog
from PIL import Image, ImageTk
from game_controller import TicTacToeController

import os
import pyautogui
import webbrowser

# Contador global para las capturas de pantalla
screenshot_counter_ganadas = 0
screenshot_counter_empatadas = 0

# Inicializa el contador de capturas de pantalla al iniciar el programa
ganadas_directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'partidas_ganadas')
if not os.path.exists(ganadas_directory):
    os.makedirs(ganadas_directory)
screenshot_counter_ganadas = len([f for f in os.listdir(ganadas_directory) if f.startswith('partidaGanada_') and f.endswith('.jpg')])

empatadas_directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'partidas_empatadas')
if not os.path.exists(empatadas_directory):
    os.makedirs(empatadas_directory)
screenshot_counter_empatadas = len([f for f in os.listdir(empatadas_directory) if f.startswith('partidaEmpatada_') and f.endswith('.jpg')])

class TicTacToeGUI:
    def __init__(self, controller, menu_window):
        self.controller = controller
        self.menu_window = menu_window
        self.root = tk.Toplevel()
        self.root.title("Tic Tac Toe")
        self.user_symbol = "O"
        
        self.root.geometry('300x350+800+100')
        
        style = ttk.Style()

        messagebox.showinfo("Simbolos", "Maquina = X \n Usuario = O")
        self.controller.select_user_symbol(self.user_symbol)

        self.buttons = []
        for i in range(3):
            row = []
            for j in range(3):
                button = tk.Button(self.root, text=" ", font=('Arial', 20), width=5, height=2, background="#2596be",
                                   command=lambda r=i, c=j: self.on_button_click(r, c))
                button.grid(row=i, column=j, padx=5, pady=5)
                row.append(button)
            self.buttons.append(row)
        
        # Agregar el botón "Salir" al tablero
        self.quit_button = ttk.Button(self.root, text="Salir", command=self.quit_game, style="Rounded.TButton")
        self.quit_button.grid(row=3, column=1, columnspan=3, pady=10, padx=20)
        
        style.configure("Rounded.TButton", padding=8, relief="flat", background="#5454d4", foreground="white", font=('Arial', 12, 'bold'))
        
        self.root.grab_set()
        self.root.focus_force()
        self.root.protocol("WM_DELETE_WINDOW", self.quit_game)

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
    
    def take_screenshot(self, empate=False):
        global screenshot_counter_ganadas, screenshot_counter_empatadas  # Referencia a los contadores globales
        folder_name = 'partidas_empatadas' if empate else 'partidas_ganadas'
        screenshots_directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), folder_name)
        
        # Crear la carpeta si no existe
        if not os.path.exists(screenshots_directory):
            os.makedirs(screenshots_directory)
        
        if empate:
            screenshot_path = os.path.join(screenshots_directory, f'partidaEmpatada_{screenshot_counter_empatadas}.jpg')
            screenshot_counter_empatadas += 1
        else:
            screenshot_path = os.path.join(screenshots_directory, f'partidaGanada_{screenshot_counter_ganadas}.jpg')
            screenshot_counter_ganadas += 1

        x = self.root.winfo_rootx()
        y = self.root.winfo_rooty()
        w = self.root.winfo_width()
        h = self.root.winfo_height()

        screenshot = pyautogui.screenshot(region=(x, y, w, h))       
        screenshot = screenshot.convert('RGB')
        screenshot.save(screenshot_path)

    def update_board(self, board):
        for i in range(3):
            for j in range(3):
                symbol = board[i][j]
                text = "X" if symbol == 1 else "O" if symbol == -1 else " "
                self.buttons[i][j].config(text=text)

    def show_message(self, message):
        messagebox.showinfo("Resultado Partida", message)

    def start(self):
        self.root.mainloop()

    def check_game_status(self):
        # Método para verificar si el juego ha terminado
        score = self.controller.check_game_status()
        if score is not None:
            if score == 10:
                self.root.after(1000, self.take_screenshot)
                return self.show_message("¡La computadora ha ganado!")
            elif score == -10:
                return self.show_message("¡Has ganado Usuario!")
            elif score == 0:
                self.root.after(1000, lambda: self.take_screenshot(empate=True))
                return self.show_message("¡Empate!")

    def quit_game(self):
        self.root.destroy()  # Cerrar la ventana del juego
        self.menu_window.deiconify()

class MainMenu:
    def __init__(self, root):
        self.root = root
        self.root.title("Menú Principal")
        self.root.configure(bg="#0E4D92")  
        self.create_menu()
        
    def create_menu(self):
        style = ttk.Style()
        style.theme_use('clam')

        self.background_image = Image.open("background.jpg")
        self.background_photo = ImageTk.PhotoImage(self.background_image)
        self.background_label = tk.Label(self.root, image=self.background_photo)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)

        self.menu_frame = ttk.Frame(self.root, padding="20", style="Dark.TFrame")  
        self.menu_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        self.new_game_button = ttk.Button(self.menu_frame, text="Nueva Partida", command=self.start_game, style="Rounded.TButton")
        self.new_game_button.pack(pady=10)

        self.winning_history_button = ttk.Button(self.menu_frame, text="Ver Partidas Ganadas", command=self.show_winning_history, style="Rounded.TButton")
        self.winning_history_button.pack(pady=10)

        self.draw_history_button = ttk.Button(self.menu_frame, text="Ver Partidas Empatadas", command=self.show_draw_history, style="Rounded.TButton")
        self.draw_history_button.pack(pady=10)
        
        self.history_learning = ttk.Button(self.menu_frame, text="Historial de Aprendizaje", command=self.show_history_learnings, style="Rounded.TButton")
        self.history_learning.pack(pady=10)

        self.team_members_button = ttk.Button(self.menu_frame, text="Integrantes del Proyecto", command=self.show_team_members, style="Rounded.TButton")
        self.team_members_button.pack(pady=10)

        self.quit_button = ttk.Button(self.menu_frame, text="Salir", command=self.root.destroy, style="Rounded.TButton")
        self.quit_button.pack(pady=10)

        style.configure("Rounded.TButton", padding=10, relief="flat", background="#5454d4", foreground="white", font=('Arial', 12, 'bold'))
        style.configure("Dark.TFrame", background="#21003e") 
        
        style.map("Rounded.TButton",
            background=[('active', '#3c3c9a')],
            foreground=[('active', 'white')])

        width = self.background_image.width
        height = self.background_image.height

        self.root.geometry(f"{width}x{height}")

    def start_game(self):
        choice = messagebox.askyesno("Nueva Partida", "¿Deseas iniciar una nueva partida?")
        if choice:
            self.root.withdraw()  
            controller = TicTacToeController()  
            gui = TicTacToeGUI(controller, self.root)  
            gui.start()  

    def show_winning_history(self):
        screenshots_directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'partidas_ganadas')
        screenshots = [f for f in os.listdir(screenshots_directory) if f.startswith('partidaGanada_') and f.endswith('.jpg')]
        if not screenshots:
           messagebox.showinfo("Historial de Partidas Ganadas", "No hay capturas de pantalla registradas.")
        else:
            self.show_screenshots(screenshots, screenshots_directory, "Ganada")
    
    def show_draw_history(self):
        screenshots_directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'partidas_empatadas')
        screenshots = [f for f in os.listdir(screenshots_directory) if f.startswith('partidaEmpatada_') and f.endswith('.jpg')]
        if not screenshots:
           messagebox.showinfo("Historial de Partidas Empatadas", "No hay capturas de pantalla registradas.")
        else:
            self.show_screenshots(screenshots, screenshots_directory, "Empatada")
    
    def show_screenshots(self, screenshots, path, tipo):
        screenshots = sorted(screenshots, key=lambda x: int(x.split('_')[1].split('.')[0]), reverse=False)
        screenshot_window = tk.Toplevel(self.root)
        screenshot_window.title(f"Historial de Partidas {tipo}s")
        screenshot_window.geometry('500x750+700+150')  # Aumenta el ancho para acomodar la scrollbar

        canvas = tk.Canvas(screenshot_window)
        scrollbar = ttk.Scrollbar(screenshot_window, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        for idx, screenshot in enumerate(screenshots):
            img = Image.open(os.path.join(path, screenshot))
            img = img.resize((200, 200), Image.LANCZOS)
            photo = ImageTk.PhotoImage(img)
            label = tk.Label(scrollable_frame, image=photo)
            label.image = photo  # Keep a reference to avoid garbage collection
            label_text = tk.Label(scrollable_frame, text=f"Partida {tipo} No.{idx + 1}", font=("Arial", 12))
            label.grid(row=idx, column=0, padx=5, pady=5)
            label_text.grid(row=idx, column=1, padx=5, pady=5)

    def show_history_learnings(self):
        top = tk.Toplevel(self.root)
        top.title("Historial Aprendizajes")
        top.geometry('500x500+700+150')
        self.directory = 'resultados'
        
        tree = ttk.Treeview(top, columns=("Filename", "Action"), show="headings")
        tree.heading("Filename", text="Nombre del Archivo")
        tree.heading("Action", text="Double click")
        tree.grid(row=1, column=1, padx=25, pady=20, sticky='nsew')
        
        tree.column("Filename", width=350)
        tree.column("Action", width=100, anchor="center")
        
        top.grid_rowconfigure(1, weight=1)

        def load_files(directory):
            for filename in os.listdir(directory):
                if filename.endswith(".pdf"):
                    filepath = os.path.join(directory, filename)
                    tree.insert("", "end", values=(filename, "Open"), tags=(filepath,))
                    
        load_files(self.directory)

        def on_tree_select(event):
            item = tree.selection()[0]
            filepath = tree.item(item, "tags")[0]
            self.open_pdf(filepath)
        
        tree.bind("<Double-1>", on_tree_select)
    
    def open_pdf(self, file_path):
        webbrowser.open(file_path)

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
    root.maxsize(1920, 1080)
    MainMenu(root)
    root.mainloop()

if __name__ == "__main__":
    start_menu()
