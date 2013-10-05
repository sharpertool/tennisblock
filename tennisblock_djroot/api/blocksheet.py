# Create your views here.

import datetime
from dateutil import parser
from django.http import HttpResponse
from django.core.servers.basehttp import FileWrapper
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view
from rest_framework import serializers

from apiutils import JSONResponse, _getBlockSchedule

import os
from fpdf import FPDF
from reportlab.pdfgen import canvas


def blockSchedule(request):

    sched = _getBlockSchedule()

    return JSONResponse(sched)

class PlaySheet(FPDF):
    
    def __init__(self,*args):
        super(PlaySheet,self).__init__(*args)
        
    def GenerateSheet(self,header,sched):
        self.set_margins(0.25,0)
        self.set_font('Arial','B', 15)
        self.set_y(0.5)
        self.cell(0,0.25,header,0,1,'C')

        match_height = 0.25
        match = 1

        sets = sorted(sched['sets'])
        crts = sorted(sched['courts'])
        for set in sets:
            x = 0.25
            y = 0.75+(0.4*5+match_height)*(set-1)
            self.set_xy(x,y)
            self.set_left_margin(0.25)
            self.set_fill_color(0,0xcc,0xff)
            self.cell(10.5,match_height,"Match %d" % set,1,1,'C',1)

            cellWidth = 10.5/len(crts)
            for crt in crts:
                match = sched['sched'][set][crt]
                x = 0.25+cellWidth*(crt-1)
                y = 1+(0.4*5+match_height)*(set-1)
                self.rect(x,y,cellWidth,0.4*5)
                self.set_left_margin(x-0.5)
                self.set_xy(x,y)
                self.set_fill_color(0xff,0xfd,0xd0)

                self.cell(cellWidth,0.25,"Court %d" % crt,1,1,'C',1)

                self.set_xy(x,y+0.3)
                #self.set_y(y+0.3)
                self.cell(cellWidth,0.25,match['ta']['guy']['name'],0,1,'C',0)
                self.cell(cellWidth,0.25,match['ta']['gal']['name'],0,1,'C',0)

                self.cell(cellWidth,0.15,'vs.','LRTB',1,'C',0)
                self.cell(cellWidth,0.25,match['tb']['guy']['name'],0,1,'C',0)
                self.cell(cellWidth,0.25,match['tb']['gal']['name'],0,1,'C',0)



def blockSheet(request):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':

        sched = _getBlockSchedule()

        header = "Friday Night Block"

        tmpFile = '/tmp/blocksheet.pdf'

        pdf = PlaySheet('L','in','Letter')
        pdf.set_font('Arial','',14);
        pdf.add_page()
        pdf.GenerateSheet(header,sched)
        os.unlink(tmpFile)
        pdf.output(tmpFile)

        pdffile = FileWrapper(file(tmpFile))

        response = HttpResponse(pdffile,content_type='application/pdf')
        response.write(pdf.output(dest="I"))
        #response['Content-Disposition'] = 'attachement; filename="BlockSheet.pdf"'

        return response

