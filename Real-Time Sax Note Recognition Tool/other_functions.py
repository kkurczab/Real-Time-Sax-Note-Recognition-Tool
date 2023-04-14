##---------------------------------Functions------------------------------
def find_closest_key(value, keys):
    """
    Finds the key from the array that has the closest value to the given value.

    Args:
        value (float or int): The value to be matched.
        keys (list): The array of keys to search.

    Returns:
        Key from the array with the closest value to the given value.
    """
    closest_key = None
    min_difference = float('inf')  # Set initial difference to infinity

    for key in keys:
        difference = abs(key - value)
        if difference < min_difference:
            min_difference = difference
            closest_key = key

    return closest_key
#-----------------------------------
def find_key_by_value(notes, value):
    for x in notes:
        if x[1] == value:
            return x[0]
    return None
#------------------------------------------------------------------------
