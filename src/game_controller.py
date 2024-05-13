from logic_model import evaluate, minimax, find_best_move

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
        self.min_paths = []
        
        
    def select_user_symbol(self, symbol):
        symbol = symbol.upper()
        if symbol.upper() == 'X':
            self.user_symbol = -1
            self.computer_symbol = 1
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
        
    def make_computer_move(self):
        best_move, best_score, best_path = find_best_move(self.board)
        if best_move:
            self.turn_counter += 1
            if best_path:
                print("Ruta de la computadora:")
                temp_board = [row[:] for row in self.board]  # Copia del tablero actual
                for move in best_path:
                    temp_board[move[0]][move[0]] = 1 if len(best_path) % 2 == 0 else -1  # Simular el movimiento en la copia del tablero
                    print("Fila:", move[0], "Columna:", move[1], "Puntaje:", evaluate(temp_board))  # Evaluar la copia del tablero
                    self.min_paths.append(move)
            else:
                print("La computadora no tomó ninguna ruta alternativa.")
            self.board[best_move[0]][best_move[1]] = self.computer_symbol
            print("La computadora ha elegido la casilla:", best_move)
            print("Peso de la ruta seleccionada:", best_score)
            print(self.min_paths)
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
                print("¡Has ganado Usuario!")
            elif score == 0:
                print("¡Empate!")
                
        else:
            # El juego continúa, actualizar la interfaz
            #print(self.board)
            print("")
            