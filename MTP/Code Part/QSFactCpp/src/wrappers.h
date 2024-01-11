#pragma once
#include <gmpxx.h>


/**
 * Just a collection of wrapper functions for the various C-style functions in gmp that don't support 
 * mpz_class because I got tired of writing .get_mpz_t() and it was horrific for readability
*/

// res = (base^exp) % mod
inline void powm(mpz_class &res, const mpz_class &base, const mpz_class &exp, const mpz_class &mod) {
    mpz_powm(res.get_mpz_t(), base.get_mpz_t(), exp.get_mpz_t(), mod.get_mpz_t());
}
inline void powm_ui(mpz_class &res, const mpz_class &base, const unsigned long exp, const mpz_class &mod) {
    mpz_powm_ui(res.get_mpz_t(), base.get_mpz_t(), exp, mod.get_mpz_t());
} 

// res = base^exp
inline void pow_ui(mpz_class &res, const mpz_class &base, const unsigned long exp) {
    mpz_pow_ui(res.get_mpz_t(), base.get_mpz_t(), exp);
}

/**
 * Using this instead of mpz_legendre because they have slightly different
 * behaviour and it broke my stuff, but it seems doing it this way is still fine?
*/
inline int legendre(const mpz_class &n, const mpz_class &p) {
    mpz_class res;
    powm(res, n, (p- 1) / 2, p);
    return res.get_si();
}

// n = sqrt(n);
inline void big_sqrt(mpz_class &n) {
    mpz_sqrt(n.get_mpz_t(), n.get_mpz_t());
}

inline void big_sqrt(mpz_class &res, const mpz_class &n) {
    mpz_sqrt(res.get_mpz_t(), n.get_mpz_t());
}

// safe mod so mod of negative integers works properly
inline mpz_class safe_mod(mpz_class a, mpz_class b) {
    return (a % b + b) % b;
}

// return the number of digits required to represent n in base "base"
inline int digit_length(const mpz_class &n, int base) {
    return mpz_sizeinbase(n.get_mpz_t(), base);
}

const int MILLER_RABIN_TRIALS = 50;

// returns if n is probably prime
inline int probably_prime(const mpz_class &n) {
    return mpz_probab_prime_p(n.get_mpz_t(), MILLER_RABIN_TRIALS);
}

// res = gcd(a, b)
inline void big_gcd(mpz_class &res, const mpz_class &a, const mpz_class &b) {
    mpz_gcd(res.get_mpz_t(), a.get_mpz_t(), b.get_mpz_t());
}

// removes factor fact from a and store the result in res, return the 
// number of times fact was removed from a
inline int remove_fact(mpz_class &res, mpz_class &a, mpz_class &fact) {
    return mpz_remove(res.get_mpz_t(), a.get_mpz_t(), fact.get_mpz_t());
}