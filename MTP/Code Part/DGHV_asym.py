import random
from random import randint,choice
import time 
import sys
sys.set_int_max_str_digits(0)

# Utility Functions
def is_odd(n):
    """
    check if number n is odd
    :param n:
    :return: if is odd return True, otherwise return False
    """
    if n % 2 == 0:
        return False  # even
    else:
        return True  # odd


def is_even(n):
    if n % 2 == 0:
        return True  # even
    else:
        return False  # odd


def is_even_mod(n,p):
    """
    check if number n mod p is even
    :param n:
    :param p:
    :return: return True if n mod p is even
    """
    if (n % p) % 2 == 0:
        return True
    else:
        return False
# This is our asymmetric key generation function

def secret_key(eta):
    while True:
        p = random.randint(2**(eta-1),(2**eta) -1)
        if p%2==1:
            break
    return p

# Function to generate our public-key

def public_key_generation(p,gamma,rho,tau):
    
    while True:
        x = []
        for i in range(0,tau + 1):
            q = randint(0, ((2**gamma) // p) - 1) 
            r = randint(-(2 ** rho) - 1, (2 ** rho) - 1)
            x.append((p * q) + r)

        x.sort(reverse=True)  # max element will come at 0 index

        if x[0] != max(x):  # sanity check
            raise ValueError("x[0] isn't max element")

        if is_odd(x[0]) and is_even_mod(x[0], p):
            break
    pbk = x
    return pbk
   

# This is our encryption function to encrypt message m ->{0,1}
def encrypt(m,pbk,tau,rho_):
    # subset_size = randint(1, tau)
    # subset_count = 0
    # subset = []
    # while subset_count < subset_size:
    #     subset.append(choice(pbk))
    #     subset_count += 1

    # r = randint(-(2 ** rho_), 2 ** rho_) 
    # return (m + 2*r + 2*sum(subset)) % pbk[0]

    #generate subsets
    subset_size=random.randint(1,tau)
    subset=[]
    for i in range(1,subset_size+1):
        temp=random.randint(1,tau)
        subset.append(pbk[temp])

    new_rho=rho_
    r=random.randint(-(2**new_rho),2**new_rho -1)    #noise
    # print(r,sum_S)
    c = (m + 2*r + 2*(sum(subset)))%pbk[0]
    return c

# This is our decryption function
def decrypt(c,p):
    m = (c % p) % 2
    return m

def checkNoise(c,p):
    noise = c % p
    print("Noise - ",noise)
    if noise > p//2:
        print("Noise level high , decryption will fail")

def message_to_bits(message):
    """
    convert a list of numbers (plaintext) to a list of bits to encrypt
    :param message:
    :return: type list, list of bits
    """
    message_bits = []
    for number in message:
        bits = "{0:b}".format(number)
        for bit in list(bits):
            message_bits.append(int(bit))
    return message_bits


# Function to show correctness of the scheme
def correctness():
    m = int(input("Enter the message(Note-m->{0,1}) :- "))
    lamda = int(input("Enter the security parameter (lamda) :- "))
    eta = lamda**2   #key size in bits
    gamma = lamda**5
    rho = lamda
    rho_ = 2*lamda
    tau = gamma+lamda
    start= time.time()
    p = secret_key(eta)   #asymmetric key
    print("secret key:",p)
    # print("Tau",tau)
    pbk=public_key_generation(p,gamma,rho,tau)
    end= time.time()
    # print(pbk[0])
    print("KeyGen time", end-start)
    c = encrypt(m,pbk,tau,rho_)
    print("Ciphertext is ", c)
    m_dash = decrypt(c,p)
    print(f"Ciphertext after decryption is {m_dash}")
    if m==m_dash:
        print("--------------The scheme works correctly--------------")
    else:
        print("--------Incorrect Decryption of message---------")
    print()

print("Enter message to check correctness of the scheme")
correctness()

# function to show the somewhat homomorphic properties of the DGHV scheme
# def homomorphism():
#     print("Proving the homomorphic propertirs of the scheme")
#     print("Enter the messages:")
#     m1 = int(input("m1:- "))
#     m2 = int(input("m2:- "))
#     n = int(input("Key Size :- "))  #key size in bits
#     p = secret_key(n)   #asymmetric key
#     tau=int(input("Number of integers  public key:"))
#     pbk=key_generation(p,n,tau)
#     c1 = encrypt(m1,pbk,tau,n,p)
#     c2 = encrypt(m2,pbk,tau,n,p)
#     print(f"ciphertext c1 is {c1} and ciphertext c2 is {c2}")

#     # Homomorphim over addition operation
#     print(" Showing Additive Homomorphism of the Scheme (m1+ m2) == D(c1+c2):")
#     c3 = c1 + c2
#     checkNoise(c3,p)
#     # print(noise_flag)
#     print(f"m1 + m2 is {(m1+m2) % 2}")
#     print("Decrypting c1 + c2 ")
#     m_add = decrypt(c3,p)
#     print(f"m_add is {m_add}")
#     print("The DGHV scheme is homomorphic over addition:- ",end="")
#     if ((m1+m2) % 2 == m_add):
#         print("True")
#     else:
#         print("False")
#     print()
#     # Homomorphic over multiplication operation
#     print(" Showing Multiplicative Homomorphism of the Scheme (m1*m2) == D(c1*c2):")
#     c4 = c1*c2
#     checkNoise(c4,p)
#     # print(noise_fg)
#     print(f"m1 * m2 is {m1*m2}")
#     print("Decrypting c1 * c2 ")
#     m_mul = decrypt(c4,p)
#     print(f"m_mul is {m_mul}")
#     print("The DGHV scheme is homomorphic over multiplication:- ",end="")
#     if (m1*m2  == m_mul):
#         print("True")
#     else:
#         print("False")

# print("Enter messages to check homomo1rphism of the scheme")
# homomorphism()





