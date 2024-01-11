# -*- coding: utf-8 -*-

from random import randint
from homomorphic_encryption.util import is_odd


class SecretKey:
    def __init__(self, eta):
        self.eta = eta
        self.sk = None

    def key_gen(self):
        """
        generate secret key p in the interval h
        p is an odd integer in the interval [2^(eta-1), 2^eta]
        :param h: interval
        :return: (int) secret key p
        """
        while True:
            sk = randint((2 ** self.eta) - 1, 2 ** self.eta)
            if is_odd(sk):
                break
        self.sk = sk
        return sk

    def get_secret_key(self):
        return self.sk