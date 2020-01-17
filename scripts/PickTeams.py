import sys
from optparse import OptionParser

from TBLib.teamgen.TeamGen import TeamGen

from TBLib.teamgen.DBTeams import DBTeams


def pick_teams(fp, db_manager, n_courts, n_sequences,
               b_allow_duplicates, testing=False):
    men, women = db_manager.get_players()

    if len(men) < n_courts * 2 or len(women) < n_courts * 2:
        print("Cannot pick teams, there are not enough men or women.")
        print("Need %d of both. Have %d men and %d women." % (n_courts * 2, len(men), len(women)))
        return

    tg = TeamGen(n_courts, n_sequences, men, women)
    sequences = tg.generate_rounds(b_allow_duplicates)

    if sequences is None or len(sequences) < n_sequences:
        fp.write("Could not generate the required sequences.")

    else:
        # Put the worst sequences last.
        sequences.reverse()
        tg.display_sequences(sequences)
        tg.show_all_diffs(sequences)

        if not testing:
            db_manager.insert_records(sequences)

    fp.write("Done")


def main():
    usage = "usage: %prog -n -m -s]"
    parser = OptionParser(usage)
    parser.add_option("-m", dest="matchid",
                      action="store",
                      type="int",
                      help="Matchid to schedule.")
    parser.add_option("-c", dest="courts",
                      action="store",
                      type="int",
                      default=3,
                      help="Number of courts.")
    parser.add_option("-s", dest="sequences",
                      action="store",
                      type="int",
                      default=3,
                      help="Number of sequences.")
    parser.add_option("-f", dest="outfile",
                      action="store",
                      type="string",
                      default="/tmp/schedule.log",
                      help="File to output debug data to")
    parser.add_option('-n', dest='nodups',
                      action="store_true",
                      default=False,
                      help="Option to disable seeing an opponent 2 times.")
    parser.add_option("-v", action="store_false", dest="verbose")
    parser.add_option("-t", action="store_true", dest="test")

    (options, args) = parser.parse_args()

    fp = sys.stdout

    try:
        if options.matchid:
            teams = DBTeams(options.matchid)
        else:
            teams = DBTeams()
    except:
        print("Could not open a DB Connection.")
        sys.exit(2)

    fp.write("Scheduling for Matchid:%s\n" % teams.matchid)

    pick_teams(fp,
               teams,
               options.courts,
               options.sequences,
               options.nodups,
               options.test)

    fp.close()


if __name__ == '__main__':
    main()
