from logic_model import evaluate, minimax, find_best_move
from graphviz import Digraph

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, landscape
from PIL import Image


import copy
import json
import os, glob
import datetime

    
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
        self.date_format = datetime.datetime.now()
        self.game_date = self.date_format.strftime("%d-%m-%Y-%H-%M-%S")
        self.pdf = f"resultados/historial_movimientos_aprendizaje_{self.game_date}.pdf"
        
        
        
    def store_game_moves(self, current, moves, weights, best_move, best_score):
        move_history = {
            "current_board": copy.deepcopy(current),  
            "moves_to_lose": moves,
            "weights_to_lose": weights,
            "best_move_pc":best_move,
            "best_score_move_pc": best_score
        }
        return move_history        
        
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
        if best_move:
            self.turn_counter += 1
            if paths:
                temp_board = [row[:] for row in self.board]  # Copia del tablero actual
                for move in paths:
                    temp_board[move[0]][move[0]] = 1 if len(paths) % 2 == 0 else -1  # Simular el movimiento en la copia del tablero
                    self.moves.append([move[0],move[1]])
                    self.weigths.append(self.user_symbol)
            else:
                print("La computadora no tomó ninguna ruta alternativa, toma el mejor score")           

            #Ejecuta y guarda el mejor movimiento
            moves_history = self.store_game_moves(self.board, self.moves.copy(), self.weigths.copy(), best_move, best_score)
            self.move_history[f"{self.turn_counter}"] = moves_history  # Aquí se crea un nuevo registro en el diccionario
            
            #Inserto despues para guardar el tablero desencadenante
            self.board[best_move[0]][best_move[1]] = self.computer_symbol
            self.print_game_history()
            #Limpio listas
            self.moves.clear()
            self.weigths.clear()
            # Verificar si el juego ha terminado
            self.check_game_status()
        else:
            print("")


    def print_game_history(self):
        print("Historial de la partida:")
        for history in self.move_history.items():
            #print(f"Turno {turn}:")
            json_data = json.dumps(history, indent=4)
            print(json_data)
    
    def check_game_status(self):
        # Método para verificar si el juego ha terminado
        score = evaluate(self.board)
        if score is not None:
            if score == 10:
                self.turn_counter = 4
                moves_history = self.store_game_moves(self.board, self.moves.copy(), self.weigths.copy(), None, None)
                self.move_history[f"{self.turn_counter}"] = moves_history  # Aquí se crea un nuevo registro en el diccionario
                self.game_over = True
                self.create_report()
                self.delete_outputs()
            elif score == -10:
                self.game_over = True
                self.create_report()
                self.delete_outputs()
            elif score == 0:
                print("¡Empate!")
                self.turn_counter = 5
                moves_history = self.store_game_moves(self.board, self.moves.copy(), self.weigths.copy(), None, None)
                self.move_history[f"{self.turn_counter}"] = moves_history  # Aquí se crea un nuevo registro en el diccionario
                #if score == 0:
                self.game_over = True
                self.create_report()
                self.delete_outputs()
            
        else:
            # El juego continúa, actualizar la interfaz
            print("")
        return score
            
    def create_report(self):
        self.imprimir_diccionario_en_graphviz(self.move_history)
        self.combinar_imagenes_en_pdf()
        
    
    def imprimir_diccionario_en_graphviz(self, diccionario, output_dir='output'):
    # Crear el directorio de salida si no existe
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # Contador para los archivos de imagen
        img_count = 0

        # Recorrer el diccionario
        for key, value in diccionario.items():
            # Crear un nuevo objeto Digraph para cada sub-diccionario
            dot = Digraph()
            
            # Si el valor es un diccionario, recorrerlo también
            if isinstance(value, dict):
                for k, v in value.items():
                    # Si el valor interno es un diccionario, recorrerlo también
                    if isinstance(v, dict):
                        for vk, vv in v.items():
                            # Agregar nodo para la clave interna del valor interno y su valor
                            dot.node(str(vk), f"{vk}: {vv}")
                            # Agregar un borde desde la clave interna hasta la clave interna del valor interno
                            dot.edge(str(k), str(vk))
                    else:
                        # Agregar nodo para la clave interna y su valor
                        dot.node(str(k), f"{k}: {v}")
                        # Agregar un borde desde la clave hasta la clave interna
                        dot.edge(str(key), str(k))
            else:
                # Agregar nodo para la clave y su valor
                dot.node(str(key), f"{key}: {value}")
            
            dot.attr(size='10,5')  # Puedes ajustar el tamaño según sea necesario
            dot.attr(rankdir='LR')  # Configurar el gráfico para que sea horizontal

            # Guardar el gráfico en un archivo de imagen
            img_count += 1
            file_path = os.path.join(output_dir, f'Detalles_Movimiento_{img_count}')
            dot.render(file_path, format='png', cleanup=True)
    
    def combinar_imagenes_en_pdf(self, output_dir='output'):
    # Crear un documento PDF
        c = canvas.Canvas(self.pdf, pagesize=letter)

        # Obtener la lista de archivos de imagen en el directorio de salida
        img_files = [f for f in os.listdir(output_dir) if f.endswith('.png')]
        img_files.sort()  # Asegurar que los archivos estén en el orden correcto

        for img_file in img_files:
            # Abrir la imagen
            img_path = os.path.join(output_dir, img_file)
            img = Image.open(img_path)
            
            # Ajustar la imagen al tamaño de la página
            width, height = letter
            img_width, img_height = img.size
            aspect = img_height / float(img_width)
            new_width = width
            new_height = aspect * new_width
            if new_height > height:
                new_height = height
                new_width = new_height / aspect
            
            # Dibujar la imagen en el PDF
            c.drawImage(img_path, 0, height - new_height, width=new_width, height=new_height-50)
            
            title = img_file.split('.')[0]
            c.setFont("Helvetica-Bold", 15)
            c.drawString(50, height - 20, title)
            c.showPage()  # Añadir una nueva página para la próxima imagen

        c.save()
            
    def delete_outputs(self, output_dir='output'):
        img_files = [f for f in os.listdir(output_dir) if f.endswith('.png')]
        img_files.sort()  # Asegurar que los archivos estén en el orden correcto
        
        for img_file in img_files:
            # Abrir la imagen
            img_path = os.path.join(output_dir, img_file)
            os.remove(img_path)
        