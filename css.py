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
        b = s[ -1 - v[0] ]
        for j in v[1:]:
            b ^= s[-1 - j]
        s = [ b ] + s[:-1]
    return (result, s)

def listToInt(_list):
    return int("".join(map(lambda x: str(x), _list)) , 2)

def intToList(_int, pad = 0):
    _list = list(map(lambda x: int(x), "{0:b}".format(_int)))

    if (pad == 0 or len(_list) >= pad):
        return _list

    _list = [0] * (pad - len(_list) ) +_list

    return _list

def carry(int1, int2):
    if (int1 + int2) > 255:
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
        z += intToList( (xi + yi + c) % 256, pad = 8)
        c = carry(xi, yi)
    return z

def nBitGenerator(n):
    result = []
    for b in itertools.product("01", repeat = n):
        result.append(list(map(lambda x: int(x), ''.join(b))))
    return result

def createS():
    return [random.randint(0,1) for i in range(40)]

# s_test = [0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 1, 0, 1, 1, 1, 0, 0, 1, 1, 1,
# 0, 1, 0, 1, 1, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 0, 0]

s_test = [0] * 40


def deCSS():
    v17 = [14, 0]
    v25 = [12, 4, 3, 0]
    z = CSS(s_test, 100)
    z_atk = z[16:] + z[8:16] + z[:8] # 2**16 z3 + 2**8 z2 + z1

    xp = LFSR([1] + s_test[:16], v17, 24)[0]
    x = xp[16:] + xp[8:16] + xp[:8]

    y = (listToInt(z_atk) - listToInt(x)) % (2**24) # 2**16 y3 + 2**8 y2 + y1
    y = intToList(y, pad = 24)
    y = y[16:] + y[8:16] + y[:8]

    yp = LFSR([1] + s_test[16:], v25, 24)[0]



    print("x:\n{}\n{}\n{}".format(s_test[:16], xp, x))
    print("y:\n{}\n{}\n{}".format(s_test[16:], yp, y))
    # bx = nBitGenerator(16)
    # for s1 in bx:
    #     s2 = []
    #
    #     x = LFSR(s1, v17, 8*3)[0]
    #     x = x[16:] + x[8:16] + x[:8] # 2**16 x3 + 2**8 x2 + x1
    #
    #     y = listToInt(z_atk) - listToInt(x)
    #     y = y % (2**24)
    #     y = intToList(y, pad = 24) # 2**16 y3 + 2**8 y2 + y1
    #     y1 = y[16:]; y1.reverse()
    #     y2 = y[8:16]; y2.reverse()
    #     y3 = y[:8]; y3.reverse()
    #     s2 = y1 + y2 + y3
    #
    #     s = s1 + s2
    #
    #     print ("Trying seed: " + "".join(map(lambda x: str(x), s)) )
    #
    #     zp = CSS(s, 100)
    #
    #     if z == zp:
    #         return "Found: {}.\n Used seed: {}".format(s, s_test)

    return "Error, seed was not found."


        # s2.append(y[16:] + y[8:16] + y[:8])
        # s2.append(
        # intToList((listToInt(y[16:])-1)%2**8, pad = 8) + y[8:16] + y[:8]
        # )
        # s2.append(
        # y[16:] + intToList((listToInt(y[8:16])-1)%2**8, pad = 8) + y[:8]
        # )
        # s2.append(
        # y[16:] + y[8:16] + intToList((listToInt(y[:8])-1)%2**8, pad = 8)
        # )
        # s2.append(
        # intToList((listToInt(y[16:])-1)%2**8, pad = 8) +
        # intToList((listToInt(y[8:16])-1)%2**8, pad = 8) + y[:8]
        # )
        # s2.append(
        # intToList((listToInt(y[16:])-1)%2**8, pad = 8) + y[8:16] +
        # intToList((listToInt(y[:8])-1)%2**8, pad = 8)
        # )
        # s2.append(
        # y[16:] + intToList((listToInt(y[8:16])-1)%2**8, pad = 8) +
        # intToList((listToInt(y[:8])-1)%2**8, pad = 8)
        # )
        # s2.append(
        # intToList((listToInt(y[16:])-1)%2**8, pad = 8) +
        # intToList((listToInt(y[8:16])-1)%2**8, pad = 8) +
        # intToList((listToInt(y[:8])-1)%2**8, pad = 8)
        # )
        #
        # for s2p in s2:
        #     s = s1 + s2p
        #     print ("Trying seed: " + "".join(map(lambda x: str(x), s)) )
        #     zp = CSS(s, 100)
        #
        #     if z == zp:
        #         return "Found: {}.\n Used seed: {}".format(s, s_test)


print(deCSS())
