import random
from secrets import randbelow

def listToInt(_list):
    return int("".join(map(lambda x: str(x), _list)) , 2)

def intToList(_int, pad = 0):
    _list = list(map(lambda x: int(x), "{0:b}".format(_int)))

    if (pad == 0 or len(_list) >= pad):
        return _list

    _list = [0] * (pad - len(_list) ) +_list

    return _list

''' Choosing an n and q so that 2n = log2(q) gives a PRG whose output is twice
the size of the input. '''
def SubsetSumPRG(seed):
    n = len(seed)
    q = 2**(2*n)
    result = 0
    a = [randbelow(q) for a_ix in range(n)]
    for ix_bit in range(n):
        if seed[ix_bit]==1:
            result += (a[ix_bit] * seed[ix_bit])%q
    result = intToList(result)
    new_seed = intToList(listToInt(seed)^listToInt(result[:n+1]))
    return result, new_seed

s = [random.randint(0,1) for i in range(40)]

print(SubsetSumPRG(s))
