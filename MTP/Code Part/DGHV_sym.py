import random
import gmpy2

# This is our symmetric key generation function
def Keygeneration(n):
    p = random.randrange(2**(n-1),2**n)
    if p%2==0:
        p+=1
    return p


#Function to generate random numbers
def random_numbers(p,n):
    q=random.randrange(2**(n-1),2**n)
    r=random.randrange(3,p//4 - 1)
    return q,r

# This is our encryption function to encrypt message m ->{0,1}
def encrypt(m,p,n):
    q,r = random_numbers(p,n)  #random numbers
    print(p,r)
    c = q*p + 2*r + m
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
# Function to show correctness of the scheme
def correctness():
    m = int(input("Enter the message(Note-m->{0,1}) :- "))
    # m2 = int(input())
    n = int(input("Key Size :- "))  #key size in bits
    p = Keygeneration(n)   #symmetric key
    c = encrypt(m,p,n)
    print(f"Ciphertext is {c}")
    # c2 = encrypt(m2,p,q,r)
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
def homomorphism():
    print("Proving the homomorphic propertirs of the scheme")
    print("Enter the messages:")
    m1 = int(input("m1:- "))
    m2 = int(input("m2:- "))
    n = int(input("Key Size :- "))  #key size in bits
    p = Keygeneration(n)   #symmetric key
    c1 = encrypt(m1,p,n)
    c2 = encrypt(m2,p,n)
    print(f"ciphertext c1 is {c1} and ciphertext c2 is {c2}")

    # Homomorphim over addition operation
    print(" Showing Additive Homomorphism of the Scheme (m1+ m2) == D(c1+c2):")
    c3 = c1 + c2
    checkNoise(c3,p)
    # print(noise_flag)
    print(f"m1 + m2 is {(m1+m2) % 2}")
    print("Decrypting c1 + c2 ")
    m_add = decrypt(c3,p)
    print(f"m_add is {m_add}")
    print("The DGHV scheme is homomorphic over addition:- ",end="")
    if ((m1+m2) % 2 == m_add):
        print("True")
    else:
        print("False")
    print()
    # Homomorphic over multiplication operation
    print(" Showing Multiplicative Homomorphism of the Scheme (m1*m2) == D(c1*c2):")
    c4 = c1*c2
    checkNoise(c4,p)
    # print(noise_fg)
    print(f"m1 * m2 is {m1*m2}")
    print("Decrypting c1 * c2 ")
    m_mul = decrypt(c4,p)
    print(f"m_mul is {m_mul}")
    print("The DGHV scheme is homomorphic over multiplication:- ",end="")
    if (m1*m2  == m_mul):
        print("True")
    else:
        print("False")

print("Enter messages to check homomo1rphism of the scheme")
homomorphism()




