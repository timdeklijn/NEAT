import keras
import gc
import numpy as np

from bird import Bird
import config

class BirdList():

    def __init__(self):
        self.alive = [Bird(color=config.BIRD_COLOR) for _ in range(config.BIRD_NR)]
        self.dead = []

    def update(self, pipe_info):
        for b in self.alive:
            b.update(pipe_info)

    def draw(self, screen):
        for b in self.alive + self.dead:
            b.draw(screen)

    def check_alive(self, pipe_list):
        for i in range(len(self.alive)-1, -1, -1):
            b = self.alive[i]
            if pipe_list.check_collision(b) or b.check_off_screen():
                self.dead.append(self.alive[i])
                self.alive.pop(i)

    def mutate(self, weights_list):
        chance = 0.5
        mutate_range = 0.5
        new_weights_list = []
        for weights in weights_list:
            new_weights = []
            for w in weights:
                np.where(
                    np.random.random(size=w.shape) < chance, w,
                    np.random.random(size=w.shape) * mutate_range - (mutate_range * 2))
                new_weights.append(w)
            new_weights_list.append(new_weights)
        return new_weights_list

    def next_generation(self):
        for b in self.dead:
            weights_list = []
            for l in b.model.layers:
                weights_list.append(l.get_weights())
            weights_list = self.mutate(weights_list)
            b.change_weights(weights_list)
            b.reset_position()
            self.alive.append(b)
        self.dead = []

