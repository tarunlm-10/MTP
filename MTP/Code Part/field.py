from petlib.ec import EcGroup
from petlib.bn import Bn

# Choose a large prime p such that p = 3 (mod 4)
p = 52435875175126190479447740508185965837690552500527637822603658699938581184513

# Choose a non-square element d in Fp
d = Bn.from_decimal(168696)

# Define the twisted Edwards curve E over Fp
E = EcGroup(1, d, p)

# Choose a point P on E of order q
q = Bn.from_decimal(7237005577332262213973186563042994240857116359379907606001950938285454250989)
P = q * E.generator()

# Compute the bilinear pairing e(P, P)
e = E.pairing(P, P)

# Serialize the parameters of the bilinear group
params = {'p': p, 'q': q, 'E': E, 'P': P, 'e': e}
params_bytes = serialization.serialize(params, serialization.Encoding.PEM)
