from statestyle.data import CROSSWALK

def generate_state_dict():
    """
    Generate a dict with all US states
    *Uses latimes-statestyle data*
    """
    states = {}

    for postal, state in CROSSWALK.items():

        # Ignore the integer, lowercase, and any other indices aside from
        # uppercase, two-letter state abbreviations.
        #
        # If this state/territory's postal abbreviation has not been added yet,
        # insert it into the dict
        if isinstance(postal, str) and len(postal) == 2 and \
                postal.isupper() and postal not in states:
            states.update({postal: state['name']})

    return states

