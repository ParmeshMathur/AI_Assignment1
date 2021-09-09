from numpy.core.fromnumeric import size
from CNF_Creator import *
import numpy as np
import copy

def fitness_func():
    val = 0
    return val

def reproduce():
    # x = random selection from narr
    # y = random selection from narr that is not x
    # n = random length from 0 to len(x)
    # append beginning substring of x to ending one of y
    child = np.array([1,2,3,4,5,6,7,8,9,10])
    return child

def gen_algo_basic():
    # generate numpy array of 20 arrays
    narr = np.empty([20,50], dtype = int)
    n=20
    # generate 20 different states in narr
    opt_sol = np.empty(50, dtype = int)
    while True:
        newnarr = np.empty(shape = narr.shape, dtype = int)
        for i in range(n):
            print(i)
            # x = random selection from narr
            # y = random selection from narr that is not x
            # child = reproduce(x,y)
            # with some random prob, mutate child
            # append child to newnarr
        # narr = copy.copy(newnarr)
        
        for i in range(n):
            if(fitness_func(narr[i]) == 100 ):
                return narr[i]
            if(fitness_func(narr[i]) > fitness_func(opt_sol)):
                opt_sol = copy.copy(narr[i])
    return opt_sol


def main():
    cnfC = CNF_Creator(n=50) # n is number of symbols in the 3-CNF sentence
    sentence = cnfC.CreateRandomSentence(m=120) # m is number of clauses in the 3-CNF sentence
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