import pygame
import random

# Initialize pygame
pygame.init()

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 600, 600
GRID_SIZE = 4
CELL_SIZE = SCREEN_WIDTH // GRID_SIZE
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

# Draw the grid
def draw_grid():
    for x in range(1, GRID_SIZE):
        pygame.draw.line(screen, BLACK, (x * CELL_SIZE, 0), (x * CELL_SIZE, SCREEN_HEIGHT), 2)
        pygame.draw.line(screen, BLACK, (0, x * CELL_SIZE), (SCREEN_WIDTH, x * CELL_SIZE), 2)

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

# Check if a shape is already placed in the row, column, or 2x2 region
def is_valid_move(row, col, shape, player):
    # Check row and column
    for i in range(GRID_SIZE):
        if board[row][i] and board[row][i][1] == shape:
            return False
        if board[i][col] and board[i][col][1] == shape:
            return False

    # Check 2x2 region
    region_row, region_col = row // 2 * 2, col // 2 * 2
    for i in range(region_row, region_row + 2):
        for j in range(region_col, region_col + 2):
            if board[i][j] and board[i][j][1] == shape:
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
    running = True
    turn = HUMAN  # Human goes first
    game_over = False

    while running:
        screen.fill(WHITE)
        draw_grid()
        draw_pieces()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if not game_over and turn == HUMAN and event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                row, col = y // CELL_SIZE, x // CELL_SIZE

                if not board[row][col]:  # If the cell is empty
                    for shape in SHAPES:
                        if pieces[HUMAN][shape] > 0 and is_valid_move(row, col, shape, HUMAN):
                            place_piece(row, col, shape, HUMAN)
                            if check_win(HUMAN):
                                print("Human Wins!")
                                game_over = True
                            turn = AI
                            break

        if not game_over and turn == AI:
            ai_move()
            if check_win(AI):
                print("AI Wins!")
                game_over = True
            turn = HUMAN

        pygame.display.flip()

    pygame.quit()

# Run the game
if __name__ == "__main__":
    main()
