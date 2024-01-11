import sys
sys.set_int_max_str_digits(0)
from random import randint,choice,random
import random 
import gmpy2
import math
from decimal import Decimal,getcontext


getcontext().prec = 6
# Utility Functions
def is_odd(n):
    """
    check if number n is odd
    """
    if n % 2 == 0:
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


def NearestInteger(a,b):
  "Gives the nearest integer to a/b"
  return (2*a+b)//(2*b)


def modNear(a,b):
  "Computes a mod b with a \in ]-b/2,b/2]"
  return a-b*NearestInteger(a,b)
    

''' Class that will generate new public key private key pair'''
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
        self.sk_new = None
        self.pk_new = None


    # generate private key
    def _private_key(self):
        while True:
            key = randint(2 ** (self.eta - 1), (2 ** self.eta) - 1)
            if is_odd(key):
                break
        self.p = key
        return self.p

    # generate public key
    def _public_key(self):
        rho_mul = 2 ** self.rho
        temp = ((2 ** self.gama) // self.p)
        while True:
            x = []
            for i in range(0, self.tau + 1):
                q = randint(0, temp - 1)   # <----- fix division overflow
                r = randint(-rho_mul - 1, rho_mul - 1)
                x.append((self.p * q) + r)

            x.sort(reverse=True)  # max element is in 0 index

            if x[0] != max(x):  # sanity check
                raise ValueError("x[0] isn't max element")

            if is_odd(x[0]) and is_even_mod(x[0], self.p):
                break
        self.pk = x
        return x

    def theta_hamming_vector(self,big_theta):

        # Create a vector with theta bits initialized to 0
        vector = [0] * big_theta
        S = set()
        small_theta = self._lambda-1
        # Set _lambda random positions to 1
        ones_indices = random.sample(range(big_theta-1), small_theta)
        for index in ones_indices:
            vector[index] = 1
            S.add(index)
        vector[big_theta-1]=1 #added last index to create the hamming weight
        return vector,S

    #return the generated key pair
    def keygen(self, save=False, verbose=False):
        
        return self._private_key(), self._public_key()
    
    def KeyGen(self):
        self.p,self.pk = self.keygen()
        kappa = self.gama + 2
        big_theta  = kappa*self._lambda
        x_p = NearestInteger(2**kappa,self.p)
        s,S = self.theta_hamming_vector(big_theta)
        u=[0]*big_theta
        mod = 2**(kappa+1)
        while True:
            for i in range(big_theta-1):
                u[i] = randint(0,mod)

            sum_u_i = 0
            for i in S:
                sum_u_i+=u[i]

            temp = (x_p) - (sum_u_i % mod)
            if temp<0:
                u[big_theta-1] = mod + temp
            elif temp>0:
                u[big_theta-1] = temp
            else:
                u[big_theta-1] = 0

            sum_u_i+=u[big_theta-1]

            if sum_u_i % mod == x_p % mod:
                print("Squashing Succesfull")
                break

        y = [0]*big_theta
        for i in range(big_theta):
            cal_yi = u[i]/(2**kappa)
            y[i] = round(cal_yi,4)
            # print(type(y[i]))

        self.pk_new = (self.pk,y)
        self.sk_new = s
        return self.p,self.pk,self.sk_new,self.pk_new
            
    def get_public_key(self):
        return self.pk

    def get_private_key(self):
        return self.p

class DGHV:
    def __init__(self, security_param):
        self._lambda = security_param

        # total complexity of encryption homomorphic encryption O(L^10)

        self.rho = security_param  # bit-length of noise
        self.rho_ = 2 * security_param  # convenient parameter for what ?
        self.eta = security_param ** 2  # bit-length of secret key
        self.gama = security_param ** 5  # bit-length of integers in the public key
        self.tau = self.gama + security_param  # number of integers in the public key
        res = self.key_gen()
        self.p = res[0]
        self.pk = res[1]
        self.sk_new = res[2]
        self.pk_new = res[3]
        print("x0 :",self.pk[0])

    def key_gen(self):
        key = PublicKey(lambda_=self._lambda)
        p, pk, sk_new, pk_new = key.KeyGen()
        return p, pk, sk_new, pk_new
    
    def get_keys(self):
        return self.p, self.pk, self.sk_new, self.pk_new

    def encrypt(self, m, pk_new):   
        y = pk_new[1]
        # print(y)
        subset_size=randint(1,self.tau)
        subset=[]
        for _ in range(subset_size):
            temp=randint(1,self.tau)
            subset.append(self.pk[temp])

        r=randint(-(2**self.rho_),2**self.rho_ )    #noise
        # print(r,sum_S)
        c_star = (m + 2*r + 2*(sum(subset)))%self.pk[0]
    
        kappa = self.gama + 2
        big_theta  = kappa*self._lambda
        z = [0]*big_theta

        for i in range(big_theta):
            zi = ((c_star % 2) * (y[i] - y[i]//2 * 2)) % 2
            # print(zi)
            z[i] = round(zi,4)
        # print(z)
        return c_star,z

    def reduce(self, c):
        return c % self.pk[0]
    
    def noise(self,c):
        return c % self.p

    def decrypt(self,sk_new, c):
        temp = 0
        for s_i,z_i in zip(sk_new,c[1]):
            temp+=s_i*z_i
        # print(temp,type(temp))
        res = int(temp+ float(0.5))

        return (c[0]- res) % 2
    


if __name__ == "__main__":
    
    lamda = int(input("Enter the security parameter(lamda):- "))
    dghv = DGHV(lamda)
    p,pk,sk_new,pk_new = dghv.get_keys()
    print(p)
    
    def correctness():
        m=int(input("Enter the message  in --> {0,1}: "))
        c = dghv.encrypt(m,pk_new)
        print("Ciphertext is - ",c[0])
        m_ = dghv.decrypt(sk_new,c)
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
        # lamda = int(input("Enter the security parameter(lamda):- "))
        # generate_keys  = PublicKey(lamda)
        # p,pk = generate_keys.keygen()
        # dghv = DGHV(lamda,pk,p)
        c1 = dghv.encrypt(m1,pk_new)
        c2 = dghv.encrypt(m2,pk_new)
        print(f"ciphertext c1 is {c1} \n \n Ciphertext c2 is {c2}")

        # Homomorphim over addition operation
        print(" Showing Additive Homomorphism of the Scheme (m1+ m2) == D(c1+c2):")
        c3 = c1[0] + c2[0]
        c3 = (c3,c1[1])
        # checkNoise(c3,p)
        # print(noise_flag)
        print(f"m1 + m2 is {(m1+m2) % 2}")
        print("Decrypting c1 + c2 ")
        m_add = dghv.decrypt(sk_new,c3)
        print(f"m_add is {m_add}")
        print("The DGHV scheme is homomorphic over addition:- ",end="")
        if ((m1+m2) % 2 == m_add):
            print("True")
        else:
            print("False")
        print()
        # Homomorphic over multiplication operation
        print(" Showing Multiplicative Homomorphism of the Scheme (m1*m2) == D(c1*c2):")
        c4 = c1[0]*c2[0]
        c4 = (c4,c1[1])
        # checkNoise(c4,p)
        # print(noise_fg)
        print(f"m1 * m2 is {m1*m2}")
        print("Decrypting c1 * c2 ")
        m_mul = dghv.decrypt(sk_new, c4)
        print(f"m_mul is {m_mul}")
        print("The DGHV scheme is homomorphic over multiplication:- ",end="")
        if (m1*m2  == m_mul):
            print("True")
        else:
            print("False")

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
    # print(sk_new)

