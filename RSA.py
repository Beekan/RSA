import random
import Crypto.Util.number
import Crypto.Random


def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a 

def eea(R1,modulo):
    if(gcd(R1,modulo)!=1):
        raise Exception(f"{R1} has no inverse in modulo {modulo}")
    newR=R1
    oldR=modulo
    newT=1
    oldT=0
    while(newR%oldR!=1):
        q=int(oldR/newR)
        oldT,newT=newT,oldT-q*newT
        oldR,newR=newR,oldR-q*newR
    #This while loop is only implemented to 
    #return an inverse within the modulo range
    while(newT<0):
        newT=newT+modulo
    return newT

def sam(expBase,expPower,modulo):
    binPower=bin(expPower)[3:]
    result=expBase%modulo
    for i in binPower:
        result=(result*result)%modulo
        if i=="1":
            result=(result*expBase)%modulo
    return result

def isPrime(x):
    if sam(2,x-1,x)==1:
        return True
    else: return False
    
def primeGen(bitLength):
    #the number is ORed with 1 to generate an odd number
    #and increase the step by 2 to divide the search space by 2
    p=random.getrandbits(bitLength) | 1
    while(not isPrime(p)):
        p=random.getrandbits(bitLength) | 1
    return p
#     return Crypto.Util.number.getPrime(bitLength, randfunc=Crypto.Random.get_random_bytes)

def keyGeneration(bitLength):
    p=primeGen(bitLength)
    q=primeGen(bitLength)
    n=p*q
    phi=(p-1)*(q-1)
    e=random.randint(1,phi-1)
    while(gcd(e,phi)!=1):
        e=random.randint(1,phi-1)
    privateKey=(n,eea(e,phi))
    publicKey=(n,e)
    return publicKey,privateKey

def encryption(message,publicKey):
    return sam(message,publicKey[1],publicKey[0])

def decryption(cipher,privateKey):
    return sam(cipher,privateKey[1],privateKey[0])
