from secrets import randbelow
import datetime
import json

def dump_json(path, var):
    with open(path, 'w') as fh:
        json.dump(var, fh)

def load_json(path):
    with open(path, 'r') as fh:
        return json.load(fh)


def listToInt(_list):
    return int("".join(map(lambda x: str(x), _list)) , 2)

def intToList(_int, pad = 0):
    _list = list(map(lambda x: int(x), "{0:b}".format(_int)))

    if (pad == 0 or len(_list) >= pad):
        return _list

        _list = [0] * (pad - len(_list) ) +_list

        return _list

def seed_prg(seed):
    n = 256
    q = 2**(2*256)
    a = load_json('a_seed')
    result = 0
    for i in range(n):
        result += (a[i]*seed[i]) % q
    result %= q
    return intToList(result, pad = n)[:n]

def my_prg(seed, bytes):
    n = 256
    q = 2**(2*256)
    a = load_json('a_prg')
    def prg(seed, n):
        result = 0
        for i in range(n):
            result += (a[i]*seed[i]) % q
        result %= q
        return result
    result = []
    si = seed
    while (bytes>0):
        prgOutput = intToList(prg(si, n), pad = n)
        result += prgOutput
        si = seed_prg(si)
        bytes -= (len(prgOutput))/8
    result += si
    return result

# create seed:
def new_seed(_len):
    return [randbelow(2) for i in range(_len)]

# create vector a:
def create_a(q,n):
    return [randbelow(q) for a_ix in range(n)]

def test(debug = False):
    seed = load_json('test_seed')
    result = my_prg(seed, 2048), len(my_prg(seed, 2048))
    print(result)
    if (debug):
        data = {"date": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        "result": result}
        dump_json('debug', data)

test(True)
