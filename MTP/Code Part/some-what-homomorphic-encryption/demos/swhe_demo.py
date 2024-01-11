# -*- coding: utf-8 -*-
import sys
sys.path.append('..')
from keys.public_key import PublicKey
from homomorphic_encryption.public_key_swhe import SWHE
import matplotlib.pyplot as plt
from timeit import default_timer as timer


def main(lambda_low=2, lambda_high=10, showFigures=False):
    lambda_low = lambda_low
    lambda_high = lambda_high
    security_parameters = [x for x in range(lambda_low, lambda_high)]

    encryption_times = []
    evaluation_times = []
    decryption_times = []
    keygen_times = []

    for security_parameter in security_parameters:
        print("\n\nSecurity parameter is: {}".format(security_parameter))

        key = PublicKey(security_parameter)
        print("Generating key pair...", end=" ")

        start = timer()
        private_key, public_key = key.keygen(save=False, verbose=True)
        end = timer()
        keygen_times.append(end - start)
        print("key ready Time elapsed: {} sec".format(end - start))
        scheme = SWHE(security_parameter, private_key=private_key, public_key=public_key)

        m0 = 0
        m1 = 1
        print("\n\nencrypting m0...", end=" ")
        start = timer()
        c0 = scheme.encrypt(m0)
        end = timer()
        print("done Time elapsed: {} sec".format(end - start))
        encryption_times.append(end - start)

        print("encrypting m1...", end=" ")
        start = timer()
        c1 = scheme.encrypt(m1)
        end = timer()
        print("done Time elapsed: {} sec".format(end - start))

        # c0 = hm.reduce(c0)
        # c1 = hm.reduce(c1)

        print("\n\ndecrypting m0...", end=" ")
        start = timer()
        m0_ = scheme.decrypt(c0)
        end = timer()
        print("done Time elapsed: {} sec".format(end - start))
        decryption_times.append(end - start)

        print("decrypting m1...", end=" ")
        start = timer()
        m1_ = scheme.decrypt(c1)
        end = timer()
        print("done Time elapsed: {} sec".format(end - start))

        print("\nresults:")
        print("plaintext: {} decrypted: {}".format(m0, m0_))
        print("plaintext: {} decrypted: {}".format(m1, m1_))

        if m0 != m0_ and m1 != m1_:
            raise ValueError("decryption error")

        print("\n\nevaluating c0+c1...", end=" ")
        start = timer()
        add_res = scheme.decrypt(c0 + c1)
        end = timer()
        print("done Time elapsed: {} sec".format(end - start))
        evaluation_times.append(end - start)

        print("evaluating c0*c1...", end=" ")
        start = timer()
        mul_res = scheme.decrypt(c0 * c1)
        end = timer()
        print("done Time elapsed: {} sec".format(end - start))

        print("\nresults:")
        print("homo add res {}+{} : {}".format(m0, m1, add_res))
        print("homo mul res {}*{} : {}".format(m0, m1, mul_res))

        if add_res != (m0 + m1) % 2 and mul_res != (m0 and m1):
            raise ValueError("evaluation error")

    x_axis = [x for x in range(lambda_low, lambda_high)]

    fig = plt.figure()
    plt.plot(x_axis, keygen_times)
    plt.xlabel("Security parameter")
    plt.ylabel("Key generation time sec")
    fig.savefig('sec_pam_vs_key_gen_time.png', dpi=fig.dpi)
    if showFigures:
        plt.show()

    fig = plt.figure()
    plt.plot(x_axis, encryption_times)
    plt.xlabel("Security parameter")
    plt.ylabel("Encryption time sec")
    fig.savefig('sec_pam_vs_encr_time.png', dpi=fig.dpi)
    if showFigures:
        plt.show()

    fig = plt.figure()
    plt.plot(x_axis, decryption_times)
    plt.xlabel("Security parameter")
    plt.ylabel("Decryption time sec")
    fig.savefig('sec_pam_vs_decry_time.png', dpi=fig.dpi)
    if showFigures:
        plt.show()

    fig = plt.figure()
    plt.plot(x_axis, decryption_times)
    plt.xlabel("Security parameter")
    plt.ylabel("Evaluation time sec")
    fig.savefig('sec_pam_vs_eval_time.png', dpi=fig.dpi)
    if showFigures:
        plt.show()


if __name__ == "__main__":
    main()
