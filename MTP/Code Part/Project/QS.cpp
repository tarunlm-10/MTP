#include <iostream>
#include <gmpxx.h>
#include <math.h>
#include <vector>
#include "utility.h"
#include "wrappers.h"

using namespace std;

class QS
{
    mpz_class root;
    long smooth_bound;
    mpz_class interval_size;
    Vec factor_base;
    int ITER_MAX;
    
    public:
        bool quad_sieve(const mpz_class &n, mpz_class &fact1, mpz_class &fact2, int iteration_cap=100)
        {   
            mpz_class root;
            mpz_sqrt(root.get_mpz_t(), n.get_mpz_t());

            ITER_MAX=iteration_cap;

            if (root * root == n) {
                cout << "N is a perfect square\n";
                fact1 = root;
                fact2 = root;
                return true;
            }

            // initialize the smooth bound B and sieve interval size
            initialize(n);

            // just as a safeguard
            int ITERS = -1;
            for (;;) {

                ++ITERS;
                if (ITERS == ITER_MAX) {
                    fact1 = 1;
                    fact2 = n;
                    return false;
                }

                Vec smooths, xlist;

                // generate a base of primes
                create_factor_base(n);

                // generate our list of smooth numbers
                gen_smooth_numbers(n, smooths, xlist);
                
                // couldn't find any smooth numbers
                // need to widen our search and try again
                if (smooths.size() != 0) {
                    
                    // build the exponent matrix
                    Matrix matrix = gen_matrix(smooths, n);

                    vector<bool> flagged;
                    SolRows solutions_rows;
                    // find solutions to the linear system
                    solve_linear(matrix, flagged, solutions_rows);

                    mpz_class x, y;

                    // try all the possible solutions we found
                    for (const auto &solution : solutions_rows) {

                        // extract dependent row
                        vector<size_t> sol_vec = find_dependencies(solution, matrix, flagged);
                        cout<<"Solution Vector"<<endl;
                        for(auto itr: sol_vec){
                            cout<<itr<<" ";
                        }
                        cout<<endl;
                        // calculate the x and y values
                        Vec a_vec, b_vec;
                        for (auto i : sol_vec) {
                            a_vec.push_back(smooths[i]);
                            b_vec.push_back(xlist[i]);
                        }
                        
                        x = abs(prod(a_vec));
                        big_sqrt(x);
                        y = prod(b_vec);

                        // test to see if this is a solution
                        big_gcd(fact1, x - y, n);
                        

                        if (fact1 != 1 && fact1 != n) {
                            fact2 = n / fact1;
                            return true;
                        }
                    }
                }
                //cout<<"hahahhahhahhahah"<<endl;
                /** 
                 * failed to find a factor, expand and try again
                 * the size of the expansion are kind of arbitrary
                 * but they seem to work pretty well
                */
                smooth_bound += smooth_bound / 10;
                interval_size += 500;
            }


        }
        void initialize(const mpz_class &n){
            size_t d = digit_length(n, 10);

            if (d <= 34) {
                smooth_bound = 100;
                interval_size = 100;
            } else if (d <= 36) {
                smooth_bound = 300;
                interval_size = 65536;
            } else if (d <= 38) {
                smooth_bound = 400;
                interval_size = 65536;
            } else if (d <= 40) {
                smooth_bound = 500;
                interval_size = 65536;
            } else if (d <= 42) {
                smooth_bound = 600;
                interval_size = 65536;
            } else if (d <= 44) {
                smooth_bound = 700;
                interval_size = 65536;
            } else if (d <= 48) {
                smooth_bound = 1000;
                interval_size = 65536;
            } else if (d <= 52) {
                smooth_bound = 1200;
                interval_size = 65536;
            } else if (d <= 56) {
                smooth_bound = 2000;
                interval_size = 65536 * 3;
            } else if (d <= 60) {
                smooth_bound = 4000;
                interval_size = 65536 * 3;
            } else if (d <= 66) {
                smooth_bound = 6000;
                interval_size = 65536 * 3;
            } else if (d <= 74) {
                smooth_bound = 10000;
                interval_size = 65536 * 3;
            } else if (d <= 80) {
                smooth_bound = 30000;
                interval_size = 65536 * 3;
            } else if (d <= 88) {
                smooth_bound = 50000;
                interval_size = 65536 * 3;
            } else if (d <= 94) {
                smooth_bound = 60000;
                interval_size = 65536 * 9;
            } else {
                smooth_bound = 100000;
                interval_size = 65536 * 9;
            }

        }


        void create_factor_base(const mpz_class &n){
            factor_base.clear();
            vector<bool> primes(smooth_bound + 1, true);
            primes[0] = primes[1] = false;

            for (long i = 2; i < (long)sqrt(smooth_bound); ++i) {
                if (primes[i]) {
                    for (long j = i*i; j < smooth_bound + 1; j += i)
                        primes[j] = false;
                }
            }

            for (long i = 2; i < smooth_bound + 1; ++i) {
                if (primes[i] && legendre(n, mpz_class(i)) == 1)
                    factor_base.push_back(i);
            }
            cout<<"Factor Base is"<<endl;
            for (auto itr : factor_base){

                cout << itr << " ";
                }
            cout<< endl;
        }

        void gen_smooth_numbers(const mpz_class &n, Vec &smooths, Vec &xlist){
            Vec sequence;
            sequence.reserve(interval_size.get_ui() * 2);
            mpz_class res;

            // build vector possible numbers
            for (mpz_class i = root - interval_size ; i < root + interval_size; ++i) {
                pow_ui(res, i, 2);
                sequence.push_back(res - n);
            }

            Vec sieved(sequence);

            bool two_in_base = factor_base[0] == 2;

            // handle the slighty special case of 2 being in the factor base
            if (two_in_base) {
                size_t i = 0;
                while (sieved[i] % 2 != 0) 
                    ++i;

                mpz_class two = 2;
                for (; i < sieved.size(); i += 2) {
                    remove_fact(sieved[i], sieved[i], two);
                    // while (sieved[i] % 2 == 0)
                    //     sieved[i] /= 2;
                }
            }

            mpz_class sol1, sol2, temp;

            for (size_t i = two_in_base ? 1 : 0; i < factor_base.size(); ++i) {
                // use tonelli shankes to solve congruence r^2 = n mod factor_base[i]
                tonelli_shanks(n, factor_base[i], sol1, sol2);
                for (auto sol : {sol1, sol2}) {

                    // calculate the start point of the interval, and then convert back to
                    // ulong
                    // using safe mod cause (sol - root + interval_size) is mostly likely
                    // a negative number
                    temp = safe_mod((sol - root + interval_size), factor_base[i].get_ui());
                    size_t start1 = temp.get_ui();

                    // remove prime in the base from the possibly smooth number
                    for (size_t j = start1; j < sieved.size(); j += factor_base[i].get_ui()) {
                        remove_fact(sieved[j], sieved[j], factor_base[i]);
                    }

                    temp = safe_mod((sol - root + interval_size), factor_base[i]) + interval_size;
                    size_t start2 = temp.get_ui();

                    for (long j = start2; j > 0; j -= factor_base[i].get_ui()) {
                        remove_fact(sieved[j], sieved[j], factor_base[i]);
                    }
                }
            }

            /**
             * if sieved[i] == 1, then the original number, which will
             * be sequence[i] is smooth
            */
            for (size_t i = 0; i < sieved.size(); ++i) {
                if (abs(sieved[i]) == 1) {
                    smooths.push_back(sequence[i]);
                    xlist.push_back(i+root-interval_size);
                }
            }
            cout<<"---------------"<<endl;
            cout<<"B-smooth values are: -"<<endl;
            for (auto itr : smooths){
                cout << itr << " ";}
            cout<<endl;
        }


        Matrix gen_matrix(const Vec &smooths, const mpz_class &n){
            factor_base.insert(factor_base.begin(), -1);
            Matrix matrix(smooths.size(), Vec(factor_base.size()));

            for (size_t i = 0; i < smooths.size(); ++i) {
                auto factors = get_p_factors(smooths[i], factor_base);

                for (size_t j = 0; j < factor_base.size(); ++j) {
                    if (factors.find(factor_base[j]) != factors.end ())
                        matrix[i][j] = factors[factor_base[j]] % 2;
                }
            }
            cout<<"---------------"<<endl;
            cout<< "Exponent Matrix"<<endl;
            for (auto &row: matrix) {
                for (auto &i: row) {
                    cout << i << ' ';
                }
                cout << endl;
            }
            return transpose(matrix);
        }


        void solve_linear(Matrix &matrix, vector<bool> &flagged, SolRows &solution_rows){
            gauss(matrix, flagged);

            for (size_t i = 0; i < flagged.size(); ++i) {
                if (!flagged[i]) {
                    solution_rows.push_back({matrix[i], i});
                }
            } 
            cout<<"---------------"<<endl;
            cout<<"Solution Set"<<endl;
            for(auto &itr : solution_rows){
                for( auto &it : itr.first){
                    cout<< it <<  " " ;
                }
                cout<<","<< itr.second << endl ;
            }

        }

        void gauss(Matrix &A, vector<bool> &flagged){
            flagged.clear();
            flagged.resize(A[0].size(), false);

            for (size_t i = 0; i < A.size(); ++i) {
                for (size_t j = 0; j < A[i].size(); ++j) {
                    if (A[i][j] == 1) {
                        flagged[j] = true;
                        for (size_t k = 0; k < A.size(); ++k) {
                            if (k == i) continue;
                            if (A[k][j] == 1) {
                                for (size_t l = 0; l < A[k].size(); ++l) {
                                    A[k][l] = (A[k][l] + A[i][l]) % 2;
                                }
                            }
                        }
                        break;
                    }
                }
            }
            A = transpose(A);

        }



        vector<size_t> find_dependencies(const pair<Vec, size_t> &solution, Matrix &matrix, vector<bool> &flagged){
            vector<size_t> sol_vec;
            vector<size_t> indices;
            for (size_t i = 0; i < solution.first.size(); ++i) {
                if (solution.first[i] == 1)
                    indices.push_back(i);
            }

            for (size_t row = 0; row < matrix.size(); ++row) {
                for (auto i : indices) {
                    if (matrix[row][i] == 1 && flagged[row]) {
                        sol_vec.push_back(row);
                    }
                }
            }
            sol_vec.push_back(solution.second);
            return sol_vec;
        }




};

int main(int argc, char *argv[]) {
    QS qs = QS(); // Create an object of QS class
    mpz_class n;
    mpz_class factor1,factor2;
    int iteration_cap = 100;
    n = argv[1];
    cout << " Factoring ------- " << n << "..." << endl;
    auto s = NOW;
    bool success = qs.quad_sieve(n, factor1, factor2, iteration_cap);
    auto e = NOW;
    auto t = DUR(s, e);

    if (!success) {
        cout << "factoring failed, try increasing iteration cap\n";
    } else {
        if (factor1 == 1 && factor2 == n) {
            cout << n << " was found to be prime\n";
        } else {
            mpz_class res = factor1*factor2;
            ASSERT((res == n), n, res);
        }
    }

    cout << "time taken (seconds): " << t << endl;
    cout << "factor 1: " << factor1 << endl;
    cout << "factor 2: " << factor2 << endl;
    return 0;
}
