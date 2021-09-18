from random import randint
from numpy.core.fromnumeric import size
from CNF_Creator import *
import numpy as np
import copy
import time
import sys
import os
import threading

# TODO: put everthing in a class

def timelimit():
    time.sleep(45)
    # print best model
    os._exit(1)

def fitness_func(sentence, model):
    sat = 0
    m = len(sentence)
    for i in range(m):
        for j in range(3):
            if sentence[i][j] * model[abs(sentence[i][j])-1] > 0:
                sat += 1
                break
    val = (sat/m)*100
    return val

def mutate(child):
    ind = randint(0,len(child)-1)
    child[ind]*=-1

def reproduce(xarr, yarr):
    n = randint(0,len(xarr)-1)
    # append beginning substring of x to ending one of y
    xtemp = xarr[:n]
    ytemp = yarr[n:]
    child = np.concatenate(xtemp, ytemp)

    # with some random prob (1 in 10), mutate child
    prob = randint(0,9)
    if prob==0:
        mutate(child)

    return child

def gen_algo_basic(sentence):
    # generate numpy array of 20 arrays
    narr = np.empty([20,50], dtype = int)
    # TODO: generate first 20 different random states in narr
    opt_sol = np.empty(50, dtype = int)
    while True:
        n=0 # number of iterations. To be used in code to check stagnation
        newnarr = np.empty(dtype = int)
        for i in range(20):
            print(i)
            x = randint(0,len(narr)-1)
            y = randint(0,len(narr)-1)
            while y==x:
                y = randint(0,len(narr)-1)
            child = reproduce(narr[x],narr[y])
            # TODO: append child to newnarr
            newnarr = newnarr.append(child)
        narr = newnarr.copy()
        
        for i in range(len(narr)):
            if(fitness_func(sentence, narr[i]) == 100 ):
                return narr[i]
            if(fitness_func(sentence, narr[i]) > fitness_func(sentence, opt_sol)):
                opt_sol = narr[i].copy()
        n+=1
        # TODO: check if algo has stagnated
    return opt_sol


def main():
    cnfC = CNF_Creator(n=50) # n is number of symbols in the 3-CNF sentence
    sentence = cnfC.CreateRandomSentence(m=120) # m is number of clauses in the 3-CNF sentence
    # TODO: also do for m = 160, 200, 240, 300
    print('Random sentence : ',sentence)

    sentence = cnfC.ReadCNFfromCSVfile()
    print('\nSentence from CSV file : ',sentence)

#    print('\n\n')
#    print('Roll No : 2020H1030999G')
#    print('Number of clauses in CSV file : ',len(sentence))
#    print('Best model : ',[1, -2, 3, -4, -5, -6, 7, 8, 9, 10, 11, 12, -13, -14, -15, -16, -17, 18, 19, -20, 21, -22, 23, -24, 25, 26, -27, -28, 29, -30, -31, 32, 33, 34, -35, 36, -37, 38, -39, -40, 41, 42, 43, -44, -45, -46, -47, -48, -49, -50])
#    print('Fitness value of best model : 99%')
#    print('Time taken : 5.23 seconds')
#    print('\n\n')
    
if __name__=='__main__':
    main()