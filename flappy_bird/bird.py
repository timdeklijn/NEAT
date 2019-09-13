import pygame

import config

class Bird():
    def __init__(self, color):
        self.color = color
        self.x = 2 * config.CIRCLE_RADIUS
        self.y = int(config.HEIGHT/4.0)
        self.radius = config.CIRCLE_RADIUS
        self.gravity_force = config.GRAVITY / config.BIRD_MASS
        self.velocity = 0
        self.acceleration = 0
        self.is_alive = True

    def draw(self, screen):
        pygame.draw.circle(
            screen, 
            self.color, 
            (self.x, self.y), 
            self.radius)

    def jump(self):
        if self.velocity > 0:
            self.acceleration += config.JUMP_FORCE

    def fall(self):
        self.acceleration += self.gravity_force

    def check_alive(self):
        if self.y - self.radius <= 0 or self.y + self.radius >= config.HEIGHT:
            self.is_alive = False

    def update(self):
        self.velocity += self.acceleration
        self.y += int(self.velocity)
        self.acceleration = 0