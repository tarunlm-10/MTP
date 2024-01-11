import sys
import time
sys.set_int_max_str_digits(0)
from random import randint,choice,random


# Utility Functions
def is_odd(n):
    """
    check if number n is odd
    """
    if n % 2:
        return False  # odd
    else:
        return True  # even


def is_even(n):
    if n % 2 == 0:
        return True  # even
    else:
        return False  # odd


def is_even_mod(n,p):
    
    if (n % p) % 2 == 0:
        return True
    else:
        return False
    

# Pulic_Key Cryptography Class
''' return a pair of public key -pk
    and private key - p'''
class PublicKey:
    def __init__(self, lambda_):
        # constrains for secure encryption
        self.rho = lambda_  # bit-length of noise
        self.rho_ = 2 * lambda_  # convenient parameter for what ?
        self.eta = lambda_ ** 2  # bit-length of secret key
        self.gama = lambda_ ** 5  # bit-length of integers in the public key
        self.tau = self.gama + lambda_  # number of integers in the public key
        self._lambda = lambda_  # security parameter
        self.p = None
        self.pk = None

    def __str__(self):
        """
        make Key objects printable
        """
        return "bit-length of noise: {}\n" \
               "bit-length of secret key: {}\n" \
               "bit-length of integers in public key: {}\n" \
               "number of integers in public key: {}\n" \
               "helper parameter p': {}\n".format(self.rho, self.eta, self.gama, self.tau, self.rho_)

    # generate private key
    def _private_key(self):
        while True:
            key = randint(2 ** (self.eta - 1), (2 ** self.eta) - 1)
            if is_odd(key):
                break
        self.p = key
        return key

    # generate public key
    def _public_key(self):
        
        while True:
            x = []
            for i in range(0, self.tau + 1):
                q = randint(0, ((2 ** self.gama) // self.p) - 1)   # <----- fix division overflow
                r = randint(-(2 ** self.rho) - 1, (2 ** self.rho) - 1)
                x.append((self.p * q) + r)

            x.sort(reverse=True)  # max element is in 0 index

            if x[0] != max(x):  # sanity check
                raise ValueError("x[0] isn't max element")

            if is_odd(x[0]) and is_even_mod(x[0], self.p):
                break
        self.pk = x
        return x

    #return the generated key pair
    def keygen(self, save=False, verbose=False):
        
        return self._private_key(), self._public_key()

    def get_public_key(self):
        return self.pk

    def get_private_key(self):
        return self.p
    


# Class defined for DGHV scheme


class DGHV:
    def __init__(self, security_param, public_key=None, private_key=None):
        self.security_param = security_param

        # total complexity of encryption homomorphic encryption O(L^10)

        self.rho = security_param  # bit-length of noise
        self.rho_ = 2 * security_param  # convenient parameter for what ?
        self.eta = security_param ** 2  # bit-length of secret key
        self.gama = security_param ** 5  # bit-length of integers in the public key
        self.tau = self.gama + security_param  # number of integers in the public key
        if public_key is not None and private_key is not None:
            self.p = private_key
            self.pk = public_key
        else:
            res = self.key_gen()
            self.p = res[0]
            self.pk = res[1]

    def key_gen(self):
        key = PublicKey(lambda_=self.security_param)
        p, pk = key.keygen(save=False, verbose=False)
        return p, pk

    def encrypt(self, m):   
        subset_size=randint(1,self.tau)
        subset=[]
        for _ in range(subset_size):
            temp=randint(1,self.tau)
            subset.append(self.pk[temp])

        r=randint(-(2**self.rho_),2**self.rho_ )    #noise
        # print(r,sum_S)
        c = (m + 2*r + 2*(sum(subset)))%self.pk[0]
        return c

    def reduce(self, c):
        return c % self.pk[0]
    
    def noise(self,c):
        return c % self.p

    def decrypt(self, c):
        return (c % self.p) % 2
    
if __name__=="__main__":
    lamda = int(input("Enter the security parameter(lamda):- "))
    generate_keys  = PublicKey(lamda)
    start = time.time()
    p,pk = generate_keys.keygen()
    end = time.time()
    print(f"Time for key_generation: {end-start :.2f}")
    dghv = DGHV(lamda,pk,p)

    # Function to check correctness of scheme
    def correctness():
        m=int(input("Enter the message  in --> {0,1}: "))
        start2 = time.time()
        c = dghv.encrypt(m)
        end2 = time.time()
        print(f"Time for encryption: {end2-start2 :.6f}")
        print("Ciphertext is - ",c)
        start3 = time.time()
        m_ = dghv.decrypt(c)
        end3 = time.time()
        print(f"Time for decryption: {end3-start3 :.6f}")
        print("Ciphertext after decryption :-",m_)
        if m_== m:
            print("--------Scheme Works Correctly--------")
        else:
            print("-------Incorrect Decryption--------")

    print("Checking correctness of the scheme \n")
    correctness()

    #function to show the somewhat homomorphic properties of the DGHV scheme
    def homomorphism():
        print("Proving the homomorphic propertirs of the scheme")
        print("Enter the messages:")
        m1 = int(input("m1:- "))
        m2 = int(input("m2:- "))
        
        c1 = dghv.encrypt(m1)
        c2 = dghv.encrypt(m2)
        # print(f"ciphertext c1 is {c1} \n \n Ciphertext c2 is {c2}")

        # Homomorphim over addition operation
        print(" Showing Additive Homomorphism of the Scheme (m1+ m2) == D(c1+c2):")
        print(f"m1 + m2 is {(m1+m2) % 2}")
        print("Decrypting c1 + c2 ")
        t1=time.time()
        c3 = c1 + c2
        # checkNoise(c3,p)
        # print(noise_flag)
        
        m_add = dghv.decrypt(c3)
        print(f"m_add is {m_add}")
        print("The DGHV scheme is homomorphic over addition:- ",end="")
        if ((m1+m2) % 2 == m_add):
            print("True")
        else:
            print("False")
        t2 = time.time()
        print(f"Addition time: {t2-t1:.6f}")
        print()
        # Homomorphic over multiplication operation
        print(" Showing Multiplicative Homomorphism of the Scheme (m1*m2) == D(c1*c2):")
        print(f"m1 * m2 is {m1*m2}")
        print("Decrypting c1 * c2 ")
        t3 = time.time()
        c4 = c1*c2
        # checkNoise(c4,p)
        # print(noise_fg)
        
        m_mul = dghv.decrypt(c4)
        print(f"m_mul is {m_mul}")
        print("The DGHV scheme is homomorphic over multiplication:- ",end="")
        if (m1*m2  == m_mul):
            print("True")
        else:
            print("False")
        t4 = time.time()
        print(f"Multiplication time: {t4-t3:.6f}")
        # Checking homomorphism  over a number of messages:
        # m=[1,1]
        # prod = 1
        # total=sum(m)
        # print(total%2,prod)
        # l=len(m)
        # add=0
        # multi=1
        # for i in range(l):
        #     c=dghv.encrypt(m[i])
        #     add+=c
        #     multi*=c
        # m_add=dghv.decrypt(add)
        # m_prod = dghv.decrypt(multi)
        # print(m_add,m_prod)
        # if m_add==total%2:
        #     print(" Correct Decryption Over Addition Operation")
        # else:
        #     print(" Incorrect Decryption Over Addition Operation")
        # if m_prod == prod:
        #     print(" Correct Decryption  Over Multiplication Operation")
        # else:
        #     print(" Inorrect Decryption  Over Multiplication Operation")


    print("Enter messages to check homomo1rphism of the scheme")
    homomorphism()
