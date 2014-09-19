from io import BytesIO

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter,landscape
from reportlab.lib.units import cm, inch
from reportlab.pdfbase.pdfmetrics import stringWidth


class PlaySheet(object):
    def __init__(self, **kwargs):
        super(PlaySheet, self).__init__()

        self.marginLeft = 0.25
        self.marginTop = 0.25
        self.pageWidth = 11 - 2 * self.marginLeft

        self.num_courts = kwargs.get('num_courts',3)
        self.num_matches = kwargs.get('num_matches',3)

        self.pagesize = landscape(letter)
        self.buffer = BytesIO()
        self.canvas = canvas.Canvas(self.buffer,
                                    pagesize=self.pagesize)

    @property
    def width(self):
        return self.pagesize[0]

    @property
    def height(self):
        return self.pagesize[1]

    def setFillColorRGB(self,r,g,b,alpha=None):
        """
        Translate the ColorPicker values (0-255) to the Reportlab
        values, 0-1
        """
        self.canvas.setFillColorRGB(r/255.0,g/255.0,b/255.0,alpha)

    def setStrokeColorRGB(self,r,g,b,alpha=None):
        """
        Translate the ColorPicker values (0-255) to the Reportlab
        values, 0-1
        """
        self.canvas.setStrokeColorRGB(r/255.0,g/255.0,b/255.0,alpha)

    def setTextColor(self,r,g,b,alpha=None):
        """
        Translate the ColorPicker values (0-255) to the Reportlab
        values, 0-1
        """
        self.canvas.setStrokeColorRGB(r/255.0,g/255.0,b/255.0,alpha)
        self.canvas.setFillColorRGB(r/255.0,g/255.0,b/255.0,alpha)


    def get_sheet_params(self):

        w = self.width
        h = self.height
        margin = 0.5*inch

        w_inner = w-(2*margin)
        h_inner = h-(2*margin)

        h_header = 0.5*inch

        w_block = w_inner/float(self.num_courts)
        h_block = (h_inner-h_header)/float(self.num_matches)

        return w,h,margin,w_inner,h_inner,h_header,w_block,h_block


    def generate_sheet(self, header="Friday Night Block", firstcourt=1,sched=None):

        c = self.canvas
        c.setFont('Helvetica',14)

        c.setTitle(header)

        self.setStrokeColorRGB(76,56,75)
        self.setFillColorRGB(255,255,255)

        self.draw_borders(c)

        w,h,margin,w_inner,h_inner,h_header,w_block,h_block = self.get_sheet_params()

        tx,ty = margin,margin+h_inner-h_header
        c.translate(tx,ty)
        self.setTextColor(57,57,57)
        c.setFont('Helvetica',24)
        c.drawCentredString(w_inner/2,0.1*inch,header)
        c.resetTransforms()

        self.setTextColor(57,57,57)
        c.setFont('Helvetica',14)
        for n,set in enumerate(sched):

            for m,match in enumerate(set):

                tx,ty = margin+w_block*m,margin+h_block*n
                c.translate(tx,ty)
                self.draw_match(match,w_block,h_block)
                c.resetTransforms()

                tx,ty = margin+w_block*m, margin+n*h_block+h_block-h_header
                c.translate(tx,ty)
                c.drawCentredString(w_block/2,0.2*inch,"Court {}".format(m+firstcourt))
                c.resetTransforms()


        c.showPage()
        c.save()

        pdffile = self.buffer.getvalue()
        self.buffer.close()
        return pdffile

    def draw_borders(self,c):
        """
        Draw the borders.
        """

        w,h,margin,w_inner,h_inner,h_header,w_block,h_block = self.get_sheet_params()

        # Border
        c.rect(margin,margin,w_inner,h_inner,fill=0)

        # Header Border
        self.setFillColorRGB(209,251,255)
        c.rect(margin,margin+h_inner-h_header,w_inner,h_header,fill=1)

        # Draw Blocks
        self.setFillColorRGB(204,204,204)
        c.saveState()
        c.translate(margin,margin)
        for n in range(0,self.num_matches):
            for m in range(0,self.num_courts):
                self.setFillColorRGB(204,204,204)
                c.rect(m*w_block,n*h_block,w_block,h_block,fill=1)
                self.setFillColorRGB(206,254,242)
                c.rect(m*w_block,n*h_block+h_block-h_header,w_block,h_header,fill=1)

        c.restoreState()
        #c.translate(-margin,-margin)

    def draw_match(self, match, width,heigth):
        """
        Draw the match in the box.. already translated.
        """
        c = self.canvas

        lineheight = 0.25*inch

        x = width/2.0
        y = 0.1*inch

        c.drawCentredString(x, y, match['team2']['f']['name'])
        y += lineheight
        c.drawCentredString(x, y, match['team2']['m']['name'])
        y += lineheight*2
        c.drawCentredString(x, y, '----- versus -----')
        y += lineheight*2
        c.drawCentredString(x, y, match['team1']['f']['name'])
        y += lineheight
        c.drawCentredString(x, y, match['team1']['m']['name'])











