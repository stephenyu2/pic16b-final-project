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
best_models = []

for i in range(10):
        model = make_model(initializer)
        print(model.predict(np.array([[1,1,1,1,1,1,1]])))
        fitness.append(Game_model_version.Game(window,model))
       
        if fitness[i][0] == True:
            best_models.append(fitness[i]) 

print(fitness)
print("")  

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