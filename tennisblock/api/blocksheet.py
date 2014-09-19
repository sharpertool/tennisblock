import os


from django.http import HttpResponse
from django.core.servers.basehttp import FileWrapper

from TBLib.teams import TeamManager
from TBLib.playsheet import PlaySheet as PlaySheetFPDF
from TBLib.playsheetrl import PlaySheet as PlaySheet
from .apiutils import get_current_season

def blockSheet(request, date=None):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':

        mgr = TeamManager()

        matchData = mgr.queryMatch(date)

        header = "Friday Night Block"

        tmpFile = '/tmp/blocksheet.pdf'

        pdf = PlaySheetFPDF(orientation='L', unit='in', format='Letter')
        pdf.set_font('Arial', '', 14);
        pdf.add_page()
        pdf.GenerateSheet(header, matchData)
        if os.path.exists(tmpFile):
            os.unlink(tmpFile)
        pdf.output(tmpFile)

        pdffile = FileWrapper(file(tmpFile))

        response = HttpResponse(pdffile, content_type='application/pdf')
        # response.write(pdf.output(dest="I"))
        #response['Content-Disposition'] = 'attachement; filename="BlockSheet.pdf"'

        return response


def blockSheetReportlab(request, date=None):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':

        mgr = TeamManager()

        matchData = mgr.queryMatch(date)
        season = get_current_season()


        gen = PlaySheet(num_courts=season.courts,num_matches=3)

        pdffile = gen.generate_sheet(header = "Friday Night Block",
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
