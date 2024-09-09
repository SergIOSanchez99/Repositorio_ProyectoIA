import pygame
import sys
import random

# initialize the constructor
pygame.init()
res = (1080, 720)

# randomly assigns a value to variables ranging from lower limit to upper
c1 = random.randint(125, 255)
c2 = random.randint(0, 255)
c3 = random.randint(0, 255)

screen = pygame.display.set_mode(res)
clock = pygame.time.Clock()
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
color_list = [red, green, blue]
colox_c1 = 0
colox_c2 = 0
colox_c3 = 254
colox_c4 = 254

# randomly assigns a colour from color_list to player
player_c = random.choice(color_list)

# light shade of menu buttons
startl = (169, 169, 169)

# dark shade of menu buttons
startd = (100, 100, 100)
white = (255, 255, 255)
start = (255, 255, 255)
width = screen.get_width()
height = screen.get_height()

# initial X position of player
lead_x = 40

# initial y position of player
lead_y = height / 2
x = 300
y = 290
width1 = 100
height1 = 40
enemy_size = 50

# defining a font
smallfont = pygame.font.SysFont('Consolas', 25)
smallfont_title = pygame.font.SysFont('Bauhaus 93', 70)

# texts to be rendered on screen
text = smallfont.render('INICIO', True, white)
text1 = smallfont.render('OPCIONES', True, white)
exit1 = smallfont.render('SALIR', True, white)

# game title
colox = smallfont_title.render('8-BIT', True, (52,205,106))
x1 = width//2 - colox.get_width()//2
y1 = 50
x2 = 60
y2 = 40
speed = 15

# score of the player
count = 0
rgb = random.choice(color_list)

# enemy position
e_p = [width, random.randint(50, height - 50)]
e1_p = [random.randint(width, width + 100), random.randint(50, height - 100)]

# function for game_over
def game_over():
    while True:
        # if the player clicks the cross button
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if ev.type == pygame.MOUSEBUTTONDOWN:
                mouse1 = pygame.mouse.get_pos()

                # Detect if "SALIR" button is clicked
                if 110 < mouse1[0] < 210 and height - 100 < mouse1[1] < height - 60:
                    pygame.quit()
                    sys.exit()

                # Detect if "EMPEZAR DE NUEVO" button is clicked
                if width - 160 < mouse1[0] < width - 80 and height - 100 < mouse1[1] < height - 80:
                    # Calling the game function to restart
                    game(lead_y, lead_x, speed, count)

        # fills the screen with specified colour
        screen.fill((65, 25, 64))
        smallfont = pygame.font.SysFont('Consolas', 40)
        smallfont1 = pygame.font.SysFont('Consolas', 20)
        game_over_text = smallfont.render('JUEGO TERMINADO', True, white)
        game_exit = smallfont1.render('SALIR', True, white)
        restart = smallfont1.render('EMPEZAR DE NUEVO', True, white)
        mouse1 = pygame.mouse.get_pos()

        # exit
        if 110 < mouse1[0] < 210 and height - 100 < mouse1[1] < height - 60:
            pygame.draw.rect(screen, startl, [110, height - 100, 100, 40])
        else:
            pygame.draw.rect(screen, startd, [110, height - 100, 100, 40])

        # restart
        if width - 160 < mouse1[0] < width - 80 and height - 100 < mouse1[1] < height - 80:
            pygame.draw.rect(screen, startl, [width - 160, height - 100, 80, 20])
        else:
            pygame.draw.rect(screen, startd, [width - 160, height - 100, 80, 20])

        screen.blit(game_exit, (120, height - 90))
        screen.blit(restart, (width - 180, height - 100))
        screen.blit(game_over_text, (width // 2 - 150, 295))

        # updates frames of the game
        pygame.display.update()

# function for body of the game
def game(lead_y, lead_x, speed, count):
    while True:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # player control
        # keeps track of the key pressed
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            # if up key is pressed then the player's y pos will decrement by 10
            lead_y -= 10
        if keys[pygame.K_DOWN]:
            # if down key is pressed then the y pos of the player is incremented by 10
            lead_y += 10
        screen.fill((65, 25, 64))
        clock.tick(speed)

        # draws a rectangle on the screen
        rect = pygame.draw.rect(screen, player_c, [lead_x, lead_y, 40, 40])
        pygame.draw.rect(screen, (c1, c2, c3), [0, 0, width, 40])
        pygame.draw.rect(screen, (c3, c2, c1), [0, 680, width, 40])
        pygame.draw.rect(screen, startd, [width - 100, 0, 100, 40])
        smallfont = pygame.font.SysFont('Monospace', 35)
        exit2 = smallfont.render('Salir', True, white)

        # exit
        # gets the X and y position of mouse pointer and stores them as a tuple
        mouse = pygame.mouse.get_pos()
        if width - 100 < mouse[0] < width and 0 < mouse[1] < 40:
            pygame.draw.rect(screen, startl, [width - 100, 0, 100, 40])
        else:
            pygame.draw.rect(screen, startd, [width - 100, 0, 100, 40])
        if width - 100 < mouse[0] < width and 0 < mouse[1] < 40:
            if ev.type == pygame.MOUSEBUTTONDOWN:
                pygame.quit()
                sys.exit()

        # enemy position
        if e_p[0] > 0 and e_p[0] <= width:
            e_p[0] -= 10
        else:
            if e_p[1] <= 40 or e_p[1] >= height - 40:
                e_p[1] = height // 2
            e_p[1] = random.randint(enemy_size, height - enemy_size)
            e_p[0] = width

        # game over
        # collision detection
        if lead_x <= e_p[0] <= lead_x + 40 and lead_y >= e_p[1] >= lead_y - 40:
            game_over()

        # checks if the player block has collided with the enemy block
        if lead_y <= e_p[1] + enemy_size <= lead_y + 40 and lead_x <= e_p[0] <= lead_x + 40:
            game_over()

        pygame.draw.rect(screen, red, [e_p[0], e_p[1], enemy_size, enemy_size])
        if e1_p[0] > 0 and e1_p[0] <= width + 100:
            e1_p[0] -= 10
        else:
            if e1_p[1] <= 40 or e1_p[1] >= height - 40:
                e1_p[1] = height // 2
            e1_p[1] = random.randint(enemy_size, height - 40)
            e1_p[0] = width + 100

        if lead_x <= e1_p[0] <= lead_x + 40 and lead_y >= e1_p[1] >= lead_y - 40:
            e1_p[0] = width + 100
            e1_p[1] = random.randint(40, height - 40)
            count += 1
            speed += 1
        if lead_y <= e1_p[1] + enemy_size <= lead_y + 40 and lead_x <= e1_p[0] <= lead_x + 40:
            e1_p[0] = width + 100
            e1_p[1] = random.randint(40, height - 40)

            # increases the score when blue box is hit
            count += 1

            # increases the speed as score increases
            speed += 1

            if count >= 45:
                # freezes the game FPS to 60 if score reaches 45 or more
                speed = 60

        if lead_y <= 38 or lead_y >= height - 38:
            game_over()
        if e1_p[1] <= 40 or e1_p[1] >= height - 40:
            e1_p[1] = height // 2
        score = smallfont.render(f'Puntaje: {count}', True, white)
        screen.blit(score, (20, 10))
        screen.blit(exit2, (width - 80, 5))
        pygame.draw.rect(screen, blue, [e1_p[0], e1_p[1], 50, 50])

        pygame.display.update()


while True:
    # stores the (x,y) coordinates into the variable as a tuple
    mouse = pygame.mouse.get_pos()

    # background color
    screen.fill((65, 25, 64))

    # when the mouse is hovered on a button, it changes to a lighter shade
    if width / 2 - 70 <= mouse[0] <= width / 2 + 60 and height / 2 <= mouse[1] <= height / 2 + 40:
        pygame.draw.rect(screen, startl, [width / 2 - 70, height / 2, 140, 40])

    else:
        pygame.draw.rect(screen, startd, [width / 2 - 70, height / 2, 140, 40])

    if width / 2 - 70 <= mouse[0] <= width / 2 + 60 and height / 2 + 60 <= mouse[1] <= height / 2 + 100:
        pygame.draw.rect(screen, startl, [width / 2 - 70, height / 2 + 60, 140, 40])

    else:
        pygame.draw.rect(screen, startd, [width / 2 - 70, height / 2 + 60, 140, 40])

    if width / 2 - 70 <= mouse[0] <= width / 2 + 60 and height / 2 + 120 <= mouse[1] <= height / 2 + 160:
        pygame.draw.rect(screen, startl, [width / 2 - 70, height / 2 + 120, 140, 40])

    else:
        pygame.draw.rect(screen, startd, [width / 2 - 70, height / 2 + 120, 140, 40])

    # superimposing the text onto our buttons
    screen.blit(text, (width / 2 - 55, height / 2))
    screen.blit(text1, (width / 2 - 60, height / 2 + 60))
    screen.blit(exit1, (width / 2 - 45, height / 2 + 120))
    screen.blit(colox, (x1, y1))

    for ev in pygame.event.get():

        # checks if a mouse is clicked
        if ev.type == pygame.MOUSEBUTTONDOWN:
            if width / 2 - 70 <= mouse[0] <= width / 2 + 60 and height / 2 <= mouse[1] <= height / 2 + 40:
                game(lead_y, lead_x, speed, count)

            if width / 2 - 70 <= mouse[0] <= width / 2 + 60 and height / 2 + 60 <= mouse[1] <= height / 2 + 100:
                game(lead_y, lead_x, speed, count)

            if width / 2 - 70 <= mouse[0] <= width / 2 + 60 and height / 2 + 120 <= mouse[1] <= height / 2 + 160:
                pygame.quit()
                sys.exit()

        # if the user clicks on the cross button, the loop will break
        if ev.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # updates the frames of the game
    pygame.display.update()
