import os

import datetime

from django.http import HttpResponse

from TBLib.teams import TeamManager
from TBLib.playsheetrl import PlaySheet as PlaySheet
from .apiutils import get_current_season, get_next_meeting

def blockSheet(request, date=None):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':

        mgr = TeamManager()

        matchData = mgr.queryMatch(date)
        season = get_current_season()

        if date:
            date_string = datetime.datetime.strptime(date,"%Y-%m-%d").strftime("%A,%B %d")
            header = "Friday Night Block:{}".format(date_string)
        else:
            mtg = get_next_meeting()
            date_string = mtg.date.strftime("%A,%B %d")
            header = "Block sheet for {}".format(date_string)

        num_courts = len(matchData[0])

        gen = PlaySheet(num_courts=num_courts,num_matches=len(matchData))

        pdffile = gen.generate_sheet(header=header,
                                     firstcourt=season.firstcourt,
                                     sched=matchData)



        response = HttpResponse(pdffile,content_type='application/pdf')

        #response.write(pdffile)
        #response['Content-Disposition'] = 'attachement; filename="BlockSheet.pdf"'

        return response


def main():
    mgr = TeamManager()

    matchData = mgr.queryMatch()

    header = "Friday Night Block"

    tmpFile = '/tmp/blocksheet.pdf'

    pdf = PlaySheet(orientation='L', unit='in', format='Letter')
    pdf.set_font('Arial', '', 14);
    pdf.add_page()
    pdf.GenerateSheet(header, matchData)
    if os.path.exists(tmpFile):
        os.unlink(tmpFile)
    pdf.output(tmpFile)


if __name__ == '__main__':
    main()
