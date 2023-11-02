import pygame
import time
import random

pygame.init()


# highscore

global highscore
highscore = 0

def load_highscore():
    global highscore
    try:
        fs = open("data.iwannagotosleep", "r")
        highscore = int(fs.read())
        fs.close()
    except Exception:
        highscore = 0

def save_highscore(score):
    fs = open("data.iwannagotosleep", "w")
    fs.write(str(score))
    fs.close()


load_highscore()
print(highscore)


# functions
def message(fonts, msg, color, posx, posy):
    # render(text, antialias, color, background=None)
    # antialias - 선을 부드럽게 만드는 그래픽 기법
    mesg = fonts.render(msg, True, color)
    mesg_Rect = mesg.get_rect()
    mesg_Rect.centerx = posx
    mesg_Rect.centery = posy
    screen.blit(mesg, mesg_Rect)

# Frame - while loop 처리 속도
clock = pygame.time.Clock()

# Fonts
# SysFont(글꼴, size, bold=False, italic=False)
# print(pygame.font.get_fonts())
font_gameOver = pygame.font.SysFont('comicsansms', 50)
font_madeBy = pygame.font.SysFont(None, 20)
font_score = pygame.font.SysFont(None, 30)

# colors
BLUE = (0,0,255); RED = (255,0,0); WHITE = (255,255,255)
BLACK = (0,0,0); GRAY = (127,127,127); YELLOW = (255,255,0)
LIGHT_GREEN = (175,215,70)

# screen 
SCR_WIDTH, SCR_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCR_WIDTH, SCR_HEIGHT))
pygame.display.set_caption('Snake Game')

# snake
snake_list = []
snake_size = 20
snake_speed = 5
snake_pos_x = int(SCR_WIDTH/2 - snake_size/2)
snake_pos_y = int(SCR_HEIGHT/2 - snake_size/2)
snake_posx_change = 0
snake_posy_change = 0
snake_tail = 1


def snake(snake_size, snake_list):
    for pos in snake_list:
        pygame.draw.rect(screen, BLUE, [pos[0], pos[1], snake_size, snake_size])


def reset():
    global snake_list, snake_size, snake_speed, \
        snake_pos_x, snake_pos_y, snake_posx_change, \
        snake_posy_change, snake_tail, \
        foodx, foody, goldx, goldy, score
    snake_list = []
    snake_size = 20
    snake_speed = 5
    snake_pos_x = int(SCR_WIDTH/2 - snake_size/2)
    snake_pos_y = int(SCR_HEIGHT/2 - snake_size/2)
    snake_posx_change = 0
    snake_posy_change = 0
    snake_tail = 1

    foodx = None
    foody = None
    goldx = None
    goldy = None

    food()
    score = 0

# food
foodx = None
foody = None
def food():
    global foodx, foody
    while True :
        foodx = random.randrange(10, SCR_WIDTH - snake_size, snake_size) 
        foody = random.randrange(10, SCR_HEIGHT - snake_size, snake_size)
        food_pos = [foodx,foody]
        if foodx == goldx and foody == goldy:
            continue
        elif food_pos in snake_list :
            continue
        else:
            break


goldx = None
goldy = None
def special_food():
    global goldx, goldy

    while True:
        goldx = random.randrange(10, SCR_WIDTH - snake_size, snake_size)
        goldy = random.randrange(10, SCR_HEIGHT - snake_size, snake_size)

        pos = [ goldx, goldy ]

        if goldx == foodx and goldy == foody:
            continue
        elif pos in snake_list:
            continue
        else:
            break




# score
score = 0 

def game_score(score):
    value = 'Score : ' + str(score)
    message(font_score, value, YELLOW, SCR_WIDTH/2, 30)

def game_highscore():
    global highscore
    value = 'Highscore : ' + str(highscore)
    message(font_score, value, BLACK, SCR_WIDTH / 2, 60)

food()
running = True
saved = False
process = True

while process:
        
    screen.fill(LIGHT_GREEN)
    pygame.draw.rect(screen, GRAY, [0,0, SCR_WIDTH, SCR_HEIGHT], 10)
    # 10은 사각형 테두리의 크기, 뱀이 외벽의 경계면을 넘어갈때, 이 값을 생각해야 함.
    pygame.draw.rect(screen, RED, [foodx, foody, 20, 20])

    # It feels so "SPECIAL!"
    if goldx != None and goldy != None:
        pygame.draw.rect(screen, YELLOW, [ goldx, goldy, 20, 20 ])
    
    snake(snake_size, snake_list)
    game_score(score)
    game_highscore()
    
    if running:
        for event in pygame.event.get():
        #print(event)
            if event.type == pygame.QUIT:
                running = False
                process = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    snake_posx_change = 0
                    snake_posy_change = -20
                if event.key == pygame.K_DOWN:
                    snake_posx_change = 0
                    snake_posy_change = 20
                if event.key == pygame.K_LEFT:
                    snake_posx_change = -20
                    snake_posy_change = 0
                if event.key == pygame.K_RIGHT:
                    snake_posx_change = 20
                    snake_posy_change = 0

        snake_pos_x += snake_posx_change
        snake_pos_y += snake_posy_change

        if snake_pos_x >= (SCR_WIDTH - snake_size) or snake_pos_x - (snake_size/2) < 0 \
            or snake_pos_y >= (SCR_HEIGHT - snake_size) or snake_pos_y - (snake_size/2) < 0:
            running = False

        snake_pos = [snake_pos_x, snake_pos_y]
        if snake_pos in snake_list and snake_pos != snake_list[0]:
            running = False

        # pygame.draw.rect(screen, BLUE, [snake_pos_x, snake_pos_y, snake_size, snake_size])
        snake_head = []
        snake_head.append(snake_pos_x)
        snake_head.append(snake_pos_y)
        snake_list.append(snake_head)
        #print(snake_list)
            
        if len(snake_list) > snake_tail:
            del snake_list[0]
        pygame.display.flip()
        
        if snake_pos_x == foodx and snake_pos_y == foody:
            #print('Yummy!')
            food()
            snake_speed += 1
            score += 10
            print(score)
            snake_tail +=1

        if snake_pos_x == goldx and snake_pos_y == goldy:
            snake_speed += 3
            score += 30
            print(score)
            snake_tail += 3
            goldx = None
            goldy = None
        else:
            rand = random.randrange(0, 100)
            if rand - 98 >= 0 and goldx == None and goldy == None:
                special_food()
            # Special foods spwaned by 2%

        clock.tick(snake_speed)
    else:
        if saved == False:
            if score > highscore:
                highscore = score
                save_highscore(score)
                game_highscore()

            saved = True
        
        message(font_gameOver, 'Game Over', RED, int(SCR_WIDTH/2), int(SCR_HEIGHT/2))
        message(font_madeBy, 'made by kig2929kig', GRAY, int(SCR_WIDTH/2), int(SCR_HEIGHT/2) + 40)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                process = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    reset()
                    saved = False
                    running = True
    


            
pygame.quit()
quit()


# ORIGINAL AUTHOR: kig2929kig

# FEATURES WHAT I MADE
# Highscore system & New death condition & Restart game
