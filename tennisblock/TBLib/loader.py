import json

from .DBTeams import DBTeams


def load_matches(jsonfile):

    with open(jsonfile, 'r') as fp:
        sequences = json.load(fp)

    db_manager = DBTeams()
    mtg = db_manager.get_meeting()
    db_manager.insert_generated_sequence(None, sequences)


def save_matches(jsonfile):

    db_manager = DBTeams()
    mtg = db_manager.get_meeting()
    sequences = db_manager.get_current_sequence(None)

    with open(jsonfile, 'w') as fp:
        json.dumps(sequences, indent=4)