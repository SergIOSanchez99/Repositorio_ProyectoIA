import pygame
import random

# Initialize pygame
pygame.init()

# Constants
BOARD_SIZE = 600  # Set fixed board size to 600x600
SCREEN_WIDTH = BOARD_SIZE
SCREEN_HEIGHT = BOARD_SIZE + 100  # Allow extra space for pieces below
GRID_SIZE = 4
CELL_SIZE = BOARD_SIZE // GRID_SIZE  # Cell size is based on board size, not screen size
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Shapes
SHAPES = ['sphere', 'cube', 'cylinder', 'cone']

# Players
HUMAN = 1
AI = 2

# Setup the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Quantik')

# Board Data Structure
board = [[None for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

# Pieces for each player
pieces = {
    HUMAN: {'sphere': 2, 'cube': 2, 'cylinder': 2, 'cone': 2},
    AI: {'sphere': 2, 'cube': 2, 'cylinder': 2, 'cone': 2}
}

# Selected piece for the human player
selected_piece = None

# Draw the grid
def draw_grid():
    for x in range(1, GRID_SIZE):
        pygame.draw.line(screen, BLACK, (x * CELL_SIZE, 0), (x * CELL_SIZE, BOARD_SIZE), 2)
        pygame.draw.line(screen, BLACK, (0, x * CELL_SIZE), (BOARD_SIZE, x * CELL_SIZE), 2)

# Draw pieces on the board
def draw_pieces():
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            if board[row][col]:
                player, shape = board[row][col]
                color = RED if player == HUMAN else BLUE
                if shape == 'sphere':
                    pygame.draw.circle(screen, color, (col * CELL_SIZE + CELL_SIZE // 2, row * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 4)
                elif shape == 'cube':
                    pygame.draw.rect(screen, color, (col * CELL_SIZE + CELL_SIZE // 4, row * CELL_SIZE + CELL_SIZE // 4, CELL_SIZE // 2, CELL_SIZE // 2))
                elif shape == 'cylinder':
                    pygame.draw.rect(screen, color, (col * CELL_SIZE + CELL_SIZE // 3, row * CELL_SIZE + CELL_SIZE // 4, CELL_SIZE // 4, CELL_SIZE // 2))
                elif shape == 'cone':
                    pygame.draw.polygon(screen, color, [(col * CELL_SIZE + CELL_SIZE // 2, row * CELL_SIZE + CELL_SIZE // 4),
                                                       (col * CELL_SIZE + CELL_SIZE // 4, row * CELL_SIZE + CELL_SIZE // 2),
                                                       (col * CELL_SIZE + 3 * CELL_SIZE // 4, row * CELL_SIZE + CELL_SIZE // 2)])

# Draw the available pieces for the human player to choose
def draw_available_pieces():
    x_offset = 10
    y_offset = BOARD_SIZE + 20  # Position just below the board

    clickable_areas = {}  # Store clickable areas for remaining pieces

    for shape in SHAPES:
        if pieces[HUMAN][shape] > 0:  # Only draw if there are pieces available
            if shape == 'sphere':
                pygame.draw.circle(screen, RED, (x_offset + 30, y_offset), 20)
                clickable_areas['sphere'] = pygame.Rect(x_offset, y_offset - 20, 60, 40)
            elif shape == 'cube':
                pygame.draw.rect(screen, RED, (x_offset + 10, y_offset - 20, 40, 40))
                clickable_areas['cube'] = pygame.Rect(x_offset + 10, y_offset - 20, 40, 40)
            elif shape == 'cylinder':
                pygame.draw.rect(screen, RED, (x_offset + 20, y_offset - 20, 20, 40))
                clickable_areas['cylinder'] = pygame.Rect(x_offset + 20, y_offset - 20, 20, 40)
            elif shape == 'cone':
                pygame.draw.polygon(screen, RED, [(x_offset + 30, y_offset - 30),
                                                  (x_offset + 10, y_offset + 20),
                                                  (x_offset + 50, y_offset + 20)])
                clickable_areas['cone'] = pygame.Rect(x_offset + 10, y_offset - 30, 40, 50)
            
            x_offset += 70

    return clickable_areas

# Check if a shape is already placed by the opponent in the row, column, or 2x2 region
def is_valid_move(row, col, shape, player):
    opponent = AI if player == HUMAN else HUMAN  # Determine the opponent
    
    # Check row and column
    for i in range(GRID_SIZE):
        if board[row][i] and board[row][i][0] == opponent and board[row][i][1] == shape:
            return False
        if board[i][col] and board[i][col][0] == opponent and board[i][col][1] == shape:
            return False

    # Check 2x2 region
    region_row, region_col = row // 2 * 2, col // 2 * 2
    for i in range(region_row, region_row + 2):
        for j in range(region_col, region_col + 2):
            if board[i][j] and board[i][j][0] == opponent and board[i][j][1] == shape:
                return False

    return True

# Place a piece on the board
def place_piece(row, col, shape, player):
    board[row][col] = (player, shape)
    pieces[player][shape] -= 1

# AI move (basic random valid move)
def ai_move():
    valid_moves = []
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            if not board[row][col]:  # empty space
                for shape in SHAPES:
                    if pieces[AI][shape] > 0 and is_valid_move(row, col, shape, AI):
                        valid_moves.append((row, col, shape))

    if valid_moves:
        move = random.choice(valid_moves)
        place_piece(*move, AI)

# Check for a winning move (4 different shapes in a row, column, or region)
def check_win(player):
    # Check rows and columns
    for i in range(GRID_SIZE):
        if len(set([board[i][j][1] for j in range(GRID_SIZE) if board[i][j] and board[i][j][0] == player])) == 4:
            return True
        if len(set([board[j][i][1] for j in range(GRID_SIZE) if board[j][i] and board[j][i][0] == player])) == 4:
            return True

    # Check 2x2 regions
    for row in range(0, GRID_SIZE, 2):
        for col in range(0, GRID_SIZE, 2):
            shapes = set()
            for i in range(row, row + 2):
                for j in range(col, col + 2):
                    if board[i][j] and board[i][j][0] == player:
                        shapes.add(board[i][j][1])
            if len(shapes) == 4:
                return True

    return False

# Main game loop
def main():
    global selected_piece  # Ensure selected_piece is global

    running = True
    turn = HUMAN  # Human goes first

    while running:
        screen.fill(WHITE)
        draw_grid()
        draw_pieces()

        # Draw available pieces for human player
        if turn == HUMAN and selected_piece is None:
            draw_available_pieces()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if turn == HUMAN:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()  # Get the mouse click position
                    if selected_piece is None:
                        # Check if the player clicked on an available piece
                        clickable_areas = draw_available_pieces()  # Get the clickable areas dynamically
                        for shape, rect in clickable_areas.items():
                            if rect.collidepoint(x, y):
                                selected_piece = shape
                                break
                    else:
                        # After selecting the piece, check where to place it
                        row, col = y // CELL_SIZE, x // CELL_SIZE  # Convert mouse click to board grid
                        if row < GRID_SIZE and col < GRID_SIZE and not board[row][col] and is_valid_move(row, col, selected_piece, HUMAN):
                            place_piece(row, col, selected_piece, HUMAN)
                            if check_win(HUMAN):
                                print("Human Wins!")
                                running = False
                            selected_piece = None  # Reset selection
                            turn = AI  # AI's turn


        if turn == AI:
            ai_move()
            if check_win(AI):
                print("AI Wins!")
                running = False
            turn = HUMAN

        pygame.display.flip()

    pygame.quit()

if __name__ == '__main__':
    main()