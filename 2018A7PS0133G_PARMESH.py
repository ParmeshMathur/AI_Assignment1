from random import randint, sample, choice
from numpy.core.fromnumeric import size
import numpy as np
import time
import threading
import itertools
import csv

optimal_solution = np.empty(50, dtype=int)

class CNF_Creator:
    def __init__(self,n): #n is number of symbols
        self._n = n
        self._sentence = None

    def _CreateAClause(self):
        n = self._n
        claus = sample(range(1,n+1),3)
        for i in range(3):
            claus[i] = -claus[i] if choice(range(2))==0 else claus[i]
            #above statement randomly negates some of the literals in the clause
        claus.sort()
        return claus

    def CreateRandomSentence(self,m): #m is number of clauses in the sentence
        n = self._n
        clauses = list()
        while len(clauses)<m:
            for mi in range(len(clauses),m):
                claus = self._CreateAClause()
                clauses.append(claus)
            clauses.sort()
#            print(clauses,len(clauses))
            clauses = list(clause for clause,_ in itertools.groupby(clauses)) # removes duplicate clauses
#            print(clauses,len(clauses))
            self._sentence = clauses
        return self._sentence
    
    def ReadCNFfromCSVfile(self):
        with open('CNF.csv') as csvfile:
            rows = csv.reader(csvfile)
            rows = list(rows)
        sentence = [[int(i) for i in ro] for ro in rows]
        return sentence


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
    while len(narr)<30:
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


class modifiedGA:
    opt_sol = np.empty(50, dtype = int)

    def genetic_algo_modified(self,sentence):
        narr = []
        fitness = np.empty(50, dtype = float)
        stagfact = 0
        # generate first 30 different random states in narr
        narr = randomGenerate(50)
        n=0 # number of iterations. To be used in code to check stagnation

        while True:
            newnarr = []
            best_fit = np.empty(50, dtype = int)
            for i in range(50):
                # print(i)
                x = randint(0,len(narr)-1)
                y = randint(0,len(narr)-1)
                while y==x: # make sure both parents are different
                    y = randint(0,len(narr)-1)
                child = reproduce(narr[x],narr[y])
                # append child to newnarr
                newnarr.append(child)
            narr = newnarr.copy()
            narr = sorted(narr, key = lambda arr: fitness_func(sentence, arr), reverse=True)
            narr = narr[:30] # sort with fitness function and choose 30 best

            if(fitness_func(sentence, narr[0]) == 100):
                self.opt_sol = narr[0]
                break
            best_fit = narr[0].copy()
            
            if(fitness_func(sentence, best_fit) > fitness_func(sentence, self.opt_sol)):
                self.opt_sol = best_fit.copy()
                
            # check if algo has stagnated
            n+=1
            n%=50
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
    print('Roll No : 2018A7PS0133G\n')
    # print('This program generates a random sentence of arbitrary length chosen from [100,120,140...280,300].\n')
    # print('The best solution (model) for that sentence is then obtained.\n')

    # sentence_length = list(range(100,300,20))
    # l = choice(sentence_length)
    # print('Length of random sentence : ', l)
    # print()
    cnfC = CNF_Creator(n=50) # n is number of symbols in the 3-CNF sentence
    # sentence = cnfC.CreateRandomSentence(m=l) # m is number of clauses in the 3-CNF sentence
    # print('Random sentence : ',sentence)
    sentence = cnfC.ReadCNFfromCSVfile()
    print('Number of clauses read : ',len(sentence))
    print()

    tbegin = time.perf_counter()
    mga = modifiedGA()
    best_sol = mga.genetic_algo_modified(sentence)
    tend = time.perf_counter() - tbegin
    best_fitness = fitness_func(sentence, best_sol)

    for i in range(50):
            best_sol[i]*=(i+1)
    print('\nBest solution model found: ', best_sol)
    print('\nFitness of model: ', best_fitness)
    print('\nTime taken: ', tend)
    print()
    
if __name__=='__main__':
    main()