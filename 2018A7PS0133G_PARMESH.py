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

# TODO: put everthing in a class

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
    # for i in range(20):
    # c = randint(1,n)
    # ind = sample(range(1,n), c)
    # arr = ones.copy()
    # for j in ind:
    # arr[j] = -1

class basicGA:
    opt_sol = np.empty(50, dtype = int)
    
    def timelimit(self):
        time.sleep(45)
        print(self.opt_sol)
        # os._exit(1)

    def gen_algo_basic(self,sentence):
        # generate numpy array of 20 arrays
        narr = np.empty([20,50], dtype = int)
        best_fit = np.empty(50, dtype = int)
        fitness = np.empty(50, dtype = float)
        stagfact = 0
        # TODO: generate first 20 different random states in narr
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
                # append child to newnarr
                temp = len(newnarr)
                newnarr = np.insert(newnarr, temp, child, axis=0)
            narr = newnarr.copy()
            
            for i in range(len(narr)):
                if(fitness_func(sentence, narr[i]) == 100 ):
                    return narr[i]
                if(fitness_func(sentence, narr[i]) > fitness_func(sentence, best_fit)):
                    best_fit = narr[i].copy()
            if(fitness_func(sentence, best_fit) > fitness_func(sentence, self.opt_sol)):
                self.opt_sol = best_fit.copy()
            n+=1
            n%=50
            # check if algo has stagnated
            if abs(fitness[n]-fitness_func(sentence, best_fit))<=1:
                if stagfact >=50:
                    break
                else:
                    stagfact += 1
            else:
                stagfact = max(0, stagfact-5)
        return self.opt_sol


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