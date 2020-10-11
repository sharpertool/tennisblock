from TBLib.teamgen.TeamGen import TeamGen
from TBLib.teamgen.player import Player as TGPlayer

import logging

logging.basicConfig(level=logging.DEBUG)
#root = logging.getLogger("*")
#root.setLevel(logging.DEBUG)

import jsonpickle

def main(filename):

    n_courts = None

    with open('players.json', 'r') as fp:
        frozen = fp.read()
        data = jsonpickle.decode(frozen)

    men = data['men']
    women = data['women']
    n_sequences = data['n_sequences']
    low_threshold = data['low_threshold']
    b_allow_duplicates = data['b_allow_duplicates']
    iterations = data['iterations']
    max_tries = data['max_tries']

    if n_courts is None:
        n_courts = (len(men) + len(women)) // 4

    tg = TeamGen(n_courts, n_sequences,
                 men, women,
                 low_threshold=low_threshold)
    sequences = tg.generate_rounds(
        b_allow_duplicates,
        iterations=iterations,
        max_tries=max_tries
    )

    if sequences is None or len(sequences) < n_sequences:
        return {"status": "fail",
                "error": "Could not generate the required sequences"}

    else:
        # Put the worst sequences last.
        # sequences.reverse()
        tg.display_sequences(sequences)
        tg.show_all_diffs(sequences)

        with open('sequences.json', 'w') as fp:
            frozen = jsonpickle.encode(sequences, indent=4)
            fp.write(frozen)


if __name__ == "__main__":
    main('players.json')

