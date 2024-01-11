import random
import gmpy2
import time
from Crypto.Util.number import getPrime

#important function definitions

def gcd(a,b):
    if b<a:
        b,a = a,b
        
    while b > 0:
        a,b = b, a%b
    return a

def lcm(a,b):
    return (a*b)//(gcd(a,b))

def compute_g(n,p,q):
    n_sq = n*n
    fi_n = gmpy2.lcm(p-1,q-1)
    g = random.randint(3,n_sq)
    # print("recurive block",g)
    if gcd(g,n_sq) != 1:
        # print("hi")
        return compute_g(n,p,q)
    else:
        # print("in else block")
        x = gmpy2.powmod(g,fi_n,n_sq)
        L = func_L(x,n)
        if gcd(n,L) == 1:
            return g
        else:
            return compute_g(n,p,q)
            # i=1
            # while i<n_sq:
            #     print(i)
            #     if gmpy2.powmod(g,i,n_sq) == 1:
            #         print("dsf",i)
            #         if i%n==0:
            #         # print(g)
            #             return g
            #     i+=1

            

# function to compute L(u) = (u-1)//n
def func_L(u,n):
    one = gmpy2.mpz(1)
    return (gmpy2.f_div(gmpy2.sub(u,one),n))

# Key Generation in Paillier cryptosystem
def key_generation(bits):
    p = getPrime(bits)
    q = getPrime(bits)
    while p == q:
        q = getPrime(bits)
    if gcd(p*q,(p-1)*(q-1)) == 1:
        n = p*q
    else:
        key_generation(bits)
    return p,q


#setup/preprocessing
a=time.time()
p,q = key_generation(128)
# p,q = 7,11
n = p*q
print(n)
g = compute_g(n,p,q)
print(g)
public_key = (n,g)
private_key = (p,q)
b=time.time()
print("keygen",b-a)


# Encryption Proces
def encrypt(m,public_key):
    n = public_key[0]
    g = public_key[1]
    # print(g)
    n_square = n*n
    if m > n:
        print("Enter different message of length less than 'n' ")
        m = int(input("Re-enter message : "))
    r = random.randint(1,n)
    while gcd(r,n)!=1:
        r = random.randint(1,n)
    cipher = gmpy2.f_mod(gmpy2.mul(gmpy2.powmod(g,m,n_square),(gmpy2.powmod(r,n,n_square))),n_square)

    # print(m)
    return cipher,m


# Decryption processs
def decrypt(c,private_key,public_key):
    p = private_key[0]
    q = private_key[1]
    n = public_key[0]
    g = public_key[1]
    n_square = n*n
    # print(n)
    fi_n = gmpy2.lcm(p-1,q-1)
    # print(fi_n,c,type(n))
    arg_c = gmpy2.powmod(c[0],fi_n,n_square)
    arg_g = gmpy2.powmod(g,fi_n,n_square)
    numerator  = func_L(arg_c,n)
    denom = func_L(arg_g,n)
    denom_inverse = gmpy2.invert(denom,n)
    # print(gcd(denom,n)==1)
    message = gmpy2.mod(gmpy2.mul(numerator,denom_inverse),n)
    return message

c=time.time()
cipher = encrypt(90,public_key)
# print(type(cipher))
d=time.time()
print(f"Encryption time: {d-c:.6f}")
print(cipher)
c=time.time()
message = decrypt(cipher,private_key, public_key)
d=time.time()
print(f"Decryption time: {d-c:.6f}")
print(message)

# Homomorphic Properties
m1 = int(input("First message : "))
m2 = int(input("Second message : "))
c1,m1= encrypt(m1,public_key)
c2,m2 = encrypt(m2,public_key)

# (i)Homomorphic over addition

print("Paillier cipher is homomorphic over addition ")
c=time.time()
ct = gmpy2.mul(c1,c2)
msg = decrypt((ct,0),private_key,public_key)

if msg == (m1+m2)%n:
    print("True")
    print(msg)
else:
    print("False")
d=time.time()
print("Add",d-c)

# (ii) Homomorphic over multilication with a scalar

# print("Raising an encrypted message to the power of a second message results in the multiplication of plaintext messages")
# ct1 = c1**m2
# msg = decrypt(ct1,private_key,public_key)

# if msg == (m1*m2)%n:
#     print("True")
#     print(msg)
# else:
#     print("False")
#     print(msg)
# temp = int(input())
# temp1= encrypt(temp,public_key)
# print(n)
# print(p,q)
# print(temp1)
# dect = decrypt(temp1,private_key, public_key)
# print(dect)

#narayanjmnnit@gmail.com

