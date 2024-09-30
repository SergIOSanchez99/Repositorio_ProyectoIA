import pygame
import numpy as np
import random

# Inicializar Pygame
pygame.init()

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GRAY = (200, 200, 200)

# Tamaños de pantalla y celdas
SCREEN_SIZE = 400
CELL_SIZE = SCREEN_SIZE // 4
MENU_HEIGHT = 100

# Crear ventana
screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE + MENU_HEIGHT))
pygame.display.set_caption("Quantik")

# Piezas de los jugadores
player_pieces = {
    0: {'A': 2, 'B': 2, 'C': 2, 'D': 2},
    1: {'A': 2, 'B': 2, 'C': 2, 'D': 2}
}

# Tablero de 4x4
EMPTY = None
board = [[EMPTY for _ in range(4)] for _ in range(4)]

# Fuente para texto
font = pygame.font.Font(None, 36)

# Piezas disponibles
piece_buttons = {}
piece_colors = {'A': RED, 'B': GREEN, 'C': BLUE, 'D': YELLOW}


def draw_board():
    """Dibuja el tablero y las piezas."""
    screen.fill(WHITE)
    
    # Dibujar líneas del tablero
    for i in range(5):
        pygame.draw.line(screen, BLACK, (0, i * CELL_SIZE), (SCREEN_SIZE, i * CELL_SIZE), 2)
        pygame.draw.line(screen, BLACK, (i * CELL_SIZE, 0), (i * CELL_SIZE, SCREEN_SIZE), 2)
    
    # Dibujar piezas en el tablero
    for row in range(4):
        for col in range(4):
            piece = board[row][col]
            if piece is not None:
                draw_piece(piece, col * CELL_SIZE + CELL_SIZE // 2, row * CELL_SIZE + CELL_SIZE // 2)

def draw_piece(piece, x, y):
    """Dibuja una pieza en la posición dada."""
    if piece == 'A':
        pygame.draw.circle(screen, RED, (x, y), CELL_SIZE // 3)
    elif piece == 'B':
        pygame.draw.rect(screen, GREEN, (x - CELL_SIZE // 3, y - CELL_SIZE // 3, CELL_SIZE // 1.5, CELL_SIZE // 1.5))
    elif piece == 'C':
        pygame.draw.polygon(screen, BLUE, [(x, y - CELL_SIZE // 3), (x - CELL_SIZE // 3, y + CELL_SIZE // 3), (x + CELL_SIZE // 3, y + CELL_SIZE // 3)])
    elif piece == 'D':
        pygame.draw.line(screen, YELLOW, (x - CELL_SIZE // 3, y), (x + CELL_SIZE // 3, y), 6)
        pygame.draw.line(screen, YELLOW, (x, y - CELL_SIZE // 3), (x, y + CELL_SIZE // 3), 6)

def draw_menu():
    """Dibuja el menú para seleccionar las piezas."""
    y_start = SCREEN_SIZE
    x_start = 0
    for piece, color in piece_colors.items():
        if player_pieces[0][piece] > 0:  # Mostrar solo si hay piezas disponibles
            button_rect = pygame.Rect(x_start, y_start, SCREEN_SIZE // 4, MENU_HEIGHT)
            piece_buttons[piece] = button_rect
            pygame.draw.rect(screen, GRAY, button_rect)
            pygame.draw.circle(screen, color, (x_start + SCREEN_SIZE // 8, y_start + MENU_HEIGHT // 2), 20)
        x_start += SCREEN_SIZE // 4

def is_valid_move(x, y, piece, player):
    """Verifica si un movimiento es válido."""
    if board[x][y] is not None:
        return False

    for i in range(4):
        if board[x][i] == piece or board[i][y] == piece:
            return False

    quad_x, quad_y = (x // 2) * 2, (y // 2) * 2
    for i in range(quad_x, quad_x + 2):
        for j in range(quad_y, quad_y + 2):
            if board[i][j] == piece:
                return False
    
    return True

def make_move(x, y, piece, player):
    if is_valid_move(x, y, piece, player):
        board[x][y] = piece
        player_pieces[player][piece] -= 1
        return True
    return False

def check_winner():
    """Comprueba si hay un ganador."""
    for i in range(4):
        if len(set(board[i])) == 4 and None not in board[i]:
            return True
        if len(set([board[j][i] for j in range(4)])) == 4 and None not in [board[j][i] for j in range(4)]:
            return True

    for quad_x in range(0, 4, 2):
        for quad_y in range(0, 4, 2):
            pieces_in_quad = []
            for i in range(quad_x, quad_x + 2):
                for j in range(quad_y, quad_y + 2):
                    pieces_in_quad.append(board[i][j])
            if len(set(pieces_in_quad)) == 4 and None not in pieces_in_quad:
                return True
    return False

def ai_move():
    """Movimiento de la IA utilizando Min-Max."""
    best_move = None
    best_value = -float('inf')
    
    for i in range(4):
        for j in range(4):
            for piece, count in player_pieces[1].items():
                if count > 0 and is_valid_move(i, j, piece, 1):
                    board[i][j] = piece
                    move_value = minimax(3, False, -float('inf'), float('inf'))
                    board[i][j] = EMPTY

                    if move_value > best_value:
                        best_value = move_value
                        best_move = (i, j, piece)
    
    if best_move:
        x, y, piece = best_move
        make_move(x, y, piece, 1)

def minimax(depth, is_maximizing, alpha, beta):
    if depth == 0 or check_winner():
        return random.randint(-10, 10)

    if is_maximizing:
        max_eval = -float('inf')
        for i in range(4):
            for j in range(4):
                for piece, count in player_pieces[1].items():
                    if count > 0 and is_valid_move(i, j, piece, 1):
                        board[i][j] = piece
                        eval = minimax(depth - 1, False, alpha, beta)
                        board[i][j] = EMPTY
                        max_eval = max(max_eval, eval)
                        alpha = max(alpha, eval)
                        if beta <= alpha:
                            break
        return max_eval
    else:
        min_eval = float('inf')
        for i in range(4):
            for j in range(4):
                for piece, count in player_pieces[0].items():
                    if count > 0 and is_valid_move(i, j, piece, 0):
                        board[i][j] = piece
                        eval = minimax(depth - 1, True, alpha, beta)
                        board[i][j] = EMPTY
                        min_eval = min(min_eval, eval)
                        beta = min(beta, eval)
                        if beta <= alpha:
                            break
        return min_eval

def player_click(pos):
    """Detecta el clic del jugador y convierte las coordenadas."""
    x, y = pos
    row = y // CELL_SIZE
    col = x // CELL_SIZE
    return row, col

def piece_selection(pos):
    """Detecta el clic del jugador en el menú de piezas."""
    for piece, rect in piece_buttons.items():
        if rect.collidepoint(pos):
            return piece
    return None

def main():
    running = True
    player_turn = True
    selected_piece = None

    while running:
        draw_board()
        draw_menu()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if player_turn:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.pos[1] < SCREEN_SIZE:
                        # Si hace clic en el tablero
                        x, y = player_click(event.pos)
                        if selected_piece and make_move(x, y, selected_piece, 0):
                            if check_winner():
                                print("¡Jugador gana!")
                                running = False
                            player_turn = False
                            selected_piece = None
                    else:
                        # Si hace clic en el menú
                        selected_piece = piece_selection(event.pos)

        if not player_turn:
            ai_move()
            if check_winner():
                print("¡IA gana!")
                running = False
            player_turn = True

        pygame.display.flip()

    pygame.quit()

# Ejecutar el juego
main()
