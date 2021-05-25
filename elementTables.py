from fpdf import FPDF
from ColorWheel import color_wheel

questions = [
    'What is the intended impact?',
    ['Who experiences the intended', 'impact?'],
    ['How significant is the intended', 'impact?'],
    ['What is the likelihood of', 'achieving expected impact?'],
    'What are significant risk \nfactors that could result in \nvariance from expected impact?',
    'Other']

data = [
    [True, 95, 96],
    [False, 89, 91],
    [True, 97, 92],
    [False, 87, 88],
    [True, 93, 90],
    [False, 89, 86]
]


class PDF(FPDF):
    def head(self):
        self.add_page()
        self.set_margins(20, 20, 20)
        self.add_font('Baskervville', '', 'Baskervville-Regular.ttf', uni=True)
        self.add_font('BaskervilleBold', '', 'Baskerville-Bold.ttf', uni=True)
        self.add_font('Optician-Sans', '', 'Optiker-K.ttf', uni=True)
        self.display_table()

    def display_table(self):
        ''' Change the top_left coordinates of the table 
        self.set_x()
        self.set_y()'''
        self.print_headrow()
        for num, q, ea in zip(range(1, 7), questions, data):
            self.print_row(num, q, ea)

    def print_headrow(self):
        # Border = 1, No Border = 0
        self.set_font('BaskervilleBold', '', 9)
        self.set_stretching(90)
        self.set_draw_color(205, 205, 205)
        self.set_fill_color(249, 249, 249)
        self.set_text_color(44, 44, 44)
        self.cell(55, 15, '', 0, fill=False)
        self.cell(35, 15, 'FinDev Canada', 'LTB', align='C', fill=True)
        self.cell(35, 15, 'Peer Group', 'TB', align='C', fill=True)
        self.cell(35, 15, '', 'RTB', align='C', fill=True)
        value_x = self.get_x() - 29
        value_y = self.get_y() + 7
        self.text(value_x, value_y, 'All Verification')
        self.text(value_x + 6, value_y + 4, 'Clients')
        self.ln(15)
        self.set_stretching(100)

    def print_row(self, num, ques, row):
        # Individual Row
        self.set_x(20)  # Align Left
        self.set_y(self.get_y())  # Space to the next line
        # Font for Question Column
        self.set_text_color(0, 0, 0)
        self.set_font('Baskervville', '', 8)
        # self.write(3.3, ques) <- deleted code
        if num == 1 or num == 6:
            txt_h = 12
            ques_line = ques
        elif num == 5:
            txt_h = 4
            ques_line = ques
        else:
            txt_h = 12
            ques_line = ''
            self.text(self.get_x() + 1, self.get_y() + 5, ques[0])
            self.text(self.get_x() + 1, self.get_y() + 9, ques[1])
        # Question Data Cell
        self.multi_cell(55, txt_h, ques_line, 'LTB', align='L')
        # Font for Columns B, C & D
        self.set_font('arial', '', 9)
        # Values for Columns B, C & D
        if row[0] == True:
            v1 = 'Check'
        else:
            v1 = 'X'
        v2 = row[1]
        v3 = row[2]
        # Client Check/X Data Cell
        self.set_xy(self.get_x(), self.get_y() - 12)
        self.cell(35, 12, v1, 'LTB', align='C')
        # Fill Colors for Columns C & D
        c2 = color_wheel(v2)
        c3 = color_wheel(v3)
        # Peer Group Data Cell
        self.set_x(self.get_x())
        self.set_text_color(255, 255, 255)
        self.set_fill_color(c2[0], c2[1], c2[2])
        self.cell(35, 12, '{0}%'.format(str(v2)), 'TBR', align='C', fill=True)
        # All Verification Clients Data Cell
        self.set_x(self.get_x())
        self.set_text_color(255, 255, 255)
        self.set_fill_color(c3[0], c3[1], c3[2])
        self.cell(35, 12, '{0}%'.format(str(v3)),
                  'TBR', 2, align='C', fill=True)


'''
    def color_wheel(self, pour_cent):
        r_float = ((100 - pour_cent) * 1.4259259) + 16
        reds = math.floor(r_float)
        g_float = ((100 - pour_cent) * 1.189873418) + 42
        greens = math.floor(g_float)
        blues = 180 - pour_cent
        return [reds, greens, blues]
'''

pdf = PDF()
pdf.head()
pdf.output('element_table.pdf')
