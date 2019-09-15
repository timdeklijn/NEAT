import pygame
import gc
import numpy as np
from keras.models import Sequential, clone_model
from keras.layers import Dense, Activation
from keras.optimizers import Adam

import config

class Bird():
    """
    Bird class, predict action, update position and
    draw the bird.
    """

    def __init__(self, color):
        """
        :param color: rgb bird color
        """
        self.color = color
        self.x = 2 * config.CIRCLE_RADIUS
        self.y = int(config.HEIGHT/2.0)
        self.radius = config.CIRCLE_RADIUS
        self.gravity_force = config.GRAVITY / config.BIRD_MASS
        self.velocity = 0
        self.acceleration = 0
        self.score = 0
        self.create_NN()


    def create_NN(self):
        """Create neural network"""
        self.model = Sequential()
        # outputs a layer with 7*[21] weights
        self.model.add(Dense(8, input_dim=4, activation="relu"))
        # outputs a layer wit 32*[1] weights
        self.model.add(Dense(16, input_dim=8, activation="relu"))
        self.model.add(Dense(1, input_dim=16, activation="softplus"))
        self.model.compile(loss="categorical_crossentropy",
                           optimizer=Adam(),
                           metrics=["accuracy"])


    def change_weights(self, weights):
       for i, layer in enumerate(self.model.layers):
            layer.set_weights(weights[i])


    def reset_bird(self):
        self.y = int(config.HEIGHT/2.0)
        self.velocity = 0
        self.score = 0


    def draw(self, screen):
        """
        Draw the bird object to the screen

        :param screen: pygame screen object
        """
        pygame.draw.circle(
            screen,
            self.color,
            (self.x, self.y),
            self.radius,)


    def check_off_screen(self):
        """
        Check if bird position is off screen

        :retrun: boolean, True when off screen
        """
        if self.y - self.radius <= 0 or self.y + self.radius >= config.HEIGHT:
            return True


    def update(self, pipe_info):
        """
        predict action based on environment input, then
        update acceleration, velocity and finally, bird position.

        :param pipe_info: tuple with environment variables
        """
        # Create NN input
        # x, y, y
        nn_input = np.array([[self.y] + [i for i in pipe_info]], dtype=np.float32)
        nn_input[0,1] = self.x - nn_input[0,1]
        nn_input[0,2] = self.y - nn_input[0,2]
        nn_input[0,3] = self.y - nn_input[0,3]
        # Based on NN output, jump or not
        if self.model.predict(nn_input)[0,0] > 0.5 and self.velocity >= 0.0:
            self.acceleration += config.JUMP_FORCE
        else:
            self.acceleration += self.gravity_force
        # Set new position
        self.velocity += self.acceleration
        self.y += int(self.velocity)
        self.acceleration = 0
        self.score += 1
