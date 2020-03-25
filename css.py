import itertools
import random
def LFSR(s, v, l):
    if max(v) > len(s):
        raise Exception("tap position greater than length of seed")
    if min(v) < 0:
        raise Exception("tap position must be positive")
    result = []
    for i in range (0, l):
        result.append(s[-1])
        b = s[ -1 - v[0] ] # in loc de s [v[0]]
        for j in v[1:]:
            b ^= s[-1 - j] # in loc de s[j]
        s = [ b ] + s[:-1]
    return (result, s)

def listToInt(_list):
    return int("".join(map(lambda x: str(x), _list)) , 2)

def intToList(_int, pad = 0):
    _list = list(map(lambda x: int(x), "{0:b}".format(_int)))

    if (pad == 0 or len(_list) >= pad):
        return _list
    while (len(_list) < pad):
        _list.insert(0, 0)
    return _list

def carry(int1, int2):
    if (int1 + int2)>255:
        return 1
    return 0

def CSS(s, l):
    v17 = [14, 0]
    v25 = [12, 4, 3, 0]
    if len(s) != 40:
        raise Exception("Seed must be of length 40.")
    s1 = s[:16]
    s2 = s[16:]
    s2.insert(0, 1)
    s1.insert(0, 1)
    c = 0
    z = []
    for i in range(0, l):
        xi, s1 = LFSR(s1, v17, 8)
        yi, s2 = LFSR(s2, v25, 8)
        xi = listToInt(xi)
        yi = listToInt(yi)
        z += intToList( (xi + yi + c) % 256 )
        c = carry(xi, yi)
    return z

def nBitGenerator(n):
    result = []
    for b in itertools.product("01", repeat=n):
        result.append(list(map(lambda x: int(x), ''.join(b))))
    return result

def createS():
    return [random.randint(0,1) for i in range(40)]

s_test = [0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 1, 0, 1, 1, 1, 0, 0, 1, 1, 1,
0, 1, 0, 1, 1, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 0, 0]



def deCSS():
    v17 = [14, 0]
    v25 = [12, 4, 3, 0]
    z = CSS(s_test, 100)
    z1 = listToInt(z[:8])
    z2 = listToInt(z[8:16])
    z3 = listToInt(z[16:24])
    bx = nBitGenerator(16)
    z_list = []
    for s1 in bx:
        s2 = []
        x = LFSR(s1, v17, 8*3)[0]
        x1 = listToInt(x[:8])
        x2 = listToInt(x[8:16])
        x3 = listToInt(x[16:])
        s = s1 + s2
        print ("Trying seed: " + "".join(map(lambda x: str(x), s)) )
        zp = CSS(s, 100)
        if z == zp:
            # print("Found the seed: " + "".join(map(lambda x: str(x), s)))
            # print ("Seed to be recovered: " + "".join(map(lambda x: str(x), s_test)) )
            # print(z)
            # print(zp)
            # z_list.append(s)
            return "Found: {}.\n Used seed: {}".format(s, s_test)
    return s_test in s



# print(CSS(s_test, 100))

# print(deCSS())
