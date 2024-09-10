import pygame
import random

# Inicializar Pygame
pygame.init()

# Dimensiones de la ventana
WINDOW_SIZE = 500
CELL_SIZE = WINDOW_SIZE // 4
BUTTON_SIZE = 80
INFO_HEIGHT = 40

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

# Piezas como formas geométricas
SHAPES = ['CIRCLE', 'SQUARE', 'TRIANGLE', 'DIAMOND']
USER_COLOR = BLUE
MACHINE_COLOR = RED

# Inicializar el tablero vacío (4x4)
board = [['' for _ in range(4)] for _ in range(4)]

# Crear la ventana del juego
screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE + BUTTON_SIZE + INFO_HEIGHT))
pygame.display.set_caption("Quantik Game")

# Cargar imágenes de las figuras
circle_img = pygame.Surface((BUTTON_SIZE, BUTTON_SIZE), pygame.SRCALPHA)
pygame.draw.circle(circle_img, USER_COLOR, (BUTTON_SIZE // 2, BUTTON_SIZE // 2), BUTTON_SIZE // 2 - 10)
square_img = pygame.Surface((BUTTON_SIZE, BUTTON_SIZE), pygame.SRCALPHA)
pygame.draw.rect(square_img, USER_COLOR, (10, 10, BUTTON_SIZE - 20, BUTTON_SIZE - 20))
triangle_img = pygame.Surface((BUTTON_SIZE, BUTTON_SIZE), pygame.SRCALPHA)
pygame.draw.polygon(triangle_img, USER_COLOR, [
    (BUTTON_SIZE // 2, 10),
    (10, BUTTON_SIZE - 10),
    (BUTTON_SIZE - 10, BUTTON_SIZE - 10)
])
diamond_img = pygame.Surface((BUTTON_SIZE, BUTTON_SIZE), pygame.SRCALPHA)
pygame.draw.polygon(diamond_img, USER_COLOR, [
    (BUTTON_SIZE // 2, 10),
    (10, BUTTON_SIZE // 2),
    (BUTTON_SIZE // 2, BUTTON_SIZE - 10),
    (BUTTON_SIZE - 10, BUTTON_SIZE // 2)
])

# Fuente para el texto
font = pygame.font.Font(None, 36)

# Función para dibujar el tablero
def draw_board(screen, board, message):
    screen.fill(WHITE)
    for row in range(4):
        for col in range(4):
            rect = pygame.Rect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, BLACK, rect, 1)
            piece = board[row][col]
            if piece:
                color = MACHINE_COLOR if piece.islower() else USER_COLOR
                draw_shape(screen, piece.upper(), color, (col * CELL_SIZE, row * CELL_SIZE))
    
    # Dibujar mensaje
    message_surf = font.render(message, True, BLACK)
    screen.blit(message_surf, (10, WINDOW_SIZE + 10))
    
    # Dibujar botones de selección de figuras
    screen.blit(circle_img, (10, WINDOW_SIZE + INFO_HEIGHT))
    screen.blit(square_img, (100, WINDOW_SIZE + INFO_HEIGHT))
    screen.blit(triangle_img, (190, WINDOW_SIZE + INFO_HEIGHT))
    screen.blit(diamond_img, (280, WINDOW_SIZE + INFO_HEIGHT))
    
    pygame.display.flip()

# Función para dibujar una figura en el tablero
def draw_shape(screen, shape, color, pos):
    if shape == 'CIRCLE':
        pygame.draw.circle(screen, color, (pos[0] + CELL_SIZE // 2, pos[1] + CELL_SIZE // 2), CELL_SIZE // 2 - 10)
    elif shape == 'SQUARE':
        pygame.draw.rect(screen, color, (pos[0] + 10, pos[1] + 10, CELL_SIZE - 20, CELL_SIZE - 20))
    elif shape == 'TRIANGLE':
        pygame.draw.polygon(screen, color, [
            (pos[0] + CELL_SIZE // 2, pos[1] + 10),
            (pos[0] + 10, pos[1] + CELL_SIZE - 10),
            (pos[0] + CELL_SIZE - 10, pos[1] + CELL_SIZE - 10)
        ])
    elif shape == 'DIAMOND':
        pygame.draw.polygon(screen, color, [
            (pos[0] + CELL_SIZE // 2, pos[1] + 10),
            (pos[0] + 10, pos[1] + CELL_SIZE // 2),
            (pos[0] + CELL_SIZE // 2, pos[1] + CELL_SIZE - 10),
            (pos[0] + CELL_SIZE - 10, pos[1] + CELL_SIZE // 2)
        ])

# Función para verificar si la colocación es válida
def is_valid_move(board, row, col, piece):
    if board[row][col] != '':
        return False
    for i in range(4):
        if board[row][i].lower() == piece.lower() or board[i][col].lower() == piece.lower():
            return False
    start_row, start_col = 2 * (row // 2), 2 * (col // 2)
    for i in range(2):
        for j in range(2):
            if board[start_row + i][start_col + j].lower() == piece.lower():
                return False
    return True

# Función para verificar si hay un ganador
def check_winner(board):
    for i in range(4):
        if len(set(board[i])) == 4 and '' not in board[i]:
            return True
        if len(set([board[j][i] for j in range(4)])) == 4 and '' not in [board[j][i] for j in range(4)]:
            return True
    for row in range(0, 4, 2):
        for col in range(0, 4, 2):
            quadrants = set()
            for i in range(2):
                for j in range(2):
                    quadrants.add(board[row + i][col + j])
            if len(quadrants) == 4 and '' not in quadrants:
                return True
    return False

# Función para el turno del jugador
def player_turn():
    selected_piece = None
    while selected_piece is None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if y > WINDOW_SIZE + INFO_HEIGHT:
                    if 10 <= x < 10 + BUTTON_SIZE:
                        selected_piece = 'CIRCLE'
                    elif 100 <= x < 100 + BUTTON_SIZE:
                        selected_piece = 'SQUARE'
                    elif 190 <= x < 190 + BUTTON_SIZE:
                        selected_piece = 'TRIANGLE'
                    elif 280 <= x < 280 + BUTTON_SIZE:
                        selected_piece = 'DIAMOND'
                else:
                    col, row = x // CELL_SIZE, y // CELL_SIZE
                    if selected_piece and is_valid_move(board, row, col, selected_piece):
                        board[row][col] = selected_piece
                        SHAPES.remove(selected_piece)
                        return

        draw_board(screen, board, "Tu turno. Elige una figura y haz tu movimiento.")

# Función para el turno de la máquina
def machine_turn():
    selected_piece = random.choice(SHAPES)
    pos = None
    while pos is None:
        row = random.randint(0, 3)
        col = random.randint(0, 3)
        if is_valid_move(board, row, col, selected_piece):
            board[row][col] = selected_piece.lower()
            SHAPES.remove(selected_piece)
            pos = (row, col)
    draw_board(screen, board, "Turno del oponente...")
    pygame.time.delay(1000)  # Añadir un pequeño retraso para que el jugador pueda ver la jugada de la máquina

# Juego principal
def play_game():
    running = True
    while running:
        player_turn()
        if check_winner(board):
            draw_board(screen, board, "¡Felicidades! ¡Has ganado!")
            running = False
        else:
            machine_turn()
            if check_winner(board):
                draw_board(screen, board, "La máquina ha ganado.")
                running = False
        if not SHAPES:
            draw_board(screen, board, "Empate. No quedan más movimientos.")
            running = False

# Iniciar el juego
play_game()

pygame.quit()
