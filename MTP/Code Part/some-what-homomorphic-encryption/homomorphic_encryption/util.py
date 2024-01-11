from math import log, sqrt
from random import choice


def is_odd(n):
    """
    check if number n is odd
    :param n:
    :return: if is odd return True, otherwise return False
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


def is_even_mod(n, p):
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


def count_num_bits(n):
    """
    :param n:  integer num
    :return: number of bits in num
    """
    return len("{0:b}".format(n))


def log2(n):
    """
    :param n: number
    :return: log base two of number
    """
    return log(n, 2)


def is_prime(n):
    """
    check if number n is a prime number
    :param n: number
    :return: (Boolean) True if n is prime , False otherwise
    """
    if n % 2 == 0 and n > 2:
        return False
    return all(n % i for i in range(3, int(sqrt(n)) + 1, 2))


def get_random_prime(interval):
    """
    find a random prime in the interval [0, interval]
    :param interval
    :return: prime number
    """
    primes = []
    for n in range(interval + 1):
        if is_prime(n):
            primes.append(n)

    return choice(primes)


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
