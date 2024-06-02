import tensorflow as tf
import keras
from keras import layers
import numpy as np
from matplotlib import pyplot as plt
import pandas as pd
import pygame
pygame.init()
import random

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
models = []
best_models = []

for i in range(10):
        model = make_model(initializer)
        models.append(model)


#fitness = Game_model_version.Game(window,models)
print(fitness)
print("")  

def score(fitness_values):
    """
    takes in a list of fitness values, returns the indeces of the two best models
    """

    scores = []
    for model_data in fitness_values:
        scores.append(1000*int(model_data[0]) + model_data[1] - model_data[2] - 500*(int(model_data[3])))
    idx1 = np.argmax(scores)
    scores = np.delete(scores,idx1)
    idx2 = np.argmax(scores)

    return [idx1,idx2]


def mutate(models):
    mutated = []
    for model in models:
         weights = model.get_weights()
         for i in range(4):
              for weight in weights[i]:
                   if random.choice([0,1]):
                        weight += random.normalvariate(0,.2)
         model.layers[0].set_weights(weights[0:2])
         model.layers[1].set_weights(weights[2:4])
         mutated.append(model)
    return mutated
        

def propagate(model1,model2,no_of_children):
    weights = model1.get_weights()+model2.get_weights()

    children = []
    for i in range(no_of_children):
         model = make_model(initializer)

         L1 = []
         L1.append(weights[random.choice([0,4])])
         L1.append(weights[random.choice([0,4])+1])
         model.layers[0].set_weights(L1)
    
         L2 = []
         L2.append(weights[random.choice([2,6])])
         L2.append(weights[random.choice([2,6])+1])
         model.layers[1].set_weights(L2)
         children.append(model)

    return children



while len(best_models) > 2: # if more than 2 models find a solution, find the best 2
    max_val, ind = -1,0     
        
    for i in range(len(best_models)):
        if best_models[i][2] > max_val:
            max_val, ind = best_models[i][2], i
    
    del best_models[ind]
    

if len(best_models) < 2:  # other cases: 0 models solve, 1 model solves (find two models where kirby survives longest)
    if len(best_models) == 0:
        max_val, ind = -1,0
        
        for i in len(fitness):
            if fitness[i][2] > max_val:
                max_val, ind = fitness[i][2], i
                
        best_models.append(fitness[i])
        del fitness[i]
        
    max_val, ind = -1,0
        
    for i in len(fitness):
        if fitness[i][2] > max_val:
             max_val, ind = fitness[i][2], i
                
    best_models.append(fitness[i])
        
print(best_models) 

#GENERATION LOOP:
generations = 10
best_of_gen = []
parents = []
for i in range(generations):
    fitness = Game_model_version.Game(window,models+parents)
    parent_ids = score(fitness)
    parents = [models[parent_ids[0]],models[parent_ids[1]]]
    best_of_gen.append(models[parent_ids[0]])
    children = propagate(models[parent_ids[0]], models[parent_ids[1]], 10)
    models = mutate(children)


