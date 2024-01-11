# -*- coding: utf-8 -*-

from keys.public_key import PublicKey
import matplotlib.pyplot as plt
from timeit import default_timer as timer


def test_key_size(L_low, L_max=20, units='mb', showFigure=False, file='sec_pam_vs_key_size.png'):
    """
    test function for key size
    """
    print("\n\nRunning test for security parameter vs key size  | L in [{}, {}]\n".format(1, L_max))

    x_axis = [x for x in range(0, L_max + 1)]

    sizes = [0, 0]

    for L in range(2, L_max + 1):
        k = PublicKey(L)
        sizes.append(k.calc_key_size(units=units, verbose=True))

    fig = plt.figure()
    plt.plot(x_axis, sizes)
    plt.xlabel("Security parameter")
    plt.ylabel("Public Key Size in {}".format(units))
    fig.savefig('sec_pam_vs_key_size.png', dpi=fig.dpi)

    print("test end")
    if showFigure:
        plt.show()


def test_key_time(L_low, L_max, units='sec', showFigure=False, file='keygen_vs_time.png'):
    """
    test function for key generation time
    """
    print("\n\nRunning test for security parameter vs key generation time | L in [{}, {}]\n".format(1, L_max))

    conversion = {
        'sec': [1],
        'hour': [60 ** 2],
        'days': [24 * (60 ** 2)]
    }
    times = [0, 0]  # quick fix for keygen with L=1 assume 0 time

    x_axis = [x for x in range(0, L_max + 1)]

    for L in range(2, L_max + 1):
        k = PublicKey(L)
        print(k)
        start = timer()
        sk, pk = k.keygen(save=False)
        end = timer()

        t = float(end - start) / conversion[units][0]
        times.append(t)
        print("L: {} -> time: {:.4f} {}".format(L, t, units))

    fig = plt.figure()

    plt.plot(x_axis, times)
    plt.xlabel("Security parameter")
    plt.ylabel("Time for Key Generation (pk,sk) in {}".format(units))
    fig.savefig(file, dpi=fig.dpi)

    print("test end")
    if showFigure:
        plt.show()


if __name__ == "__main__":
    units_size = 'mb'
    units_time = 'sec'
    L_low = 2
    L_max = 10

    test_key_size(L_low, L_max=L_max, showFigure=False, units=units_size)

    test_key_time(L_low, L_max=L_max, showFigure=False, units=units_time)
