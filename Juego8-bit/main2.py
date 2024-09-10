import pygame
import sys
import math

# Inicializar Pygame
pygame.init()

# Configuración de la pantalla
WIDTH, HEIGHT = 600, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Quantik")

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Tamaño del tablero y casillas
ROWS, COLS = 4, 4
SQUARE_SIZE = WIDTH // COLS

# Inicializar el tablero
board = [[None for _ in range(COLS)] for _ in range(ROWS)]

# Definir las piezas (formas)
PIECES = ['CIRCLE', 'SQUARE', 'TRIANGLE', 'RHOMBUS']
PIECE_COLORS = {'CIRCLE': RED, 'SQUARE': GREEN, 'TRIANGLE': BLUE, 'RHOMBUS': YELLOW}

def draw_board():
    screen.fill(WHITE)
    for row in range(ROWS):
        for col in range(COLS):
            pygame.draw.rect(screen, BLACK, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), 1)
            if board[row][col]:
                draw_piece(row, col, board[row][col])
    pygame.display.flip()

def draw_piece(row, col, piece):
    x = col * SQUARE_SIZE + SQUARE_SIZE // 2
    y = row * SQUARE_SIZE + SQUARE_SIZE // 2
    size = SQUARE_SIZE // 3
    color = PIECE_COLORS[piece]
    
    if piece == 'CIRCLE':
        pygame.draw.circle(screen, color, (x, y), size)
    elif piece == 'SQUARE':
        pygame.draw.rect(screen, color, (x - size, y - size, size * 2, size * 2))
    elif piece == 'TRIANGLE':
        points = [
            (x, y - size),
            (x - size, y + size),
            (x + size, y + size)
        ]
        pygame.draw.polygon(screen, color, points)
    elif piece == 'RHOMBUS':
        points = [
            (x, y - size),
            (x - size, y),
            (x, y + size),
            (x + size, y)
        ]
        pygame.draw.polygon(screen, color, points)

def check_winner():
    for row in range(ROWS):
        for col in range(COLS):
            piece = board[row][col]
            if piece:
                if check_line(row, col, piece):
                    return True
    return False

def check_line(row, col, piece):
    # Check row
    if all(board[row][c] == piece for c in range(COLS)):
        return True
    # Check column
    if all(board[r][col] == piece for r in range(ROWS)):
        return True
    # Check quadrants
    if row < 2 and col < 2:
        if (all(board[r][c] == piece for r in range(row, row + 2) for c in range(col, col + 2))):
            return True
    return False

def main():
    clock = pygame.time.Clock()
    running = True
    player_turn = 'CIRCLE'
    
    while running:
        draw_board()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                col = x // SQUARE_SIZE
                row = y // SQUARE_SIZE
                
                if board[row][col] is None:
                    board[row][col] = player_turn
                    if check_winner():
                        print(f"Player with {player_turn} wins!")
                        pygame.quit()
                        sys.exit()
                    player_turn = 'SQUARE' if player_turn == 'CIRCLE' else 'TRIANGLE' if player_turn == 'SQUARE' else 'RHOMBUS' if player_turn == 'TRIANGLE' else 'CIRCLE'
        
        clock.tick(30)

if __name__ == "__main__":
    main()
