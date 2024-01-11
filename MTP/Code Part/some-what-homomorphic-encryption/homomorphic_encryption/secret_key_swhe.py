# -*- coding: utf-8 -*-
import sys
sys.path.append('..')
from keys.secret_key import SecretKey
from random import randint
from math import sqrt

class secret_swhe:
    def __init__(self, lambda_, secret_key=None, eta=10):
        self.lambda_ = lambda_
        self.eta = eta
        if secret_key is None:
            self.p = self._key_gen(eta)
        else:
            self.p = secret_key

    def _key_gen(self, eta):
        k = SecretKey(eta)
        return k.key_gen()

    def encrypt(self, m):
        while True:
            r = randint(round(2 ** (sqrt(self.eta) - 1)), round(2 ** sqrt(self.eta)) + 1)
            if abs(2 * r) < self.p / 2:  # this must hold to find q
                break
        q = randint(2 ** ((self.eta ** 3) - 1), 2 ** (self.eta ** 3))
        return self.p * q + 2 * r + m

    def decrypt(self, c):
        return (c % self.p) % 2
    
ob=secret_swhe(4,None,10)
c=ob.encrypt(0)
m_=ob.decrypt(c)
print(m_)
