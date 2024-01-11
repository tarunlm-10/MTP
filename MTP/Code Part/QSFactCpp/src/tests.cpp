#include <iostream>
#include <gmpxx.h>
#include "utils.h"
#include <vector>
#include "quad_sieve.h"
#include <string>
#include "wrappers.h"
#include "test_numbers.h"
#include <random>
#include "pollard.h"

using namespace std;


bool test_tonelli_shanks() {
    string expected = "(9, 4)";
    char recieved[10];
    mpz_class n = 315;
    mpz_class p = 13;
    mpz_class s1, s2;

    auto s = NOW;
    tonelli_shanks(n, p, s1, s2);
    auto e = NOW;

    gmp_sprintf(recieved, "(%Zd, %Zd)", s1.get_mpz_t(), s2.get_mpz_t());
    ASSERT((s1 == 9 && s2 == 4), expected, recieved);

    PASSED;
}

bool test_tonelli_shanks2() {
    string expected = "(14, 3)";
    char recieved[10];
    mpz_class n = 315;
    mpz_class p = 17;
    mpz_class s1, s2;

    auto s = NOW;
    tonelli_shanks(n, p, s1, s2);
    auto e = NOW;

    gmp_sprintf(recieved, "(%Zd, %Zd)", s1.get_mpz_t(), s2.get_mpz_t());
    ASSERT((s1 == 14 && s2 == 3), expected, recieved);

    PASSED;
}

bool test_transpose() {
    Matrix orig = {
        { 1, 2, 3 },
        { 4, 5, 6 },
        { 7, 8, 9 }
    };
    Matrix expected = {
        { 1, 4, 7 },
        { 2, 5, 8 },
        { 3, 6, 9 }
    };
    auto s = NOW;
    Matrix res = transpose(orig);
    auto e = NOW;
    ASSERT((matrix_eq(expected, res)), mat_to_string(expected), mat_to_string(res));

    PASSED;
}

bool test_powm() {
    mpz_class res, base=1123, exp=4, mod=23, expected=3;
    auto s = NOW;
    powm(res, base, exp, mod);
    auto e = NOW;
    ASSERT((res == expected), expected, res);
    PASSED;
}

bool test_legendre() {
    mpz_class n=315, p=13;
    auto s = NOW;
    int res = legendre(n, p);
    auto e = NOW;
    ASSERT((res == 1), 1, res);
    PASSED;
}

QSFact qs = QSFact();
mpz_class f1, f2, n, res;

bool test_qs_tiny() {
    n = TINY;
    auto s = NOW;
    qs.quad_sieve(n, f1, f2);
    auto e = NOW;
    res = f1 * f2;
    ASSERT((res == n && (f1 != 1 && f1 != n)), n, res);
    PASSED;
}

bool test_qs_small() {
    n = SMALL;
    auto s = NOW;
    qs.quad_sieve(n, f1, f2);
    auto e = NOW;
    res = f1 * f2;
    ASSERT((res == n && (f1 != 1 && f1 != n)), n, res);
    PASSED;
}

bool test_qs_medium() {
    n = MEDIUM;
    auto s = NOW;
    qs.quad_sieve(n, f1, f2);
    auto e = NOW;
    res = f1 * f2;
    ASSERT((res == n && (f1 != 1 && f1 != n)), n, res);
    PASSED;
}

bool test_qs_large() {
    n = LARGE;
    auto s = NOW;
    qs.quad_sieve(n, f1, f2);
    auto e = NOW;
    res = f1 * f2;
    ASSERT((res == n && (f1 != 1 && f1 != n)), n, res);
    PASSED;
}

bool test_qs_prime() {
    n = SMALL_PRIME;
    auto s = NOW;
    qs.quad_sieve(n, f1, f2);
    auto e = NOW;
    res = f1 * f2;
    ASSERT((res == n && (f1 == 1 && f2 == n)), n, res);
    PASSED;
}

bool test_qs_really_big() {
    n = RANDOM_BIG_NUMBER;
    auto s = NOW;
    qs.quad_sieve(n, f1, f2);
    auto e = NOW;
    res = f1 * f2;
    ASSERT((res == n && (f1 != 1 && f1 != n)), n, res);
    PASSED;
}

bool test_qs_RSA32() {
    n = RSA_32bit;
    auto s = NOW;
    qs.quad_sieve(n, f1, f2);
    auto e = NOW;
    res = f1 * f2;
    ASSERT((res == n && (f1 != 1 && f1 != n)), n, res);
    PASSED;
}

bool test_qs_RSA45() {
    n = RSA_45bit;
    auto s = NOW;
    qs.quad_sieve(n, f1, f2);
    auto e = NOW;
    res = f1 * f2;
    ASSERT((res == n && (f1 != 1 && f1 != n)), n, res);
    PASSED;
}

bool test_qs_RSA60() {
    n = RSA_60bit;
    auto s = NOW;
    qs.quad_sieve(n, f1, f2);
    auto e = NOW;
    res = f1 * f2;
    ASSERT((res == n && (f1 != 1 && f1 != n)), n, res);
    PASSED;
}

bool test_qs_RSA64() {
    n = RSA_64bit;
    auto s = NOW;
    qs.quad_sieve(n, f1, f2);
    auto e = NOW;
    res = f1 * f2;
    ASSERT((res == n && (f1 != 1 && f1 != n)), n, res);
    PASSED;
}

bool test_qs_RSA80() {
    n = RSA_80bit;
    auto s = NOW;
    qs.quad_sieve(n, f1, f2);
    auto e = NOW;
    res = f1 * f2;
    ASSERT((res == n && (f1 != 1 && f1 != n)), n, res);
    PASSED;
}

bool test_qs_RSA80_2() {
    n = RSA_80bit_2;
    auto s = NOW;
    qs.quad_sieve(n, f1, f2);
    auto e = NOW;
    res = f1 * f2;
    ASSERT((res == n && (f1 != 1 && f1 != n)), n, res);
    PASSED;
}


bool test_perfect_square() {
    n = 9;
    auto s = NOW;
    qs.quad_sieve(n, f1, f2);
    auto e = NOW;
    res = f1 * f2;
    ASSERT((res == n && (f1 != 1 && f1 != n)), n, res);
    PASSED;
}

bool random_test() {
    random_device rd;
    uniform_int_distribution<unsigned long> dist(400, sqrt(INT_MAX));
    int bad_count = 0;
    auto s = NOW;
    cout << "Starting random tests...\n"; 
    for (int i = 0; i < 100; ++i) {
        mpz_class a = dist(rd);
        mpz_class b = dist(rd);
        n = a * b;
        qs.quad_sieve(n, f1, f2);
        res = f1 * f2;
        IS_TRUE((f1 != 1 && f1 != n));
        ASSERT((res == n), n, res);
        // cout << n << " " << f1 << " " << f2 << endl;
        if (f1 < 10 || f2 < 10)
            ++bad_count;
    }
    auto e = NOW;
    auto t = DUR(s, e);
    cout << GREEN << "random test suceeded " << bad_count << "/100 weak factors generated in " << t << " seconds" << RESET << endl;
    return true;
}

bool qs_vs_pollard_1() {
    long long long_n = RSA_60bit.get_ui();
    cout << "Using pollard for 60 bit RSA\n";
    auto s = NOW;
    long long res = PollardRho(long_n);
    auto e = NOW;
    auto t = DUR(s, e);
    long long fact2 = long_n / res;
    IS_TRUE(res * fact2 == long_n);
    cout << "pollard found " << res << " " << fact2 << " in " << t << " seconds\n";

    n = RSA_60bit;
    cout << "Using QS for 60 bit RSA\n";
    s = NOW;
    qs.quad_sieve(n, f1, f2);
    e = NOW;
    t = DUR(s, e);
    IS_TRUE(f2 * f2 == n);
    cout << "QS found " << f1 << " " << f2 << " in " << t << " seconds\n";

    return true;
}

bool test_probprime_true() {
    n = 897345903661;
    auto s = NOW;
    int ans = probably_prime(n);
    auto e = NOW;
    ASSERT((ans != 0), "1 or 2", 0);
    PASSED;
}

bool test_probprime_false() {
    n = RSA_129bit;
    auto s = NOW;
    int ans = probably_prime(n);
    auto e = NOW;
    ASSERT((ans == 0), 0, ans);
    PASSED;
}

int main() {
    test_tonelli_shanks();
    test_tonelli_shanks2();
    test_transpose();
    test_powm();
    test_legendre();
    test_qs_tiny();
    test_qs_small();
    test_qs_medium();
    test_qs_large();
    test_qs_prime();
    test_qs_RSA32();
    test_qs_RSA45();
    test_qs_RSA60();
    test_qs_RSA64();
    test_qs_RSA80();
    test_qs_RSA80_2();
    test_perfect_square();
    random_test();
    test_probprime_true();
    test_probprime_false();
    // qs_vs_pollard_1();
}
