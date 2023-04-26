import pygame, time, sys
from pygame.locals import *

pygame.init()
pygame.mixer.init()
WIDTH, HEIGHT = 700, 400
surface = pygame.display.set_mode((WIDTH, HEIGHT)) 
pygame.display.set_caption('Ping Pong') 
FPS = 60
clock = pygame.time.Clock()
intro_loop = True
game_loop = False
end_loop = True

#table
background_color = 'White'
intro_img = pygame.image.load('assets/menu.png')
intro_img_rect = intro_img.get_rect(center = (WIDTH/2, HEIGHT/2))
press_img = pygame.image.load('assets/press.png')
press_img_rect = press_img.get_rect(center = (WIDTH/2, HEIGHT/2 + 80))

#score
player_score = 0
bot_score = 0
font = pygame.font.SysFont('assets/font.otf', 30)
font2 = pygame.font.SysFont('assets/font.otf', 100)
sound2 = pygame.mixer.Sound('assets/win.wav')

#player
player = pygame.Rect(5,HEIGHT/2 - 60, 10, 120)
bot = pygame.Rect(WIDTH - 15,HEIGHT/2 - 60, 10, 120)
player_move = 0
bot_move = 10

#ball 
ball = pygame.Rect(WIDTH/2 - 10, HEIGHT/2 - 10, 20, 20)
ball_move_x = 5
ball_move_y = 2
sound = pygame.mixer.Sound('assets/pong.wav')

def table():
    surface.fill(background_color)
    pygame.draw.line(surface, 'red', (350,0), (350,400))
    pygame.draw.line(surface, 'red', (0,0), (WIDTH,0))
    pygame.draw.line(surface, 'red', (0,0), (0,HEIGHT))
    pygame.draw.line(surface, 'red', (WIDTH-1,0), (WIDTH-1,HEIGHT))
    pygame.draw.line(surface, 'red', (0,HEIGHT-1), (WIDTH,HEIGHT-1))

def score(text, font, color, score_x_pos, score_y_pos):
    img = font.render(str(text), True, color)
    img_rect = img.get_rect(center= (score_x_pos, score_y_pos))
    surface.blit(img, img_rect)

def ball_movement():
    global ball_move_x,ball_move_y, player_score, bot_score

    pygame.draw.ellipse(surface,'black', ball)

 
    ball.x += ball_move_x
    ball.y += ball_move_y

    if ball.top <= 0 or ball.bottom >= HEIGHT:
        ball_move_y *= -1

    if ball.left <= 0:
        bot_score += 1
        ball.x = WIDTH/2 - 10
        ball.y = HEIGHT/2 - 10
        ball.x -= ball_move_x
        ball.y -= ball_move_y
        pygame.time.delay(600)
        sound2.play()
    if ball.right >= WIDTH:
        player_score += 1
        ball.x = WIDTH/2 - 10
        ball.y = HEIGHT/2 - 10
        pygame.time.delay(400)
        sound2.play()

    if ball.colliderect(player) or ball.colliderect(bot):
        ball_move_x *= -1
        sound.play()

def player_movement():
    player.y += player_move
    if player.top <= 0:
        player.top = 0
    if player.bottom >= HEIGHT:
        player.bottom = HEIGHT

    pygame.draw.rect(surface, 'black', player)

def bot_movement():
    if bot.top <= 0:
        bot.top = 0
    if bot.bottom >= HEIGHT:
        bot.bottom = HEIGHT

    if bot.top < ball.y:
        bot.y += bot_move
    if bot.bottom > ball.y:
        bot.y -= bot_move

    pygame.draw.rect(surface, 'black', bot)

def game_menu():
    global intro_loop, game_loop, end_loop

    while intro_loop:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == KEYDOWN:
                if event.key == K_SPACE:
                    intro_loop = False
                    game_loop = True

        surface.fill(background_color)
        surface.blit(intro_img, intro_img_rect)
        surface.blit(press_img, press_img_rect)
        pygame.display.update()
        clock.tick(FPS)

def game_end():
    global intro_loop, game_loop, end_loop
    if player_score >= 10:
        game_loop = False
        while end_loop:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == KEYDOWN:
                    if event.key == K_SPACE:
                        end_loop = False       

            surface.fill(background_color)
            score('YOU WON!', font2, 'black', WIDTH/2,50)
            pygame.display.update()
            clock.tick(FPS)
    if bot_score >= 10:
        game_loop = False
        while end_loop:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == KEYDOWN:
                    if event.key == K_SPACE:
                        end_loop = False

            surface.fill(background_color)
            score('YOU LOST!', font2, 'black', WIDTH/2,50)
            pygame.display.update()
            clock.tick(FPS)

def game_main():
    global intro_loop, game_loop, end_loop
    global player_move

    while game_loop:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == KEYDOWN:
                if event.key == K_UP:
                    player_move -= 10
                if event.key == K_DOWN:
                    player_move += 10

            if event.type == KEYUP:
                if event.key == K_UP:
                    player_move += 10
                if event.key == K_DOWN:
                    player_move -= 10

        table()
        score(player_score, font, 'black', WIDTH/2 - 30,20)
        score(bot_score, font, 'black', WIDTH/2 + 30,20)
        player_movement()
        bot_movement()
        ball_movement()
        game_end()

        pygame.display.update()
        clock.tick(FPS)

game_menu()
game_main()
