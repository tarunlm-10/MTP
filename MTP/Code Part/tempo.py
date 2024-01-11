import gmpy2

def multiply_large_fraction_and_integer(fraction, integer):
    # Convert input strings to GMP integers and fractions
    fraction = gmpy2.mpq(fraction)
    integer = gmpy2.mpz(integer)

    # Perform multiplication
    result = gmpy2.mul(fraction, integer)

    return result

# Example usage:
large_fraction = "1234567890123456789098765432109876.7878778"
large_integer = "987654321098765432109876543210"
result = multiply_large_fraction_and_integer(large_fraction, large_integer)

print(f"The result of multiplying {large_fraction} and {large_integer} is:")
print(result)