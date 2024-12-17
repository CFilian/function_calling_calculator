def add(a, b):
    """
    Adds two numbers and returns the result.
    
    Args:
        a (int/float): The first number.
        b (int/float): The second number.

    Returns:
        int/float: The sum of a and b.
    """
    return a + b

def subtract(a, b):
    """
    Subtracts the second number from the first and returns the result.
    
    Args:
        a (int/float): The first number.
        b (int/float): The second number.

    Returns:
        int/float: The result of a - b.
    """
    return a - b

def multiply(a, b):
    """
    Multiplies two numbers and returns the result.
    
    Args:
        a (int/float): The first number.
        b (int/float): The second number.

    Returns:
        int/float: The product of a and b.
    """
    return a * b

def divide(a, b):
    """
    Divides the first number by the second and returns the result.
    
    Args:
        a (int/float): The first number (numerator).
        b (int/float): The second number (denominator).

    Returns:
        float: The result of a / b.

    Raises:
        ValueError: If the denominator is zero.
    """
    if b == 0:
        raise ValueError("Cannot divide by zero.")
    return a / b
