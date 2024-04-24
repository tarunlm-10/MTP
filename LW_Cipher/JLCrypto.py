import gmpy2
import random
import time
from crypto import *


class JoyeLibert(object):
    [p, q, n, y, k] = [0]*5
    [priv, pub] = [None]*2
    def __init__(self, kappa):
    #Given the security parameter kappa, choose a k>=1.
        self.k = 128
        self.kappa = kappa
        #Randomly generate primes p,q = 1 mod 2^k. N = pq.
        self.p = self.generate_prime_1mod2k()
        self.q = self.generate_prime_1mod2k()
        self.n = self.p * self.q
        #Pick y \in J_n \ QR_N.
        self.y = self.generate_y()

    class PrivateKey(object):
        def __init__(self, p):
            self.p = p
        def __str__(self):
            return "PrivateKey\n P = " + str(self.p)
    
    class PublicKey(object):
        def __init__(self, n, y, k):
            self.n = n
            self.y = y
            self.k = k
            #The following value does not need to be in
            #the public key, but it’s done as an optimization.
            self.p2k = pow(2,self.k)
        def __str__(self):
            return "PublicKey\n N = " + str(self.n) + "\n Y = "\
            + str(self.y) + "\n K = " + str(self.k)
        
    """ Change public and private keys for the given ones. """
    def change_keys(self, priv, pub):
        self.priv = priv
        self.pub = pub


    def generate_keypair(self):
        self.priv = self.PrivateKey(self.p)
        self.pub = self.PublicKey(self.n, self.y, self.k)
        return self.priv, self.pub
    
    """
    Encrypts a message m seen as an integer in [0,2^k-1].
    """
    def encrypt(self, m):
        p2 = self.pub.p2k #This is pow(2,self.pub.k)
        if (m >= p2):
            print("Error, message should be in [0,2^k-1].")
            return None
        x = random.randrange(1, self.pub.n)
        c = (self.mpow(self.pub.y,m, self.pub.n) * self.mpow(x,p2, self.pub.n))%self.pub.n
        return c
    

    def decrypt(self, c):
        p = self.priv.p
        k = self.pub.k
        y = self.pub.y
        m = 0
        B = 1
        D = pow(y, -(p-1)//(2**k), p)
        # print("D:",D)
        C = pow(c, (p-1)//(2**k), p)
        # print("C:",C)

        for j in range(1, k):
            z = pow(C, 2**(k-j), p)
            if z != 1:
                m += B
                C = (C * D) % p
            B *= 2
            D = pow(D, 2, p)

        if C != 1:
            m += B

        return m
    
    """ Add two encrypted messages. """
    def add(self, a, b):
        return (a * b) % self.pub.n
        
    #Mathematic methods

    """ 
    Returns the result of modular exponentiation
    a^b (mod m)
    """
    def mpow(self,a,b,m):
        ans=1
        while b > 0:
            if b & 1:
                ans = (ans * a) % m
            b = b >> 1
            a  = (a * a) % m
        return ans
    

    """ Check for primality using Miller - Rabin
        i.e determines whether n is likely to be prime"""

    def miller_rabin(self,n, t):

        assert(n % 2 == 1)
        assert(n > 4)
        assert(t >= 1)

        # select n - 1 = 2**s * r
        r, s = n - 1, 0
        while r % 2 == 0:
            s += 1
            r >>= 1 #r = (n - 1) / 2 ** s

        for i in range(t):
            a = random.randint(2, n - 2) # this requires n > 4

            y = pow(a, r, n) # python has built-in modular exponentiation
            if y != 1 and y != n - 1:
                j = 1
                while j <= s - 1 and y != n - 1:
                    y = pow(y, 2, n)
                    if y == 1:
                        return False
                    j += 1
                if y != n - 1:
                    return False

        return True
    

    """determines if n is  prime"""
    def is_probably_prime(self,n):
        
        if n in [2, 3]:
            return True
        if n % 2 == 0:
            return False

        return self.miller_rabin(n, 10)

    """
    Returns a probable prime p of self.k bits, such that
    p = 1 mod 2^k
    """
    def generate_prime_1mod2k(self):
        p2 = pow(2,self.k)
        start_time = time.time()
        x = 1
        it = 0
        while not self.is_probably_prime(p2*x+1):
            x=random.randrange(1, p2)
            it += 1
        goal_time = time.time()
        print("Running time (random[1,2^k) approach):", (goal_time-start_time))
        print("Iterations =", it)
        print(self.k, x, p2*x+1)
        return p2*x+1
    

    """
    Returns the n-th power residue symbol modulo p, p being a prime.
    The absolute small residue of a^{(p-1)/n} modulo p.
    For n=2:
        # 1 if a is a quadratic residue modulo p.
        # -1 if a is a quadratic non-residue modulo p.
    """

    def legendre_symbol(self, a, p, n):
        if (p-1)%n != 0:
            print("Error calculating legendre_symbol for", a, p, n)
            return None
        return self.mpow(a, (p-1)//n, p)
    
    
    """
    Return an y \in J_N \ QR_N.
    Which is setting n = 2 and requesting
    # symbol(y/p)*symbol(y/q) = 1
    # But not satisfying symbol(y/p) = symbol(y/q) = 1
    Which yields to symbol(y/p) = symbol(y/q) = -1
    """
    def generate_y(self):
        y = 1
        it = 0
        #If the legendre symbols are both -1, the jacobi symbol (y/N) =
        # = (y/p)*(y/q) = -1*-1 = 1.
        while self.legendre_symbol(y, self.p, 2) != self.p-1 or \
            self.legendre_symbol(y, self.q, 2) != self.q-1:
            y = random.randrange(1, self.n)
            it += 1
        print("Found y after", it, "iterations. y =", y)
        return y
    

if __name__ == "__main__":
    obj = JoyeLibert(128)
    sk,pk = obj.generate_keypair()
    m = int(input("Enter an integer:- "))
    ctx = obj.encrypt(m)
    c1 = (ctx**1000)%pk.n
    print("Ciphertext is: ",ctx)
    print(obj.decrypt(c1))
    ptx = obj.decrypt(ctx)
    print("Message after decryption:",ptx)
    if ptx==m:
        print("Correct Decryption") 
    else:
        print("Incorrect Decryption")
    m1 = int(input("Enter first message: "))
    m2 = int(input("Enter seecond message: "))
    ct1 = obj.encrypt(m1)
    ct2 = obj.encrypt(m2)
    ct = obj.add(ct1,ct2)
    ans = obj.decrypt(ct)
    if ans == (m1+m2)% 2**pk.k:
        print("Scheme is additively homomorphic")
    else:
        print("Wrong")
    print(ans)

