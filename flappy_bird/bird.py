import pygame
import numpy as np
from keras.models import Sequential
from keras.layers import Dense, Activation
from keras.optimizers import Adam

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
        self.create_NN()

    def create_NN(self):
        self.model = Sequential()
        # outputs a layer with 7*[21] weights
        self.model.add(Dense(32, input_dim=7, activation="relu"))
        # outputs a layer wit 32*[1] weights
        self.model.add(Dense(1, input_dim=32, activation="softmax"))

        self.model.compile(loss="categorical_crossentropy",
                           optimizer=Adam(),
                           metrics=["accuracy"])

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

    def update(self, pipe_info):
        nn_input = np.array([[self.y] + [i for i in pipe_info]])
        if self.model.predict(nn_input)[0,0] == 1.0:
            self.jump()
        self.velocity += self.acceleration
        self.y += int(self.velocity)
        self.acceleration = 0
