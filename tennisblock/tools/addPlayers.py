
import os
import sys
import argparse
from unipath import Path

PROJECT_DIR = Path(__file__).ancestor(3)

#sys.path.append(GARDENBUZZ_DIR)
#sys.path.append(PROJECT_DIR)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tennisblock_dj.settings.dev")

from django.db import connection

from tennisblock.blockdb.models import Player,Couple,Season,SeasonPlayers
from ToolLib.block import PlayerExcel,currentSeason,addCouples,addPlayers, addSeasonPlayers

def main():
    """
    Main driver for the script.

    """

    parser = argparse.ArgumentParser(description="addPlayers")

    parser.add_argument("xlfile",
                        help="Excel Input file.")

    args = parser.parse_args()

    if not os.path.exists(args.xlfile):
        print "Specified Excel file  %s does not exist." % args.xlfile
        sys.exit(2)

    pe = PlayerExcel()
    players = pe.importExcel(args.xlfile)


    print("Imported %d players" % len(players))

    season = currentSeason()
    addPlayers(players)

    addSeasonPlayers(season,players)

    addCouples(season,players)


if __name__ == '__main__':
    main()




