from fpdf import FPDF

class PlaySheet(FPDF):
    """
    Create the tennisblock sheet using the FPDF library.

    deprecated.. the reportlab works much better.
    """
    def __init__(self, **kwargs):
        super(PlaySheet, self).__init__(**kwargs)

        self.marginLeft = 0.25
        self.marginTop = 0.25
        self.pageWidth = 11 - 2 * self.marginLeft

    def GenerateSheet(self, header, sched):

        self.set_margins(self.marginLeft, self.marginTop)

        self.set_font('Arial', 'B', 13)
        self.set_xy(0, 0.5)
        self.cell(0, 0, header, 0, 1, 'C')

        matchTitleHeight = 0.4
        matchHeight = (7.0 / float(len(sched[0])))
        matchY = 1.2
        matchNum = 1

        for set in sched:
            x = self.marginLeft
            self.set_fill_color(0, 0xcc, 0xff)
            self.set_margins(0, 0)
            self.set_xy(self.marginLeft, matchY)
            self.cell(w=self.pageWidth, h=matchTitleHeight, txt="Match %d" % matchNum,
                      border=1, ln=1, align='C', fill=True)

            cellWidth = self.pageWidth / float(len(set))
            cellHeight = (matchHeight - matchTitleHeight) / 5
            crtidx = 1
            for match in set:
                self.outputMatch(match,
                                 crtidx,
                                 self.marginLeft,
                                 matchY + matchTitleHeight,
                                 cellWidth,
                                 cellHeight - 0.05)
                crtidx += 1

            matchY += matchHeight
            matchNum += 1

    def outputMatch(self, match, crtidx, marginLeft, matchY, cellWidth, cellHeight):

        x = marginLeft + cellWidth * (crtidx - 1)
        y = matchY
        # self.rect(x,y,cellWidth,0.4*5)
        self.set_left_margin(x - 0.5)
        self.set_fill_color(0xff, 0xfd, 0xd0)

        lineHeight = 0.20
        self.set_xy(x, y)
        self.cell(cellWidth, cellHeight, "Court %d" % crtidx, 1, 1, 'C', 1)
        self.rect(x, self.get_y(), cellWidth, 6 * lineHeight + 0.2)

        x += 0.4
        y += cellHeight + 0.4
        self.centerText(x, y, cellWidth, match['team1']['m']['name'])
        y += lineHeight
        self.centerText(x, y, cellWidth, match['team1']['f']['name'])

        y += lineHeight
        self.centerText(x, y, cellWidth, '----- versus -----')

        y += lineHeight
        self.centerText(x, y, cellWidth, match['team2']['m']['name'])
        y += lineHeight
        self.centerText(x, y, cellWidth, match['team2']['f']['name'])

    def centerText(self, x, y, width, text):
        print("StringWidth:%f" % self.get_string_width(text))
        self.text(
            x,
            y,
            text
        )








