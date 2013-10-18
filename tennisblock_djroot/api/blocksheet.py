# Create your views here.

from django.http import HttpResponse
from django.core.servers.basehttp import FileWrapper

import os
from fpdf import FPDF
from TBLib.teams import TeamManager


class PlaySheet(FPDF):
    
    def __init__(self,**kwargs):
        super(PlaySheet,self).__init__(**kwargs)

        self.marginLeft =0.25
        self.marginTop = 0.25
        self.pageWidth= 11-2*self.marginLeft

    def GenerateSheet(self,header,sched):

        self.set_margins(self.marginLeft,self.marginTop)

        self.set_font('Arial','B', 15)
        self.set_xy(0,0.5)
        self.cell(0,0,header,0,1,'C')

        matchTitleHeight = 0.4
        matchHeight = (7.0/float(len(sched[0])))-0.5
        matchY = 0.75
        matchNum = 1

        for set in sched:
            x = self.marginLeft
            self.set_fill_color(0,0xcc,0xff)
            self.set_margins(0,0)
            self.set_xy(self.marginLeft,matchY)
            self.cell(w=self.pageWidth,h=matchTitleHeight,txt="Match %d" % matchNum,
                      border=1,ln=1,align='C',fill=True)

            cellWidth = self.pageWidth/float(len(set))
            cellHeight = (matchHeight-matchTitleHeight)/5
            crtidx = 1
            for match in set:
                self.outputMatch(match,
                                 crtidx,
                                 self.marginLeft,
                                 matchY+matchTitleHeight,
                                 cellWidth,
                                 cellHeight-0.05)
                crtidx += 1

            matchY += matchHeight
            matchNum += 1

    def outputMatch(self,match,crtidx,marginLeft,matchY,cellWidth,cellHeight):

        x = marginLeft+cellWidth*(crtidx-1)
        y = matchY
        #self.rect(x,y,cellWidth,0.4*5)
        self.set_left_margin(x-0.5)
        self.set_xy(x,y)
        self.set_fill_color(0xff,0xfd,0xd0)

        self.cell(cellWidth,cellHeight,"Court %d" % crtidx,1,1,'C',1)

        lineHeight = 0.25

        y += lineHeight
        self.centerText(x,y,cellWidth,match['team1']['m']['name'])
        y += lineHeight
        self.centerText(x,y,cellWidth,match['team1']['f']['name'])

        y += lineHeight
        self.centerText(x,y,cellWidth,match['team2']['m']['name'])
        y += lineHeight
        self.centerText(x,y,cellWidth,match['team2']['f']['name'])

    def centerText(self,x,y,width,text):
        print("StringWidth:%f" % self.get_string_width(text))
        self.text(
            x+width/2-self.get_string_width(text),
            y,
            text
        )


def blockSheet(request,date=None):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':

        mgr = TeamManager()

        matchData = mgr.queryMatch(date)

        header = "Friday Night Block"

        tmpFile = '/tmp/blocksheet.pdf'

        pdf = PlaySheet(orientation='L',unit='in',format='Letter')
        pdf.set_font('Arial','',14);
        pdf.add_page()
        pdf.GenerateSheet(header,matchData)
        if os.path.exists(tmpFile):
            os.unlink(tmpFile)
        pdf.output(tmpFile)

        pdffile = FileWrapper(file(tmpFile))

        response = HttpResponse(pdffile,content_type='application/pdf')
        #response.write(pdf.output(dest="I"))
        #response['Content-Disposition'] = 'attachement; filename="BlockSheet.pdf"'

        return response


def main():

    mgr = TeamManager()

    matchData = mgr.queryMatch()

    header = "Friday Night Block"

    tmpFile = '/tmp/blocksheet.pdf'

    pdf = PlaySheet(orientation='L',unit='in',format='Letter')
    pdf.set_font('Arial','',14);
    pdf.add_page()
    pdf.GenerateSheet(header,matchData)
    if os.path.exists(tmpFile):
        os.unlink(tmpFile)
    pdf.output(tmpFile)

if __name__ == '__main__':
    main()
