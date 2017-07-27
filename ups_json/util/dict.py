
def get_nested(dictionary, *keys):
    """
    Get a value from nested keys in a dictionary
    """
    for key in keys:
        if isinstance(dictionary, dict):
            dictionary = dictionary.get(key)
        else:
            return None

    return dictionary

