import keras
import gc
import os
import pygame
import numpy as np
import copy

from bird import Bird
import config

class BirdList():

    def __init__(self):
        self.bird_image = pygame.image.load(os.path.join("flappy_bird", "images", "fish.png"))
        self.alive = [Bird(image=self.bird_image) for _ in range(config.BIRD_NR)]
        self.dead = []
        self.max_score = 0

    def update(self, pipe_info):
        for b in self.alive:
            b.update(pipe_info)

    def draw(self, screen):
        for b in self.alive:
            b.draw(screen)

    def check_alive(self, pipe_list):
        for i in range(len(self.alive)-1, -1, -1):
            b = self.alive[i]
            if pipe_list.check_collision(b) or b.check_off_screen():
                self.dead.append(self.alive[i])
                self.alive.pop(i)

    def mutate(self, weights_list):
        chance = 0.05
        mutate_range = 0.1
        new_weights_list = []
        for weights in weights_list:
            new_weights = []
            for w in weights:
                rand_weights = (np.random.random(size=w.shape) - 0.5) * mutate_range
                w = np.where(np.random.random(size=w.shape) < chance, w, w + rand_weights)
                new_weights.append(w)
            new_weights_list.append(new_weights)
        return new_weights_list

    def next_generation(self):
        self.dead.sort(key=lambda b: b.score, reverse=True)
        print(f"Max score: {self.dead[0].score}")
        weights_list = []
        weights_list = [np.array(l.get_weights()) for l in self.dead[0].model.layers]
        self.alive.append(self.dead[0])
        self.max_score = self.alive[0].score
        self.alive[0].reset_bird()
        for b in self.dead[1:]:
            bird_weights_list = self.mutate(weights_list)
            b.change_weights(bird_weights_list)
            b.reset_bird()
            self.alive.append(b)
        self.dead = []

