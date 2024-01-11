#include <gmpxx.h>
#include <iostream>
#include "quad_sieve.h"
#include "utils.h"
#include <assert.h>
#include "test_numbers.h"
#include <map>

using namespace std;

/**
 * Comments below are the runtimes on my personal
 * machine in seconds
*/
map<int, mpz_class> difficulties {
    {1, RSA_32bit},     // 0.075
    {2, RSA_45bit},     // 0.067
    {3, RSA_60bit},     // 0.569
    {4, RSA_64bit},     // 0.925
    {5, RSA_80bit},     // 3.428
    {6, RSA_80bit_2},   // 9.079
    {7, RSA_90bit_2},
    {8, RSA_100bit},
    {9, RSA_129bit},
};


int main(int argc, char* argv[]) {

    if (argc != 3 && argc != 5) {
        cout << "requires exactly 2 or 4 args, recieved: " << argc-1 << endl;
        return 0;
    }
    
    string arg1(argv[1]);
    string arg2(argv[2]);
    string arg3;
    string arg4;

    // default iteration cap
    int iteration_cap = 100;

    // if argc == 5, the the iter cap arg was used
    if (argc == 5) {
        arg3 = argv[3];
        arg4 = argv[4];
        if (arg3 == "--iter-cap") {
            try {
                iteration_cap = stoi(arg4);
                if (iteration_cap < 1) throw(1);
            } catch(...) {
                cout << RED << "Error: --iter-cap must be followed by a valid positive integer" << RESET << endl;
                return 0;
            }
        } else {
            cout << "3rd arg must be --iter-cap " << arg3 << " recieved\n";
            return 0;
        }
    }

    int level = 0;
    mpz_class n;

    // messy arg handling stuff
    if (arg1 == "--level") {
        try {
            level = stoi(arg2);
        } catch (...) {
            cout << RED << "Error: level must be an integer" << RESET << endl;
            return 0;
        }

        if (level < 0 || level > 9)  {
            cout << RED << "Error: level must with the range [0, 9], recieved " << level << RESET << endl;
            return 0;
        }
        n = difficulties[level];
    } else if (arg1 == "--user") {
        try {
            n = arg2;
            if (n < 0) {
                cout << RED << "Error: N must be a postive integer" << RESET << endl;
                return 0;
            }
        } catch (...) {
            cout << RED << "Error: could not parse input as integer" << RESET << endl;
            return 0;
        }
    } else {
        cout << RED << "Error: invalid arg given\nfirst arg must be --level or --user\n" << arg2 << " recieved" << RESET << endl;
        return 0;
    }
    

    // a warning in case a very large number is requested
    if (level > 6 || digit_length(n, 2) > 80)  {
        char resp;
        cout << YELLOW << "Warning: factoring integers over roughly 80 bits may take a very long time, or crash due to lack of memory" << RESET << endl;
        cout << "Do you still wish to continue? [Y/n]: ";
        cin >> resp;
        if (tolower(resp) != 'y')
            return 1;
    }

    cout << "Attempting to factor " << n << "..." << endl;
    mpz_class f1, f2;;
    QSFact qs = QSFact();
    auto s = NOW;
    bool success = qs.quad_sieve(n, f1, f2, iteration_cap);
    auto e = NOW;
    auto t = DUR(s, e);

    if (!success) {
        cout << "factoring failed, try increasing iteration cap\n";
    } else {
        if (f1 == 1 && f2 == n) {
            cout << n << " was found to be prime\n";
        } else {
            mpz_class res = f1*f2;
            ASSERT((res == n), n, res);
        }
    }

    cout << "time taken (seconds): " << t << endl;
    cout << "factor 1: " << f1 << endl;
    cout << "factor 2: " << f2 << endl;
}
