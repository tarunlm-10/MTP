# QSFact

## The algorithm

For my project I implemented a self-initializing quadratic sieve
(SIQS). The purpose of this algorithm is to factor extremely large
integers. It is the 2nd fastest classical integer factoring algorithm, behind the general number field sieve.

This implementation utilizes the GMP library for arbitrary precision integers, which can be found [here](https://gmplib.org/). Development was done using version `6.2.1-1`.

For performance benchmarking I used a simple implementation of Pollard Rho and a 60 bit RSA number (1002429489260870947). My program completes in roughly 0.54 seconds, while pollards takes
between 10 - 50 seconds, depending on the randomness in the algorithm, even though it doesn't have the extra overhead of doing GMP arithmetic.

### Runtime
according to [this](https://mathworld.wolfram.com/QuadraticSieve.html) page from wolfram mathworld, general runtime of the algorithm is O(X) where X = exp(sqrt(ln(n) ln(ln(n)))). From what I
understand, this is due to the fact that the analytically optimal choice of smoothness
B is X ^ (sqr(2)/4) [reference (page 4)](http://www.damianball.com/pdf/portfolio/quadratic-sieve.pdf), and the asymptotic runtime of the algorithm is relative to the size of the
factor base. My program does not use that formula however, as I found computing
logs using gmp is not supported, and I didn't like any of the workarounds I found.
So instead I use a set of fixed parameters based on the base 10 digit length of N. Therefore, my solution is likely some factor slower than optimal.

## Running the program
1. Enter the source folder: `cd src`
2. compile the project: `make`
3. Run the program with the appropriate arguments

    For choosing the number to factor, there are two options, use `--level` and choose a
    number `[1, 9]`. Each level corresponds to a RSA number generated [here](https://bigprimes.org/RSA-challenge), with the difficulty of the number increasing with each level. The exact numbers the levels refer to can be found in `qsmain.cpp`
    ```
    ./qsmain --level 5
    ```
    Another option is to input any valid positive integer yourself using `--user`
    ```
    ./qsmain --user 23894623598
    ```
    An additional optional argument is `--iter-cap` which allows the user to set the
    max number of iterations the algorithm will try before giving up (default: 100).
    This should be used if you want to test out a large number, but don't want to
    risk it running for hours. As due to the fact that the factor base size, and interval size both increase with each
    iteration, completing 100 iterations could take a very long time.
    ```
    ./qsmain --level 8 --iter-cap 20
    ```
    Bear in mind that either `--level` or `--user` must be the first argument to the program, and `--iter-cap` must be second if included, otherwise an error will be printed and the program will exit.

    If you try and factor a number that is over 80 bits, you will be warned that factoring this number could take a very long time (at least on my machine), and you will be prompted to enter `y` if you wish to continue. You may also be warned if the probable prime test returns an uncertain result, meaning N is probably prime, but not proven to be prime. In this event you should probably abort, but just in case the user knows for a fact the number is not prime, and the test has made a mistake, the option to continue is still there.
### Running Tests
1. Running Unit tests
    
    A few unit tests have also been included that includes test for number up until 80 bits long, as well as one test which tests random number with factors from with the interval [400, sqrt(MAX_INT)]. The random test will also report the number of "weak factors" that were produced. I have defined a weak factor as anything less than 10. This metric isn't terribly important, but since the factor of every test case is at least 400, then it should have been possible to find a more interesting factor.
    ```
    cd src
    make tests
    ./tests
    ```
    For the unit tests the output of the factoring will not be shown, but rather it will print whether each test passed. Ex: e.g: `test_qs_RSA64 passed in 0.861948 seconds`.

    If you wish to perform the Pollard Rho performance test on your own machine, simply uncomment the last test case in `tests.cpp` called `qs_vs_pollard_1()`

## Program Ouput
The output of the main program is simply the time it took to find a solution in seconds, as well as
the two factors that were found, e.g:
```
Attempting to factor 2345346...
time taken (seconds): 0.0891863
factor 1: 8986
factor 2: 261
```

## Issues to Note
Very large inputs (~90 bits) seem to have a chance of causing a `segfault`, and I was never able to understand why, as running the program through valgrind is orders of magnitude slower, and it may take far longer to find the segfault than I am at liberty to wait. Although my only guess is the size of the matrix grows too large to be allocated in memory, as unfortunately since my implementation is quite naive, it is also not very memory efficient. It is also possible that the random tests section of the unit tests may take far longer than the average of 4 seconds if a problematic number is generated, of which I also don't know the cause. Otherwise, the program should work as intended.

The case where the primality test returns 1 because N is only probably prime hasn't actually been tested because I couldn't find a number that caused that to happen.

Another note is this project was developed using my personal machine with these specs:
```
Ryzen 3700x 8-core CPU
32 GB RAM
Manjaro Linux
gcc version 10.2.0
gmp version 6.2.1-1
```
I seem to have ironed out any MacOS-specific issues due to the differences in the C compilers on Linux and MacOS, but just in case something goes wrong, I would first try and run it on a linux system.

## Summary of Files
- qsmain.cpp: The entry point for the CLI program, usage explained [above](##Running-the-program)
- quad_sieve.cpp: Contains the core implementation of the SIQS algorithm
- utils.cpp/.h: A collection of utilities for debugging, more general algorithms e.g: matrix transpose, and helpful macros and type definitions
- pollard.h: An implementation of Pollard Rho's to compare the performance of my SIQS algorithm
- wrappers.h: A collection of wrapper functions for the old C-style GMP functions, so I could avoid having to use `mpz_class.get_mpz_t()` so often
- test_numbers.h: All the numbers I used for unit testing, as well as a few that are too large for me to factor in a reasonable timeframe

# References
https://en.wikipedia.org/wiki/Quadratic_sieve

https://en.wikipedia.org/wiki/Smooth_number#Definition

https://planetmath.org/QuadraticSieve

http://www.damianball.com/pdf/portfolio/quadratic-sieve.pdf

https://www.geeksforgeeks.org/p-smooth-numbers-p-friable-number/

https://www.youtube.com/watch?v=Y3N0vZoPCWE

https://en.wikipedia.org/wiki/Sieve_of_Eratosthenes

https://martinlauridsen.info/pub/bsc_thesis.pdf

https://github.com/Maosef/Quadratic-Sieve/blob/242238b74ded1983f91160952e57e949beae16eb/Quadratic%20Sieve.py

https://en.wikipedia.org/wiki/Tonelli%E2%80%93Shanks_algorithm

 self intializing values taken from https://github.com/skollmann/PyFactorise/blob/master/factorise.py

all RSA numbers generated here https://bigprimes.org/RSA-challenge

https://stackoverflow.com/questions/9158150/colored-output-in-c/9158263