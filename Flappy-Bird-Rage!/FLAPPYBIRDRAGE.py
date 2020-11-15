import pygame , sys, random
import random

pygame.init()

#Game Environment variables
#Thanks to Clear Code for the tutorial, was able to manufacture my own spin off.

game_font = pygame.font.Font("04b_19.ttf",47)
gravity = 0.25
bird_movement = 0

score = 0
high_score = 0

programIcon = pygame.image.load('crazybird.png')

pygame.display.set_icon(programIcon)
pygame.display.set_caption("Flappy Bird Rage by Lirdi")

bg_surface = pygame.image.load("champ.jpg")
bg_surface = pygame.transform.scale2x(bg_surface)
floor_x_pos = 0
def draw_floor():
    screen.blit(floor_surface, (floor_x_pos, 900))
    screen.blit(floor_surface, (floor_x_pos + 576, 900))

def score_display():
    score_surface = game_font.render(str(int(score)),True,(255,255,255))
    score_rect = score_surface.get_rect(center = (288,100))
    screen.blit(score_surface,score_rect)

def create_pipe():
    random_pipe_pos = random.choice(pipe_height)
    bottom_pipe = pipe_surface.get_rect(midtop = (700,random_pipe_pos))
    top_pipe = pipe_surface.get_rect(midbottom = (700,random_pipe_pos - 300))
    return bottom_pipe, top_pipe

def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -= 5
    return pipes

def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= 700:
            screen.blit(pipe_surface,pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surface,False,True)
            screen.blit(flip_pipe, pipe)

def check_collision(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            bird_surface = pygame.image.load("crazybird.png")
            bird_surface = pygame.transform.scale2x(bird_surface)
            die_sound.play()
            return False

    if bird_rect.top <= -100 or bird_rect.bottom >=900:
        fall_sound.play()
        return False

    return True

def rotate_bird(bird):
    new_bird = pygame.transform.rotozoom(bird,bird_movement * 2,1)
    return new_bird

flap_sound = pygame.mixer.Sound("sfx_wing.wav")
die_sound = pygame.mixer.Sound("sfx_hit.wav")
fall_sound = pygame.mixer.Sound("sfx_die.wav")
rage = pygame.mixer.Sound("rage.mp3")
pixeltunes = pygame.mixer.Sound("pixeltunes.mp3")
floor_surface = pygame.image.load("base.png")
floor_surface = pygame.transform.scale2x(floor_surface)
screen = pygame.display.set_mode((576,1024))
clock = pygame.time.Clock()
pixeltunes.play()
bird_surface = pygame.image.load("midflap.png")
bird_surface = pygame.transform.scale2x(bird_surface)
bird_rect = bird_surface.get_rect(center=(100, 512))

pipe_surface = pygame.image.load("redpipe].png")
pipe_surface = pygame.transform.scale2x(pipe_surface)
pipe_list = []
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE,1200)

game_over_surface = pygame.transform.scale2x(pygame.image.load("message.png").convert_alpha())
game_over_rect = game_over_surface.get_rect(center =(288,512))
#pipe height
game_active = True
pipe_height = [700,280,500,330]

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                bird_movement = 0
                bird_movement -= 9

                flap_sound.play()


            if event.key == pygame.K_SPACE and game_active == False:
                game_active = True
                pipe_list.clear()
                bird_movement = 0
                bird_rect.center = (100,512)

                cc = random.randint(1,4)
                if cc == 3:
                    bird_surface = pygame.image.load("crazybird.png")
                    bird_surface = pygame.transform.scale2x(bird_surface)
                    pygame.time.set_timer(SPAWNPIPE, 700)






                floor_x_pos -= 5

        if event.type == SPAWNPIPE:
            pipe_list.extend(create_pipe())


    screen.blit(bg_surface,(0,0))
    if game_active:

        bird_movement += gravity
        bird_rect.centery += bird_movement
        game_active = check_collision(pipe_list)
        rotated_bird = rotate_bird(bird_surface)



        #Pipes
        pipe_list = move_pipes(pipe_list)
        draw_pipes(pipe_list)


    #floor
        screen.blit(rotated_bird,bird_rect)
    else:
        screen.blit(game_over_surface,game_over_rect)
    check_collision(pipe_list)


    floor_x_pos -= 1
    draw_floor()
    if floor_x_pos < -576:
        floor_x_pos = 0



    screen.blit(floor_surface, (floor_x_pos, 900))
    pygame.display.update()
    clock.tick(120)