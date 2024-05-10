from src.logic_model import evaluate, minimax, find_best_move
from src.gui_view import TicTacToeGUI

class TicTacToeController:
    def __init__(self):
        self.board = [
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0]
        ]
        self.turn_counter = 0
        self.user_symbol = None
        self.computer_symbol = None
        self.gui = TicTacToeGUI(self)
        
        
        
    def select_user_symbol(self, symbol):
        if symbol.upper() == 'X':
            self.user_symbol = 1
            self.computer_symbol = -1
        elif symbol.upper() == 'O':
            self.user_symbol = -1
            self.computer_symbol = 1
        else:
            print("Invalid symbol")
            return False
        return True
    
    def make_user_move(self, row, col):
        if self.board[row][col] != 0:
            print("¡Casilla ocupada! Intenta de nuevo.")
            return
        # Realizar la jugada del usuario
        self.board[row][col] = self.user_symbol
        self.turn_counter += 1
        # Verificar si el juego ha terminado
        self.check_game_status()
        # Turno de la computadora
        self.make_computer_move()
        
    def make_computer_move(self):
        best_move = find_best_move(self.board)
        if best_move:
            self.board[best_move[0]][best_move[1]] = self.computer_symbol
            self.turn_counter += 1
            # Verificar si el juego ha terminado
            self.check_game_status()
        else:
            # No hay movimientos posibles, se considera empate
            self.check_game_status()
    
    def check_game_status(self):
        # Método para verificar si el juego ha terminado
        score = evaluate(self.board)
        if score is not None:
            if score == 10:
                print("¡La computadora ha ganado!")
            elif score == -10:
                print("¡Has ganado!")
            else:
                print("¡Empate!")
        else:
            # El juego continúa, actualizar la interfaz
            print(self.board)