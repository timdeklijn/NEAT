import sys
import pygame

# user inputs
import config
from bird import Bird
from bird_list import BirdList
from pipe_list import PipeList

# Setup screen ================================================================

pygame.init()
screen = pygame.display.set_mode((config.WIDTH, config.HEIGHT))
pygame.display.set_caption('Flappy Fish')

# Game variables ==============================================================

bird_list = BirdList()
pipe_list = PipeList()
gen_num = 1
font = pygame.font.Font("freesansbold.ttf", 20)

# Start game loop =============================================================
while 1:
    # Make sure pygame quits on signal
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

    # Update cycle ============================================================

    # check for collision or off screen
    bird_list.check_alive(pipe_list)
    # Update bird if it is alive
    pipe_info = pipe_list.update()
    bird_list.update(pipe_info)

    # Reset ===================================================================

    if len(bird_list.alive) == 0:
        # pygame.time.wait(500)
        bird_list.next_generation()
        pipe_list = PipeList()

    # Draw Frame ==============================================================

    screen.fill(config.BACKGROUND_COLOR)
    pipe_list.draw(screen)
    bird_list.draw(screen)
    text = font.render(f"gen: {gen_num} score: {bird_list.alive[0].score} ({bird_list.max_score})",
                       True, (250, 250, 200), None)
    text_rect = text.get_rect()
    text_rect.center = (config.WIDTH // 2, 30)
    screen.blit(text, text_rect)
    pygame.display.flip()
    pygame.time.wait(10)

