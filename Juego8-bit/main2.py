import random

# Inicializar el tablero vacío (4x4)
board = [['' for _ in range(4)] for _ in range(4)]

# Piezas disponibles para el jugador y la máquina
user_pieces = ['A', 'B', 'C', 'D']
machine_pieces = ['a', 'b', 'c', 'd']

# Función para mostrar el tablero
def print_board(board):
    for row in board:
        print(' '.join([cell if cell else '.' for cell in row]))

# Función para verificar si la colocación es válida
def is_valid_move(board, row, col, piece):
    # Verifica si el lugar está vacío
    if board[row][col] != '':
        return False
    
    # Verifica si la pieza ya está en la misma fila, columna o cuadrante
    for i in range(4):
        if board[row][i].lower() == piece.lower() or board[i][col].lower() == piece.lower():
            return False
    
    # Verificar cuadrante
    start_row, start_col = 2 * (row // 2), 2 * (col // 2)
    for i in range(2):
        for j in range(2):
            if board[start_row + i][start_col + j].lower() == piece.lower():
                return False
    
    return True

# Función para verificar si hay un ganador en un cuadrante
def check_quadrant_winner(board, start_row, start_col):
    pieces = set()
    for i in range(2):
        for j in range(2):
            piece = board[start_row + i][start_col + j]
            if piece == '':
                return False
            pieces.add(piece.lower())
    return len(pieces) == 4

# Función para verificar si hay un ganador general
def check_winner(board):
    # Verificar filas y columnas
    for i in range(4):
        if len(set(board[i])) == 4 and '' not in board[i]:
            return True
        if len(set([board[j][i] for j in range(4)])) == 4 and '' not in [board[j][i] for j in range(4)]:
            return True

    # Verificar cada cuadrante
    for start_row in range(0, 4, 2):
        for start_col in range(0, 4, 2):
            if check_quadrant_winner(board, start_row, start_col):
                return True
    
    return False

# Función para turno del jugador
def player_turn():
    while True:
        print_board(board)
        row = int(input("Ingresa la fila (0-3): "))
        col = int(input("Ingresa la columna (0-3): "))
        piece = input("Elige una pieza (A, B, C, D): ").upper()
        
        if piece in user_pieces and is_valid_move(board, row, col, piece):
            board[row][col] = piece
            user_pieces.remove(piece)
            break
        else:
            print("Movimiento no válido, intenta nuevamente.")

# Función para turno de la máquina
def machine_turn():
    print("Turno de la máquina...")
    while True:
        row = random.randint(0, 3)
        col = random.randint(0, 3)
        piece = random.choice(machine_pieces)
        
        if is_valid_move(board, row, col, piece):
            board[row][col] = piece
            machine_pieces.remove(piece)
            break

# Juego principal
def play_game():
    while True:
        player_turn()
        if check_winner(board):
            print("¡Felicidades! ¡Has ganado!")
            break
        
        machine_turn()
        if check_winner(board):
            print("La máquina ha ganado.")
            break
        
        if not user_pieces and not machine_pieces:
            print("Empate. No quedan más movimientos.")
            break

play_game()
