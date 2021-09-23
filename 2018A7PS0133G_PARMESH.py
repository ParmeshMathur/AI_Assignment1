from random import randint, sample
from numpy.core.fromnumeric import size
from CNF_Creator import *
import numpy as np
import copy
import time
import sys
import os
import threading
from collections import deque

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
    return child

def reproduce(xarr, yarr):
    n = randint(0,len(xarr)-1)
    o = randint(0,1)
    # append beginning substring of one to ending one of another
    if(o==1):
        xtemp = xarr[:n]
        ytemp = yarr[n:]
    else:
        xtemp = yarr[:n]
        ytemp = xarr[n:]
    child = np.concatenate((xtemp, ytemp))

    # with some random prob (1 in 10), mutate child
    prob = randint(0,9)
    if prob==0:
        child = mutate(child)

    return child

def randomGenerate(n):
    ones = np.ones(n, dtype=int)
    narr = []
    while len(narr)<20:
        c = randint(0,n)
        ind = sample(range(n), c)
        arr = ones.copy()
        for j in ind:
            arr[j] = -1
        # append if new one is unique
        uni = True
        for j in range(len(narr)):
            if(np.array_equal(narr[j], arr)):
                uni = False
                break
        if(uni==True):
            narr.append(arr)
    return narr

class basicGA:
    opt_sol = np.empty(50, dtype = int)
    # TODO: make an init function?
    # TODO: make a function that calls timelimit and gen_algo_basic
    def timelimit(self):
        time.sleep(45)
        print(self.opt_sol)
        # TODO: make a proper timelimit function
        # os._exit(1)

    def gen_algo_basic(self,sentence):
        narr = []
        fitness = np.empty(50, dtype = float)
        stagfact = 0
        # generate first 20 different random states in narr
        narr = randomGenerate(50)
        n=0 # number of iterations. To be used in code to check stagnation
        while True:
            # newnarr = np.empty(dtype = int)
            newnarr = []
            best_fit = np.empty(50, dtype = int)
            for i in range(30):
                # print(i)
                x = randint(0,len(narr)-1)
                y = randint(0,len(narr)-1)
                while y==x:
                    y = randint(0,len(narr)-1)
                child = reproduce(narr[x],narr[y])
                # append child to newnarr
                # temp = len(newnarr)
                # newnarr = np.insert(newnarr, temp, child, axis=0)
                newnarr.append(child)
            narr = newnarr.copy()
            narr = sorted(narr, key = lambda arr: fitness_func(sentence, arr), reverse=True)
            narr = narr[:20]
            if(fitness_func(sentence, narr[0]) == 100):
                return narr[0]
            if(fitness_func(sentence, narr[0]) > fitness_func(sentence, best_fit)):
                best_fit = narr[0].copy()
            
            # for i in range(len(narr)):
            #     if(fitness_func(sentence, narr[i]) == 100 ):
            #         return narr[i]
            #     if(fitness_func(sentence, narr[i]) > fitness_func(sentence, best_fit)):
            #         best_fit = narr[i].copy()
            if(fitness_func(sentence, best_fit) > fitness_func(sentence, self.opt_sol)):
                self.opt_sol = best_fit.copy()
            n+=1
            n%=50
            # check if algo has stagnated
            if fitness_func(sentence, best_fit)-fitness[n] <= 5: #difference in current fitness and fitness 50 iterations ago
                if stagfact >=50: # stagnant for past 50 iterations (assumed stagnated)
                    break
                else: # stagnated for a while but not enough to assign stagnated
                    fitness[n] = fitness_func(sentence, best_fit)
                    stagfact += 1
            else:
                fitness[n] = fitness_func(sentence, best_fit)
                stagfact = max(0, stagfact-10) # decrease stagnation factor to give more time to stagnate
        return self.opt_sol


def main():
    cnfC = CNF_Creator(n=50) # n is number of symbols in the 3-CNF sentence
    sentence = cnfC.CreateRandomSentence(m=120) # m is number of clauses in the 3-CNF sentence
    # TODO: also do for m = 160, 200, 240, 300
    print('Random sentence : ',sentence)
    print()
    tbegin = time.perf_counter()
    bga = basicGA()
    best_sol = bga.gen_algo_basic(sentence)
    tend = time.perf_counter() - tbegin
    best_fitness = fitness_func(sentence, best_sol)
    for i in range(50):
            best_sol[i]*=(i+1)
    print('Best solution model: ', best_sol)
    print()
    print('Fitness of model: ', best_fitness)
    print()
    print('Time taken: ', tend)

    # sentence = cnfC.ReadCNFfromCSVfile()
    # print('\nSentence from CSV file : ',sentence)

#    print('\n\n')
#    print('Roll No : 2020H1030999G')
#    print('Number of clauses in CSV file : ',len(sentence))
#    print('Best model : ',[1, -2, 3, -4, -5, -6, 7, 8, 9, 10, 11, 12, -13, -14, -15, -16, -17, 18, 19, -20, 21, -22, 23, -24, 25, 26, -27, -28, 29, -30, -31, 32, 33, 34, -35, 36, -37, 38, -39, -40, 41, 42, 43, -44, -45, -46, -47, -48, -49, -50])
#    print('Fitness value of best model : 99%')
#    print('Time taken : 5.23 seconds')
#    print('\n\n')
    
if __name__=='__main__':
    main()