import tensorflow as tf
import keras
from keras import layers
import numpy as np
from matplotlib import pyplot as plt
import pandas as pd
import pygame
pygame.init()

import Game_model_version

width = 600
height = 600
window = pygame.display.set_mode((width,height))


def make_model(initializer):
    FNNmodel = keras.Sequential(
        [
            keras.Input(shape = 7),
            layers.Dense(10, activation = "relu", name = "layer1", kernel_initializer = initializer),
            layers.Dense(3, name = "output")
        ])

    return FNNmodel


initializer = tf.keras.initializers.HeNormal(seed = 1)
fitness = []

for i in range(10):
        model = make_model(initializer)
        print(model.predict(np.array([[1,1,1,1,1,1,1]])))
        fitness.append(Game_model_version.Game(window,model))

print(fitness)