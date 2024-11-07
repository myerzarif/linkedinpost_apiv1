import random

def random_number(length: int = 5) -> int:
    if length <= 1:
        raise ValueError("Length must be a positive integer.")
    
    # Generate the minimum and maximum values for the given length
    min_value = 10**(length - 1)
    max_value = 10**length - 1
    
    # Return a random number in the calculated range
    return random.randint(min_value, max_value)