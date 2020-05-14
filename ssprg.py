import random
import typing
import marshal
import pickle
from secrets import randbelow

def listToInt(_list):
    return int("".join(map(lambda x: str(x), _list)) , 2)

def intToList(_int, pad = 0):
    _list = list(map(lambda x: int(x), "{0:b}".format(_int)))

    if (pad == 0 or len(_list) >= pad):
        return _list

    _list = [0] * (pad - len(_list) ) +_list

    return _list

# seed = seed, prg = prg function, n = n-wise composition parameter
def BlumMicali(seed, prg, n:int):
    result = []
    si = seed
    for i in range(n):
        ri, si = prg(si)
        result += ri
    result += si
    return result

# seed = seed, prg = prg function
# this function will return the result of the prg using the seed
# and a new random seed from the seed space
def SubsetSumPRGExtension(seed , prg):
    result = prg(seed)
    new_seed = [randbelow(2) for i in range(len(seed))]
    return (result, new_seed)

# SubsetSum - function, n - how many time to be parallelised
# def ParallelSubsetSum(SubsetSum, n:int, seed_length:int):


# generator; q should be  n = length of seed
def SubsetSumPRGFamily(q:int, n:int):
    a = [randbelow(q) for a_ix in range(n)]
    def SubsetSumPRG(seed):
        result = 0
        for i in range(n):
            result += (a[i]*seed[i]) % q
        result %= q
        return result

    return SubsetSumPRG


####### utils for saving the  generated prg #######
# path = disk path where to save function. prg = prg function to be saved
def savePRG(path, prg):
    with open(path, 'wb') as filehandler:
        pickle.dump(prg, filehandler)

# path = disk path from where to load function
def loadPRG(path):
    filehandler = open(path, 'rb')
    function = pickle.load(filehandler)
    return function

n = 40
s = [0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1,
 0, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 1, 0]
 
def pickler():
    saveprg('newprg.func', SubsetSumPRGFamily(2**(2*n), n))

def test():
    pickler()
    newG = loadprg('newprg.func')
    # print(G(s))
    print(newG(s))


# ''' Choosing an n and q so that 2n = log2(q) gives a prg whose output is twice
# the size of the input. '''
# def SubsetSumprg(seed, q, a):
#     n = len(seed)
#     q = 2**(2*n)
#     result = 0
#     for ix_bit in range(n):
#         result += (a[ix_bit] * seed[ix_bit])%q
#     result = intToList(result)
#     new_seed = intToList(listToInt(seed)^listToInt(result[:n+1]))
#     return result, new_seed
#
# s = [random.randint(0,1) for i in range(40)]
#
# print(SubsetSumprg(s))
