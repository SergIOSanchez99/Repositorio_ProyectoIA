import pygame
import random

# Inicializar Pygame
pygame.init()

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)   # Color del jugador
BLUE = (0, 0, 255)  # Color de la IA
GRAY = (200, 200, 200)
GREEN = (0, 255, 0)

# Tamaños de pantalla y celdas
SCREEN_SIZE = 400
CELL_SIZE = SCREEN_SIZE // 4
MENU_HEIGHT = 100

# Crear ventana
screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE + MENU_HEIGHT))
pygame.display.set_caption("Quantik")

# Piezas de los jugadores
player_pieces = {
    0: {'cuadrado': 2, 'rectangulo': 2, 'circulo': 2, 'triangulo': 2},
    1: {'cuadrado': 2, 'rectangulo': 2, 'circulo': 2, 'triangulo': 2}
}

# Tablero de 4x4
EMPTY = None
board = [[EMPTY for _ in range(4)] for _ in range(4)]

# Fuente para texto
font = pygame.font.Font(None, 36)

# Piezas disponibles
piece_buttons = {}
piece_colors = {'cuadrado': RED, 'rectangulo': BLUE, 'circulo': RED, 'triangulo': BLUE}

ganador = None  # Variable para almacenar el nombre del ganador
empate = False  # Variable para verificar si hay empate

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
    """Dibuja una pieza en la posición dada con el color apropiado."""
    color = RED if piece[1] == 'HUMANO' else BLUE  # Piezas del jugador en rojo y de la IA en azul
    if piece[0] == 'cuadrado':
        pygame.draw.rect(screen, color, (x - CELL_SIZE // 3, y - CELL_SIZE // 3, CELL_SIZE // 1.5, CELL_SIZE // 1.5))
    elif piece[0] == 'rectangulo':  # Cambio de cilindro a rectángulo vertical
        pygame.draw.rect(screen, color, (x - CELL_SIZE // 6, y - CELL_SIZE // 3, CELL_SIZE // 3, CELL_SIZE // 1.5))
    elif piece[0] == 'circulo':
        pygame.draw.circle(screen, color, (x, y), CELL_SIZE // 3)
    elif piece[0] == 'triangulo':
        pygame.draw.polygon(screen, color, [(x, y - CELL_SIZE // 3), (x - CELL_SIZE // 3, y + CELL_SIZE // 3), 
                                             (x + CELL_SIZE // 3, y + CELL_SIZE // 3)])

def draw_menu():
    """Dibuja el menú para seleccionar las piezas."""
    y_start = SCREEN_SIZE
    x_start = 0
    for piece, color in piece_colors.items():
        if player_pieces[0][piece] > 0:  # Mostrar solo si hay piezas disponibles
            button_rect = pygame.Rect(x_start, y_start, SCREEN_SIZE // 4, MENU_HEIGHT)
            piece_buttons[piece] = button_rect
            draw_piece((piece, 'HUMANO'), x_start + SCREEN_SIZE // 8, y_start + MENU_HEIGHT // 2)
        x_start += SCREEN_SIZE // 4

def is_valid_move(x, y, piece):
    """Verifica si un movimiento es válido."""
    if board[x][y] is not None:
        return False

    for i in range(4):
        if board[x][i] is not None and board[x][i][0] == piece[0]:
            return False
        if board[i][y] is not None and board[i][y][0] == piece[0]:
            return False

    quad_x, quad_y = (x // 2) * 2, (y // 2) * 2
    for i in range(quad_x, quad_x + 2):
        for j in range(quad_y, quad_y + 2):
            if board[i][j] is not None and board[i][j][0] == piece[0]:
                return False
    
    return True

def make_move(x, y, piece):
    """Coloca la pieza en el tablero si es un movimiento válido."""
    if is_valid_move(x, y, piece):
        board[x][y] = piece
        player_pieces[0 if piece[1] == 'HUMANO' else 1][piece[0]] -= 1
        return True
    return False

def check_winner():
    """Comprueba si hay un ganador, verificando filas, columnas y cuadrantes."""
    global ganador
    # Comprobar filas
    for i in range(4):
        fila_piezas = [board[i][j] for j in range(4) if board[i][j] is not None]
        if len(fila_piezas) == 4 and len(set(p[0] for p in fila_piezas)) == 4:
            ganador = fila_piezas[0][1]  # Asignar ganador
            return True
    # Comprobar columnas
    for i in range(4):
        columna_piezas = [board[j][i] for j in range(4) if board[j][i] is not None]
        if len(columna_piezas) == 4 and len(set(p[0] for p in columna_piezas)) == 4:
            ganador = columna_piezas[0][1]  # Asignar ganador
            return True

    # Comprobar cuadrantes
    for quad_x in range(0, 4, 2):
        for quad_y in range(0, 4, 2):
            piezas_cuadrante = []
            for i in range(quad_x, quad_x + 2):
                for j in range(quad_y, quad_y + 2):
                    if board[i][j] is not None:
                        piezas_cuadrante.append(board[i][j])
            if len(piezas_cuadrante) == 4 and len(set(p[0] for p in piezas_cuadrante)) == 4:
                ganador = piezas_cuadrante[0][1]  # Asignar ganador
                return True
    return False

def check_tie():
    """Comprueba si hay empate cuando no quedan movimientos válidos."""
    for i in range(4):
        for j in range(4):
            if board[i][j] is None:
                return False  # Si hay alguna celda vacía, no es empate
    return True  # No hay celdas vacías, es empate

def draw_winner():
    """Dibuja al ganador en la interfaz."""
    if ganador == "HUMANO":
        win_text = font.render("¡Jugador gana!", True, RED)
    elif ganador == "IA":
        win_text = font.render("¡IA gana!", True, BLUE)
    
    screen.blit(win_text, (SCREEN_SIZE // 2 - win_text.get_width() // 2, SCREEN_SIZE // 2 - win_text.get_height() // 2))
    pygame.display.flip()
    pygame.time.wait(3000)

def draw_tie():
    """Dibuja un mensaje de empate en la interfaz."""
    tie_text = font.render("¡Empate!", True, BLACK)
    screen.blit(tie_text, (SCREEN_SIZE // 2 - tie_text.get_width() // 2, SCREEN_SIZE // 2 - tie_text.get_height() // 2))
    pygame.display.flip()
    pygame.time.wait(3000)

def ai_move():
    """Movimiento de la IA."""
    valid_moves = []
    for i in range(4):
        for j in range(4):
            for piece, count in player_pieces[1].items():
                if count > 0 and is_valid_move(i, j, (piece, 'IA')):
                    valid_moves.append((i, j, piece))
    
    if valid_moves:
        x, y, piece = random.choice(valid_moves)
        make_move(x, y, (piece, 'IA'))
        draw_board()  # Mostrar el movimiento de la IA
        pygame.display.flip()  # Actualizar la pantalla antes de continuar
        pygame.time.wait(500)  # Esperar medio segundo para visualizar el movimiento

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

def seleccionar_turno():
    """Muestra una pantalla para seleccionar quién comienza el juego."""
    screen.fill(WHITE)
    font = pygame.font.Font(None, 48)
    texto_humano = font.render("Humano empieza", True, BLACK)
    texto_ia = font.render("IA empieza", True, BLACK)

    boton_humano = pygame.Rect(50, 200, 300, 50)
    boton_ia = pygame.Rect(50, 300, 300, 50)

    pygame.draw.rect(screen, GREEN, boton_humano)
    pygame.draw.rect(screen, GREEN, boton_ia)

    screen.blit(texto_humano, (boton_humano.x + 10, boton_humano.y + 10))
    screen.blit(texto_ia, (boton_ia.x + 10, boton_ia.y + 10))
    pygame.display.flip()

    esperando_seleccion = True
    while esperando_seleccion:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                if boton_humano.collidepoint(event.pos):
                    esperando_seleccion = False
                    return "HUMANO"
                elif boton_ia.collidepoint(event.pos):
                    esperando_seleccion = False
                    return "IA"

def main():
    global ganador, empate
    running = True
    player_turn = True
    selected_piece = None

    # Elegir quién comienza
    quien_comienza = seleccionar_turno()

    # Dibujar el tablero antes de que la IA haga el primer movimiento
    draw_board()
    pygame.display.flip()

    if quien_comienza == "IA":
        ai_move()
        player_turn = True
    else:
        player_turn = True

    while running:
        draw_board()
        draw_menu()

        if ganador:  # Si ya hay un ganador, detener el juego
            draw_winner()
            running = False
            continue

        if check_tie():  # Verificar si hay empate
            empate = True
            draw_tie()  # Mostrar el mensaje de empate
            running = False
            continue

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if player_turn and not ganador and not empate:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.pos[1] < SCREEN_SIZE:
                        # Si hace clic en el tablero
                        x, y = player_click(event.pos)
                        if selected_piece and make_move(x, y, (selected_piece, 'HUMANO')):
                            draw_board()  # Mostrar el movimiento del jugador
                            pygame.display.flip()  # Actualizar la pantalla
                            pygame.time.wait(500)  # Esperar medio segundo
                            if check_winner():
                                draw_board()  # Mostrar el último movimiento
                                pygame.display.flip()  # Actualizar la pantalla
                                pygame.time.wait(500)  # Esperar un momento
                                draw_winner()  # Mostrar el mensaje del ganador
                                running = False
                            else:
                                ai_move()
                                if check_winner():
                                    draw_board()  # Mostrar el último movimiento de la IA
                                    pygame.display.flip()  # Actualizar la pantalla
                                    pygame.time.wait(500)  # Esperar un momento
                                    draw_winner()  # Mostrar el mensaje del ganador
                                    running = False
                            player_turn = True
                            selected_piece = None
                    else:
                        # Si hace clic en el menú
                        selected_piece = piece_selection(event.pos)

        pygame.display.flip()

    pygame.quit()

# Ejecutar el juego
main()
