
#pragma once

#include <iostream>
#include <gmpxx.h>
#include <gmp.h>
#include <vector>
#include <chrono>
#include <iterator>
#include <map>
#include <utility>
#include <sstream>

using namespace std;

// macros for timing things
#define NOW chrono::high_resolution_clock::now()
#define DUR(x,y) chrono::duration<double, chrono::seconds::period>(y - x).count()

// test macros
#define ASSERT(x, y, z) { if (!x) {cout << RED << __FUNCTION__ << " failed on line " << __LINE__ << " "; \
    cout << "Expected " << y << " got " << z << RESET << endl; return 0;} }
#define IS_TRUE(x) { if (!x) {cout << RED << __FUNCTION__ << " failed on line " << __LINE__ << RESET << endl; return 0;} }
#define PASSED auto t = DUR(s,e); cout << GREEN << __FUNCTION__ << " passed in " << t << " seconds" << RESET << endl; return 1

/// FOR COLORING OUTPUT TEXT
#define RESET   "\033[0m"
#define RED     "\033[31m"
#define GREEN   "\033[32m"
#define YELLOW  "\033[33m" 

// type definitions
using Vec = vector<mpz_class>;
using ull = unsigned long long;
using Matrix = vector<Vec>;
using SolRows = vector<pair<Vec, size_t>>;

// functions defined in utils.cpp
void tonelli_shanks(const mpz_class n, const mpz_class &p, mpz_class &x, mpz_class &other);
map<mpz_class, int> get_p_factors(mpz_class n, Vec base);
Matrix transpose(Matrix &m);

/**
 * Returns the product of a vector
*/
inline mpz_class prod(Vec &vals) {
    mpz_class ret = 1;
    for (auto it = vals.begin(); it != vals.end(); ++it)
        ret *= *it;
    return ret;
}

/// DEBUGGING STUFF BELOW

template<typename T>
string mat_to_string(const vector<vector<T>>& t) {
    stringstream ss;
    for (auto row : t) {
        ss << "{ ";
        for (auto el : row) {
            ss << el << ", ";
        }
        ss << "}\n";
    }
    ss << endl;
    return ss.str();
}

template<typename T>
string vec_to_string(const vector<T>& t) {
    stringstream ss;
    ss << "{ ";
    for (auto el : t) {
        ss << el << ", ";
    }
    ss << "}\n";
    return ss.str();
}

template<typename T>
void show_mat(const vector<vector<T>>& t) {
    cout << mat_to_string(t) << endl;
}

template<typename T>
void showvec(const vector<T>& t) {
    cout << vec_to_string(t) << endl;
}

template<typename T>
bool vec_equality(const vector<T> &t1, const vector<T> &t2) {
    if (t1.size() != t2.size()) return false;
    for (size_t i = 0; i < t1.size(); ++i) {
        if (t1[i] != t2[i]) return false;
    }
    return true;
}

bool matrix_eq(const Matrix &m1, const Matrix &m2);
