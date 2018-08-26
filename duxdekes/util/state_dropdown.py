import csv

def generate_state_dict(data_file):
    """
    Generate a dict with all US states
    *Uses latimes-statestyle data CSV*
    """

    data = list(csv.DictReader(open(data_file, "r")))
    states = {}

    for state in data:
        data.update({state['postal']: state['name']})

    return states

