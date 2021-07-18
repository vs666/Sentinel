import hashlib
from config import MAX_SPLIT_A,MAX_SPLIT_B,PRIME_GOD

def hexToInt(hs):
    return int(hs,16)

def splitHash(hash):
    '''
        This function splits the given hash into two numbers a, b
        We can manually change values of constants in config.py
    '''

    # assuming hash is a hex string without 0x in front

    a = hexToInt(hash)&((1<<32) - 1)%MAX_SPLIT_A
    b = hexToInt(hashlib.sha256(bytes(str(a)+str(hash),encoding='utf-8')).hexdigest())&((1<<32) - 1)%MAX_SPLIT_B
    return a,b

def modexponent(a,b,q=1):
    '''
        This function does a^b % q 
    '''
    val = 1
    rad = a
    while b>0:
        if b&1 == 1:
            val*=rad
            # optimize by reducing number of times we use % operation (log n)
            if val >= q and q!=1:
                val %=q
        rad*= rad
        if rad >= q & q!=1:
            rad %= q
        b>>=1
    return val



def puzzle_gen(email,pass_hash):
    thex = hashlib.sha256(bytes(email+pass_hash,encoding='utf-8')).hexdigest() # get the pun ?

    a,b = splitHash(thex)
    return modexponent(a,b,PRIME_GOD)
    