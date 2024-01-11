import numpy as np

# First we set the parameters
M = 8
N = M //2

# We set xi, which will be used in our computations
xi = np.exp(2 * np.pi * 1j / M)
print(xi)

from numpy.polynomial import Polynomial

class CKKSEncoder:
    """Basic CKKS encoder to encode complex vectors into polynomials."""
    
    def __init__(self, M: int):
        """Initialization of the encoder for M a power of 2. 
        
        xi, which is an M-th root of unity will, be used as a basis for our computations.
        """
        self.xi = np.exp(2 * np.pi * 1j / M)
        self.M = M
        
    @staticmethod
    def vandermonde(xi: np.complex128, M: int) -> np.array:
        """Computes the Vandermonde matrix from a m-th root of unity."""
        
        N = M //2
        matrix = []
        # We will generate each row of the matrix
        for i in range(N):
            # For each row we select a different root
            root = xi ** (2 * i + 1)
            row = []

            # Then we store its powers
            for j in range(N):
                row.append(root ** j)
            matrix.append(row)
        return matrix
    
    def sigma_inverse(self, b: np.array) -> Polynomial:
        """Encodes the vector b in a polynomial using an M-th root of unity."""

        # First we create the Vandermonde matrix
        A = CKKSEncoder.vandermonde(self.xi, M)

        # Then we solve the system
        coeffs = np.linalg.solve(A, b)

        # Finally we output the polynomial
        p = Polynomial(coeffs)
        return p

    def sigma(self, p: Polynomial) -> np.array:
        """Decodes a polynomial by applying it to the M-th roots of unity."""

        outputs = []
        N = self.M //2

        # We simply apply the polynomial on the roots
        for i in range(N):
            root = self.xi ** (2 * i + 1)
            output = p(root)
            outputs.append(output)
        return np.array(outputs)


# First we initialize our encoder
encoder = CKKSEncoder(M)

b = np.array([1, 2, 3, 4])
print(b)
print("-----------------------------------------------------")

p = encoder.sigma_inverse(b)
print(p)
print("-----------------------------------------------------")

b_reconstructed = encoder.sigma(p)
print(b_reconstructed)
print("-----------------------------------------------------")

print(np.linalg.norm(b_reconstructed - b))
print("-----------------------------------------------------")

# Show the Homomorphic properties

m1 = np.array([1, 2, 3, 4])
m2 = np.array([1, -2, 3, -4])

p1 = encoder.sigma_inverse(m1)
p2 = encoder.sigma_inverse(m2)

#Homomorphic over addition
print("Addition")
p_add = p1 + p2
print(p_add)
print("-----------------------------------------------------")
res  = encoder.sigma(p_add)
print(res)
print("-----------------------------------------------------")

#Homomorphic over multiplication
print("Multiliplication")
poly_modulo = Polynomial([1,0,0,0,1])
print(poly_modulo)
print("")
p_mult = p1 * p2 % poly_modulo
ans = encoder.sigma(p_mult)
print(ans)