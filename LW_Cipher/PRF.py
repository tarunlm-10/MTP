import hashlib
import random
def PRF(seed, input_value, output_range):
    # Concatenate the seed and input_value
    data = str(seed) + str(input_value)
    
    # Compute the hash value
    hashed = hashlib.sha256(data.encode()).hexdigest()
    
    # Convert the hashed value to an integer
    hashed_int = int(hashed, 16)
    
    # Map the integer to the desired output range
    output = hashed_int % output_range
    
    return output

# Example usage
# seed = random.randint(2**127 +1,2**128)
# print(seed)
if __name__ == "__main__":

    seed = 234636982233052536655583361199366795077
    input_value = 1
    output_range = 2**128

    result = PRF(seed, input_value, output_range)
    print("Output:", result)
