import pygame
from random import randint
import time
pygame.init()
clock = pygame.time.Clock()

# some defines
WIDTH , HEIGHT = 400, 600
WHITE = (255, 255 , 255)
RED = (255, 0, 0)
BLUE = (0, 255, 0)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
FPS = 60
tube_width = 50
tube_velocity = 3
tube_gap = 150
bird_width = 35
gravity = 0.5
bird_jump = 8
score = 0
running = True
playing = False
pausing = False

# define some texts
font = pygame.font.SysFont('sans', 20)
score_txt = font.render("Score : " + str(score), True, BLACK)
game_over_txt = font.render("GAME OVER , Score : " + str(score), True, BLACK)
press_enter_txt = font.render("Press C To Continue ", True, BLACK)

# draw the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")

# draw all tubes
class Tube:
    def __init__(self, screen, color, tube_x , tube_y):
        self.screen = screen
        self.color = color
        self.tube_x = tube_x
        self.tube_y = tube_y
        self.tube_height = randint(100,400)
        self.dx = 0
        self.show()
        self.tube_pass = False

    def show(self): # draw tubes and inverse tubes
         pygame.draw.rect(self.screen, self.color, (self.tube_x, self.tube_y, tube_width, self.tube_height))
         pygame.draw.rect(self.screen, self.color, (self.tube_x, self.tube_height+tube_gap, tube_width, HEIGHT-self.tube_height-tube_gap))

    def start_play(self): # press p lead to tube move
        self.dx = tube_velocity

    def update(self): # re-draw tubes after go out of screen
        self.tube_x -=self.dx
        if self.tube_x< -tube_width:
            self.tube_x = 550
            self.tube_height = randint(100, 400)
            self.tube_pass = False

# draw the bird
class Bird:
    def __init__(self, screen, color, bird_x, bird_y):
        self.screen = screen
        self.color = color
        self.bird_x = bird_x
        self.bird_y = bird_y
        self.bird_drop =0
        self.state ='stopped'

    def show(self):
        screen.blit(flappy_image,(self.bird_x, self.bird_y))

    def jump(self): # bird jump when press p key
        self.bird_drop += gravity
        self.bird_y+=self.bird_drop
        if self.state == 'up':
            self.bird_y-=bird_jump


# import the background and the bird
background_image = pygame.image.load("background.jpg")
flappy_image = pygame.image.load("flappy.png")
flappy_image = pygame.transform.scale(flappy_image,(bird_width,bird_width))

# draw the screen
def update_screen():
    screen.fill(WHITE)
    screen.blit(background_image,(0,0))
    pygame.draw.rect(screen, YELLOW, (0, 550, 400, 50))

# draw bird rectangle and update flappy bird over bird rectangle
update_screen()
bird = Bird(screen , RED ,50, 300)
bird.show()


# draw tubes and inverse tubes
tube1 = Tube(screen, BLUE , 400, 0)
tube2 = Tube(screen, BLUE , 600, 0)
tube3 = Tube(screen, BLUE , 800, 0)

# main loop
while running:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p and pausing == False: # press p key to begin game
                tube1.start_play()
                tube2.start_play()
                tube3.start_play()
                playing = True

            if event.key == pygame.K_SPACE and playing == True and pausing == False: # press Space Key for bird jump
                bird.bird_drop = 0
                bird.bird_drop -=2
                bird.state ='up'
            if event.key ==pygame.K_c: # press c key for continue again after fail
                if pausing: # reset all when press c key
                    update_screen()
                    bird.bird_y = 300
                    tube_velocity = 3
                    tube1.tube_x = 400
                    tube2.tube_x = 600
                    tube3.tube_x = 800
                    score = 0
                    bird.show()
                    pausing = False

    if playing:  # after press p key , game will start as below
        update_screen()
        bird.show()
        bird.jump()
        tube1.update()
        tube2.update()
        tube3.update()
        tube1.show()
        tube2.show()
        tube3.show()

        # count score each pass the tube
        if tube1.tube_x + tube_width <= bird.bird_x and tube1.tube_pass == False:
            score += 1
            tube1.tube_pass = True
        if tube2.tube_x + tube_width <= bird.bird_x and tube2.tube_pass == False:
            score += 1
            tube2.tube_pass = True
        if tube3.tube_x + tube_width <= bird.bird_x and tube3.tube_pass == False:
            score += 1
            tube3.tube_pass = True
        screen.blit(score_txt, (5, 5))

        # check collision
        for tube in [tube1, tube2, tube3]:
            if (bird.bird_y < tube.tube_height) and (tube.tube_x + tube_width > bird.bird_x + bird_width > tube.tube_x):
                bird.bird_drop = 0
                tube_velocity = 0
                playing = False
                screen.blit(game_over_txt, (50, 300))
                screen.blit(press_enter_txt, (50, 350))
                pausing = True
                screen.blit(game_over_txt,(50,300))
                screen.blit(press_enter_txt,(50,350))
            if (bird.bird_y + bird_width > tube.tube_height + tube_gap) and (bird.bird_x + bird_width > tube.tube_x):
                bird.bird_drop = 0
                tube_velocity = 0
                playing = False
                screen.blit(game_over_txt, (50, 300))
                screen.blit(press_enter_txt, (50, 350))
                pausing = True
                screen.blit(game_over_txt,(50,300))
                screen.blit(press_enter_txt,(50,350))

    pygame.display.update()
pygame.quit()