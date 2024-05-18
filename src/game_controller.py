from logic_model import evaluate, minimax, find_best_move
import graphviz

import json
import copy

    
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
        self.move_history = {} 
        self.moves = []
        self.weigths = []
        self.game_over = False
        
    def store_game_moves(self, current, moves, weights, best_move, best_score):
        move_history = {
            "current_board": copy.deepcopy(current),  
            "possible_moves": moves,
            "weights": weights,
            "best_move_pc":best_move,
            "best_score_move_pc": best_score
        }
        return move_history
        
        
        
    def print_game_history(self):
        print("Historial de la partida:")
        for history in self.move_history.items():
            #print(f"Turno {turn}:")
            json_data = json.dumps(history, indent=4)
            print(json_data)

        
        
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
        if self.game_over:
            return
        
        if self.board[row][col] != 0:
            print("¡Casilla ocupada! Intenta de nuevo.")
            return
        # Realizar la jugada del usuario
        self.board[row][col] = self.user_symbol
    # Verificar si el juego ha terminado
        self.check_game_status()
        
    def make_computer_move(self):
        if self.game_over:
            return
        
        best_move, best_score, paths = find_best_move(self.board)
        print(paths)
        if best_move:
            self.turn_counter += 1
            if paths:
                print("Ruta de la computadora:")
                #current = self.board()
                temp_board = [row[:] for row in self.board]  # Copia del tablero actual
                for move in paths:
                    temp_board[move[0]][move[0]] = 1 if len(paths) % 2 == 0 else -1  # Simular el movimiento en la copia del tablero
                    print("Fila:", move[0], "Columna:", move[1], "Puntaje:", evaluate(temp_board))  # Evaluar la copia del tablero
                    self.moves.append([move[0],move[1]])
                    self.weigths.append(self.user_symbol)
            else:
                print("La computadora no tomó ninguna ruta alternativa.")           
            
            moves_history = self.store_game_moves(self.board, self.moves.copy(), self.weigths.copy(), best_move, best_score)
            self.move_history[f"{self.turn_counter}"] = moves_history  # Aquí se crea un nuevo registro en el diccionario
            self.print_game_history()  # Modificado aquí
            self.moves.clear()
            self.weigths.clear()
          
            
            self.board[best_move[0]][best_move[1]] = self.computer_symbol
            print("La computadora ha elegido la casilla:", best_move)
            print("Peso de la ruta seleccionada:", best_score)
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
                self.game_over = True
                print("¡La computadora ha ganado!")
            elif score == -10:
                self.game_over = True
                print("¡Has ganado Usuario!")
            elif score == 0:
                self.game_over = True
                print("¡Empate!")
                
            self.print_all_turns()
        else:
            # El juego continúa, actualizar la interfaz
            #print(self.board)
            print("")
            
    def print_all_turns(self):  
        for turn, history in self.move_history.items():
            print(f"Turno {turn}:")
            print("Tablero actual:")
            for row in history["current_board"]:
                print(row)
            print("Movimientos posibles:")
            for move in history["possible_moves"]:
                print(move)
            print("Pesos:")
            print(history["weights"])
            print("Mejor movimiento de la PC:")
            print(history["best_move_pc"])
            print("Mejor puntuación de la PC:")
            print(history["best_score_move_pc"])
            print("\n")
    
    # def imprimir_diccionario_en_graphviz(self,diccionario,dot, parent_node=None):
    #     for key, value in diccionario.items():
    #     # Si la clave es un número, omitir la impresión
    #         if isinstance(key, int):
    #             continue
            
    #         # Si el valor es un diccionario, recorrerlo recursivamente
    #         if isinstance(value, dict):
    #             # Llamar a la función de impresión recursivamente
    #             self.imprimir_diccionario_en_graphviz(dot, value, key)
    #             # Si hay un nodo padre, agregar una conexión desde él al nodo hijo
    #             if parent_node is not None:
    #                 dot.edge(parent_node, key)
    #         else:
    #             # Agregar nodo y conexión para el valor
    #             dot.node(key, str(value))
    #             if parent_node is not None:
    #                 dot.edge(parent_node, key)
        
