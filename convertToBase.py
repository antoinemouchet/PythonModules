"""
Module with a function to convert a positive integer (in base 10) into another base (<10) specified
"""

def convert(number, base):
    """
    Parameters
    ----------
    number: the number to convert (int)
    base: the base in which the number has to be converted (int)

    Returns
    -------
    newNum: the number in the new base (int)

    Notes
    -----
    This function does not work with float numbers or negative numbers.
    The base has to be strictly inferior to 10
    """
    
    # List to store remainders
    remainders = []

    done = False
    # Loop until number is equal to 0
    while not done:
        # Get the result of the entire division and keep it
        result = number // base
    
        # If result is 0 then we leave the loop
        if result == 0:
            done = True
    
        # Add remainder of division to the list of remainders
        remainders.append(number % base)
    
        # Update number value
        number = result

    newNumStr = ''

    # Reverse the list
    remainders.reverse()

    # Add all remainder to string that represents new num
    for remainder in remainders:
        newNumStr += str(remainder)
    
    # Convert string into int
    newNum = int(newNumStr)

    return newNum
