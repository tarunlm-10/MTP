# -*- coding: utf-8 -*-
import sys
sys.path.append('..')
sys.set_int_max_str_digits(0)
from random import randint, choice
from keys.public_key import PublicKey


class SWHE:
    def __init__(self, security_param, public_key=None, private_key=None):
        self.security_param = security_param
        # total complexity of encryption homomorphic encryption O(L^10)
        self.rho = security_param  # bit-length of noise
        self.rho_ = 2 * security_param  # convenient parameter for what ?
        self.eta = security_param ** 2  # bit-length of secret key
        self.gama = security_param ** 5  # bit-length of integers in the public key
        self.tau = self.gama + security_param  # number of integers in the public key
        if public_key is not None and private_key is not None:
            self.sk = private_key
            self.pk = public_key
        else:
            res = self.key_gen()
            self.sk = res[0]
            self.pk = res[1]

    def key_gen(self):
        key = PublicKey(lambda_=self.security_param)
        sk, pk = key.keygen(save=False, verbose=False)
        return sk, pk

    def encrypt(self, m):
        subset_size = randint(1, self.tau)
        subset_count = 0
        subset = []
        while subset_count < subset_size:
            subset.append(choice(self.pk))
            subset_count += 1

        r = randint(-(2 ** self.rho_), 2 ** self.rho_)
        return (m + 2 * r + 2 * sum(subset)) % self.pk[0]

    def reduce(self, c):
        return c % self.pk[0]

    def decrypt(self, c):
        return (c % self.sk) % 2
l=int(input())
ob=SWHE(l,None,None)
m=int(input())
c=ob.encrypt(m)
print("Ciphertext is ",c)
m_=ob.decrypt(c)
print(m_)