#pragma once
#include <gmpxx.h>

const mpz_class SMALL_PRIME = 13;
const mpz_class TINY = 315;
const mpz_class SMALL = 164009;
const mpz_class MEDIUM = 31590235;
const mpz_class LARGE = 3453456235233;
const mpz_class RANDOM_BIG_NUMBER("390458390458039483495839045830495834095"); // this one causes segfault on my machine
const mpz_class RSA_32bit = 2697347339;
const mpz_class RSA_45bit = 21257118674101;
const mpz_class RSA_60bit = 1002429489260870947;
const mpz_class RSA_64bit("14385151724416134083");
const mpz_class RSA_80bit("954805732328070751006589");
const mpz_class RSA_80bit_2("996600870464138084090833");

// limit for being able to solve quickly (under 15 seconds)
const mpz_class RSA_90bit("862276052120412518585657711");               // this one causes segfault on my machine
const mpz_class RSA_90bit_2("805752301779934695941029157");

// never actually successfully either of these
const mpz_class RSA_100bit("875362224385178178735528477353");
const mpz_class RSA_129bit("482066570627341320630247668806730696571");
