def random_number_generator(length=6):
    """Generates a random number of specified length."""
    import random
    import string
    
    if length < 1:
        raise ValueError("Length must be at least 1")
    
    digits = string.digits
    return ''.join(random.choice(digits) for _ in range(length))
