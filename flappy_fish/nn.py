import numpy as np
from keras.models import Sequential, clone_model
from keras.layers import Dense, Activation
from keras.optimizers import Adam

class NN():

    def __init__(self):
        pass


    def create_NN(self):
        """Create neural network

        Create and compile a model and save it in:
        self.model
        """
        self.model = Sequential()
        # outputs a layer with 7*[21] weights
        self.model.add(Dense(8, input_dim=4, activation="relu"))

        # =====================================================================
        #
        # Add aditional layers, or not
        #
        # =====================================================================

        self.model.add(Dense(1, input_dim=16, activation="softplus"))
        self.model.compile(loss="categorical_crossentropy",
                           optimizer=Adam(),
                           metrics=["accuracy"])


    def mutate(self, weights_list):
        """
        Mutate weights somehow.

        :param weights_list: list of weights
        :returns: weight_list with modified values
        """
        new_weights_list = weights_list

        # =====================================================================
        #
        # Mutate the weights 
        #
        # =====================================================================

        return new_weights_list


    def change_weights(self, weights):
        """Replace weights in self.model with weights"""
        for i, layer in enumerate(self.model.layers):
            layer.set_weights(weights[i])


    def next_generation(self):
        """
        Create the next generation by:
            * finding the fittest fish in self.dead (list of fish)
            * Extract the weights of the fish that need to reproduce
            * Mix/Mutate the weights and set weights to next generation
            * For all fish, run fish_reset()
            * Append all changed fish to self.alive (list of fish)
            * empty self.dead (list of fish)
        """

        # =====================================================================
        #
        # Currently the whole next generation gets the weights of the 
        # fittest fish. Mutate/mix weights to evolve the next generation
        #
        # =====================================================================

        # Sort fish on score
        self.dead.sort(key=lambda b: b.score, reverse=True)
        # Extract all weights from the fittest fish
        weights_list = []
        weights_list = [np.array(l.get_weights()) for l in self.dead[0].model.layers]
        # Let the fittest fish live, and reset it
        self.alive.append(self.dead[0])
        self.max_score = self.alive[0].score
        self.alive[0].reset_fish()
        # Mutate the weights of the fittest fish and spread over the population
        for b in self.dead[1:]:
            fish_weights_list = self.mutate(weights_list)
            b.change_weights(fish_weights_list)
            # Reset all fish
            b.reset_fish()
            self.alive.append(b)
        # update dead list
        self.dead = []

