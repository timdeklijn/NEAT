import numpy as np
from keras.models import Sequential, clone_model
from keras.layers import Dense, Activation
from keras.optimizers import Adam

class NN():

    def __init__(self):
        pass


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


    def change_weights(self, weights):
       for i, layer in enumerate(self.model.layers):
            layer.set_weights(weights[i])


    def next_generation(self):
        self.dead.sort(key=lambda b: b.score, reverse=True)
        weights_list = []
        weights_list = [np.array(l.get_weights()) for l in self.dead[0].model.layers]
        self.alive.append(self.dead[0])
        self.max_score = self.alive[0].score
        self.alive[0].reset_fish()
        for b in self.dead[1:]:
            fish_weights_list = self.mutate(weights_list)
            b.change_weights(fish_weights_list)
            b.reset_fish()
            self.alive.append(b)
        self.dead = []

