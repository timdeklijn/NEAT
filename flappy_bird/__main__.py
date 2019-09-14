# NN inputs:
# bird.y
# pipe.x
# pipe.y_top
# pipe.y_bottom

import sys
import pygame

import config
from bird import Bird
from pipe_list import PipeList

# Setup screen
pygame.init()
screen = pygame.display.set_mode((config.WIDTH, config.HEIGHT))
# Game variables
bird = Bird(color=config.BIRD_COLOR)
p = PipeList()
update_mouse = True

# Start game loop
while 1:
    # Make sure pygame quits on signal
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

    # Check there is jump input or not
    if pygame.mouse.get_pressed()[0] and update_mouse:
        bird.jump()
        update_mouse = False
    else:
        bird.fall()
        update_mouse = True

    bird.check_alive() # Bird hits top or bottom of screen
    bird.is_alive *= p.no_collision(bird)
    # Update bird if it is alive
    if bird.is_alive:
        pipe_info = p.update()
        bird.update(pipe_info)
    else:
        pygame.time.wait(500)
        bird = Bird(color=config.BIRD_COLOR)
        p = PipeList()

    # Draw, and wait
    screen.fill(config.BACKGROUND_COLOR)
    p.draw(screen)
    bird.draw(screen)
    pygame.display.flip()
    pygame.time.wait(16)
