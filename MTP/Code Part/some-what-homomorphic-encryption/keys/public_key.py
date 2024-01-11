from random import randint
from homomorphic_encryption.util import is_odd, is_even_mod


class PublicKey:
    def __init__(self, lambda_):
        # constrains for secure encryption
        self.rho = lambda_  # bit-length of noise
        self.rho_ = 2 * lambda_  # convenient parameter for what ?
        self.eta = lambda_ ** 2  # bit-length of secret key
        self.gama = lambda_ ** 5  # bit-length of integers in the public key
        self.tau = self.gama + lambda_  # number of integers in the public key
        self._lambda = lambda_  # security parameter
        self.sk = None
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

    def _private_key(self):
        """
        generate a private key
        :return: a private key
        """
        while True:
            key = randint(2 ** (self.eta - 1), (2 ** self.eta) - 1)
            if is_odd(key):
                break
        self.sk = key
        return key


    def _public_key(self):
        """
        generate public keys
        :return: a list of public public keys sampled from a distribution see below
        """
        while True:
            x = []
            for i in range(0, self.tau + 1):
                q = randint(0, ((2 ** self.gama) // self.sk) - 1)   # <----- fix division overflow
                r = randint(-(2 ** self.rho) - 1, (2 ** self.rho) - 1)
                x.append((self.sk * q) + r)

            x.sort(reverse=True)  # max element is in 0 index

            if x[0] != max(x):  # sanity check
                raise ValueError("x[0] isn't max element")

            if is_odd(x[0]) and is_even_mod(x[0], self.sk):
                break
        self.pk = x
        return x

    def keygen(self, save=False, verbose=False):
        """
        :param save: option to dump keys generated to file
        :param verbose: option to display information during key generation process
        :return:a tuple of (sk , pk)
        """
        if verbose:
            print("Private Key Range Space Low: {} - High: {}".format(2 ** (self.eta - 1), (2 ** self.eta) - 1))
            self.calc_key_size(verbose=True)
        if save:
            sk = self._private_key()

            with open("sk.key", 'w') as file:
                file.write(str(sk))

            pk = self._public_key()

            with open("pk.key", 'w') as file:
                for k in pk:
                    file.write(str(k) + '\n')

            return sk, pk
        else:
            return self._private_key(), self._public_key()

    def calc_key_size(self, units='mb', verbose=True):
        """
        :param units: option to specify units subdivision
        :param verbose:  option to display information during key size calculation process
        :return: size of the public key in units
        """
        conversion = {
            'mb': [8 * (1024 ** 2)],
            'gb': [8 * (1024 ** 3)],
            'tb': [8 * (1024 ** 4)]
        }
        size = (self.gama * self.tau) / conversion[units][0]
        if verbose:
            print("L:{} -> Public Key size: {:.2f} {}".format(self._lambda, size, units))
        return size

    def get_public_key(self):
        return self.pk

    def get_private_key(self):
        return self.sk
