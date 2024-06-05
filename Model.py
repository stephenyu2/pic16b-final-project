import tensorflow as tf
import keras
from keras import layers
import numpy as np
from matplotlib import pyplot as plt
import pandas as pd
import pygame
import random
pygame.init()

import Game_model_version

# Customizable values on Model.py and Game_mode_version.py/Game.py

width = 600
height = 600
model_type = 2 ### SEE DISCLAIMER BELOW
models_per_gen = 10 # customizable (default: 10)
level = 5           # customizable (levels 1-5)

"""
VERY IMPORTANT: 

model_type is a variable that you can change to different integers to change the model 

Below is the legend: 
0: Inputs: Maximum (23) Layers: (23, 10, 3) with 23 being the input layer and 3 being the output layer
1: Inputs: Maximum (23) Layers: (23, 5, 5, 3) with 23 being the input layer and 3 being the output layer
"""
window = pygame.display.set_mode((width,height))


def make_model(initializer, model_type):
    
    if model_type == 0:                 # FNN with 1 layer and sightlines
        FNNmodel = keras.Sequential(
            [
                keras.Input(shape = (23,)),
                layers.Dense(10, activation = "relu", name = "layer1", kernel_initializer = initializer),
                layers.Dense(3, name = "output")
            ])
    elif model_type == 1:               # FNN with 2 layers and sightlines
        FNNmodel = keras.Sequential(
            [
                keras.Input(shape = (23,)),
                layers.Dense(5, activation = "relu", name = "layer1", kernel_initializer = initializer),
                layers.Dense(5, activation = "relu", name = "layer2", kernel_initializer = initializer),
                layers.Dense(3, name = "output")
            ])

    elif model_type == 2:
        FNNmodel = keras.Sequential(
            [
                keras.Input(shape = (23,)),
                layers.Dense(4, activation = "relu", name = "layer1", kernel_initializer = initializer),
                layers.Dense(2, activation = "relu", name = "layer2", kernel_initializer = initializer),
                layers.Dense(4, activation = "relu", name = "layer3", kernel_initializer = initializer),
                layers.Dense(3, name = "output")
            ])

    return FNNmodel


initializer = tf.keras.initializers.HeNormal(seed = 1)
fitness = []
models = []
best_models = []

for i in range(models_per_gen):
        model = make_model(initializer, model_type = model_type)
        models.append(model)


def score(fitness_values):
    """
    takes in a list of fitness values, returns the indeces of the two best models
    """

    scores = []
    for model_data in fitness_values:
        scores.append(1000*model_data[0] + model_data[1] - model_data[2] - 500*model_data[3])
    
    print(fitness_values)
    print(scores)

    idx1 = np.argmax(scores)
    print(idx1)
    scores = np.delete(scores,idx1)
    idx2 = np.argmax(scores)
    if idx2 >= idx1:
         idx2 += 1
    return [idx1,idx2]


def mutate(models):
    mutated = []
    for model in models:
        weights = model.get_weights()
        for i in range(len(weights)):
            for weight in weights[i]:
                if random.choice([0, 1]):
                    weight += random.normalvariate(0, .2)
        model.set_weights(weights)
        mutated.append(model)
    return mutated
        

def propagate(model1, model2, no_of_children, initializer, model_type):
    weights1 = model1.get_weights()
    weights2 = model2.get_weights()
    
    children = []
    for i in range(no_of_children):
        model = make_model(initializer, model_type=model_type)
        
        new_weights = []
        for j in range(len(weights1)):
            new_weights.append(random.choice([weights1[j], weights2[j]]))
        
        model.set_weights(new_weights)
        children.append(model)
    
    return children

generations = 100
best_of_gen = []
parents = []
for i in range(generations):
    fitness = Game_model_version.Game(window,models,level)
    parent_ids = score(fitness)
    parents = [models[parent_ids[0]],models[parent_ids[1]]]
    best_of_gen.append(models[parent_ids[0]])
    children = propagate(models[parent_ids[0]], models[parent_ids[1]], models_per_gen, initializer, model_type)
    models = mutate(children)+parents


