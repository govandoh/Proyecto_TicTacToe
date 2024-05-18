from tkinter import Tk
from gui_view import TicTacToeGUI
from game_controller import TicTacToeController

def main():
    controller = TicTacToeController()
    gui = TicTacToeGUI(controller)
    gui.start()

if __name__ == "__main__":
    main()
