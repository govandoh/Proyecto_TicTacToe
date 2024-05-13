# class Node:
#     def __init__(self, estado, jugador):
#         self.estado = estado
#         self.jugador = jugador
#         self.hijos = []
#         self.valor = None
    
#     def add_hijo(self, hijo):
#         self.hijos.append(hijo)
    
#     def terminal(self):
#         return len(self.hijos) == 0

#     def make_tree(estado,jugador):
#         nodo = Node(estado,jugador)
        
#         if juego_ter



def evaluate(board):
    # Filas
    for row in board:
        if row.count(1) == 3:
            return 10
        elif row.count(-1) == 3:
            return -10
    # Columnas
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col]:
            if board[0][col] == 1:
                return 10
            elif board[0][col] == -1:
                return -10
    # Diagonales
    if board[0][0] == board[1][1] == board[2][2]:
        if board[0][0] == 1:
            return 10
        elif board[0][0] == -1:
            return -10
    if board[0][2] == board[1][1] == board[2][0]:
        if board[0][2] == 1:
            return 10
        elif board[0][2] == -1:
            return -10
    # Empate
    if all(cell != 0 for row in board for cell in row):
        return 0
    # Juego en curso
    return None


def minimax(board, depth, alpha, beta, is_maximizing):
    score = evaluate(board)
    if score is not None:
        return score, []

    if is_maximizing:
        best_score = float('-inf')
        best_path = []
        for i in range(3):
            for j in range(3):
                if board[i][j] == 0:
                    board[i][j] = 1
                    score, path = minimax(board, depth + 1, alpha, beta, False)
                    board[i][j] = 0
                    if score > best_score:  # Verificar si el puntaje no es None
                        best_score = max(score, best_score)
                        best_path = [(i, j)] + path
                        alpha = max(alpha, best_score)
                    if beta <= alpha:
                        break
        return best_score, best_path
    else:
        best_score = float('inf')
        best_path = []
        for i in range(3):
            for j in range(3):
                if board[i][j] == 0:
                    board[i][j] = -1
                    score, path = minimax(board, depth + 1, alpha, beta, True)
                    board[i][j] = 0
                    if score < best_score:  # Verificar si el puntaje no es None
                        best_score = min(score, best_score)
                        best_path = [(i, j)] + path
                        beta = min(beta, best_score)
                    if beta <= alpha:
                            break
        return best_score, best_path
    
def find_best_move(board, path=[]):
    best_score = float('-inf')
    best_move = None
    alpha = float('-inf')
    beta = float('inf')
    best_path = []
    for i in range(3):
        for j in range(3):
            if board[i][j] == 0:
                # Simular el movimiento del jugador X
                board[i][j] = 1
                score, current_path = minimax(board, 0, alpha, beta, False)
                board[i][j] = 0  # Deshacer el movimiento

                # Actualizar la mejor jugada si es necesario
                if score is not None:  # Verificar si el puntaje no es None
                    if score > best_score:
                        best_score = score
                        best_move = (i, j)
                        best_path = path + current_path
    return best_move, best_score, best_path

