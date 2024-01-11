import random
import math
from math import gcd
import gmpy2
from Crypto.Util.number import getPrime
from cryptography.hazmat.primitives.asymmetric import ec
import galois
from Crypto.PublicKey import ECC


# Function to generate a prime number of a given size
def generate_primes(bits):
    p = getPrime(bits)
    q = getPrime(bits)
    while p == q:
        q = getPrime(bits)
    if gcd(p*q,(p-1)*(q-1)) == 1:
        n = p*q
    else:
        generate_primes(bits)
    return p,q

q1,q2 = generate_primes(5)
n = q1*q2
print(n)
# Function to check if a number is prime
# def is_prime(n):
#     if n == 2:
#         return True
#     if n % 2 == 0 or n == 1:
#         return False
#     for i in range(3, int(math.sqrt(n)) + 1, 2):
#         if n % i == 0:
#             return False
#     return True

# Construct Bilinear groups of order n

def bilinear(n):
    for i in range(n):
        p = i*n - 1
        if gmpy2.is_prime(p):
            if p%3 == 2:
                return p
    return 0

p = bilinear(n)
print(p)



# Generate a point of order n on the curve
G = d * E.generator() 
p2 = p**2
# Compute the bilinear pairing e(P, P)
e  = E.pairing(G, G)




#generate keys
# public_key = (n,G,G_1,e,g,h)


# Encryption function
def encrypt(msg, public_key):
    n = public_key[0]
    g = public_key[4]
    h = public_key[5]
    r = random.randrange(1,n)
    res = gmpy2.f_mod((g**msg)*(h**r),n)
    return res

# Decryption function
def decrypt(cipher,private_key,public_key):
    q = private_key
    g = public_key[4]
    temp = cipher**q
    base = g**q
    result = math.log(temp,base)
    return result