from fpdf import FPDF
import os.path
import math
from django.contrib.staticfiles.storage import staticfiles_storage
from .plot import barGraph_labels, info_graph
from .format import split_into_sentences


class PDF(FPDF):
    # Page Header
    # includes loading fonts and header cell (except first page)
    def header(self, mock=True):
        self.set_margins(20, 5, 20)
        # Import Fonts
        self.add_font('Baskerville',
                      '',
                      staticfiles_storage.path(
                          "writePDF/fonts/Baskervville-Regular.ttf"),
                      uni=True)
        self.add_font(
            'BaskervilleLight',
            '',
            staticfiles_storage.path("writePDF/fonts/Baskerville-Light.ttf"),
            uni=True)
        self.add_font(
            'BaskervilleItalic',
            '',
            staticfiles_storage.path("writePDF/fonts/Baskerville-Italic.ttf"),
            uni=True)
        self.add_font(
            'BaskervilleBold',
            '',
            staticfiles_storage.path("writePDF/fonts/Baskerville-Bold.ttf"),
            uni=True)
        self.add_font('Optician-Sans',
                      '',
                      staticfiles_storage.path("writePDF/fonts/Optiker-K.ttf"),
                      uni=True)
        self.add_font(
            'Montserrat',
            '',
            staticfiles_storage.path("writePDF/fonts/Montserrat-Regular.ttf"),
            uni=True)
        self.add_font(
            'MontserratItalic',
            '',
            staticfiles_storage.path("writePDF/fonts/Montserrat-Italic.ttf"),
            uni=True)
        self.add_font(
            'MontserratBold',
            '',
            staticfiles_storage.path("writePDF/fonts/Montserrat-Bold.ttf"),
            uni=True)
        # self.set_y(10)
        self.set_font('BaskervilleItalic', '', 12)
        self.set_text_color(234)
        title = "Practice Verification Benchmark Report"
        if not mock:
            title = "Practice Verification Benchmark Report"
        if self.page_no() != 1:
            self.cell(0, 10, title, 0, 0, 'R')
        self.ln(15)

    # Page Footer
    # includes image and footer cell (Page Number)
    def footer(self, mock=True):
        # Position at 1.5 cm from bottom
        footer_file = "writePDF/mock/foot.png"
        if not mock:
            footer_file = "writePDF/images/foot.png"
        self.image(staticfiles_storage.path(footer_file), 0, 280, 211)
        self.set_y(-15)
        self.set_text_color(254)
        self.set_font('Baskerville', '', 8)
        # Page number
        self.cell(0, 10, 'Page ' + str(self.page_no()), 0, 0, 'C')

    # PAGE 1

    # Head: Title Design Block
    # includes images, Dynamic Paragraph, Floating Text
    def head(self, head_image, client_index, client_name, head_txt, mock):
        self.add_page()
        # self.set_margins(20, 10, 20)
        self.image(head_image, 20, 20, 170)
        self.set_font('Montserrat', '', 7)
        self.set_text_color(254)
        self.text(151, 53, "P R E P A R E D  F O R")
        self.image(self.display_cphoto(client_index, mock), 151, 55, w=26)
        if client_name[0] > 1:
            c_nam = " ".join(client_name[1])
        else:
            c_nam = str(client_name[1][0])
        with open(head_txt, 'rb') as fh:
            txt_h = fh.read().decode(encoding='UTF-8')
        txt_final = txt_h.replace("client_name", c_nam)
        self.set_font('Montserrat', '', 9)
        self.set_text_color(254)
        self.set_xy(25, 80)
        self.multi_cell(160, 4.5, txt_final, 0, 'J', False)
        self.ln(5)

    # Element A: Alignment Score Block
    # includes Title, Score Cells
    def element_a(self, client_name, pg_name, score):
        self.set_text_color(254)
        # client_name parameter is a list (refer to function in produce_pdf())
        if client_name[0] > 1:
            var1 = " ".join(client_name[1])
        else:
            var1 = str(client_name[1][0])
        var2 = pg_name
        var3 = 'All Verification Clients'
        self.set_xy(21, 118)
        self.set_draw_color(202, 206, 207)
        self.set_xy(21, self.get_y() + 5)
        self.set_text_color(16, 12, 110)
        self.set_font('Montserrat', '', 14)
        # Alignment Score Title Text
        self.cell(168, 10, "A L I G N M E N T   S C O R E", 0, 2, 'C')
        self.ln(1)
        self.set_x(21)
        self.set_fill_color(239)
        self.set_text_color(17, 36, 74)
        self.set_font('Baskerville', '', 11)
        # Score Cell Design
        self.cell(56, 8, var1, 0, 0, 'C', True)
        self.cell(56, 8, var2, 0, 0, 'C', True)
        self.cell(56, 8, var3, 0, 2, 'C', True)
        self.set_font('MontserratBold', '', 30)
        self.set_text_color(3, 41, 83)
        self.set_x(21)
        self.set_fill_color(244)
        # Score Cell Values
        self.cell(56, 16, str(score[0]), 0, 0, 'C', True)
        self.cell(56, 16, str(score[1]), 0, 0, 'C', True)
        self.cell(56, 16, str(score[2]), 0, 0, 'C', True)

    # Element B: Spider Graph
    # includes Spider Graph and Legend
    def element_b(self, client_name, pg_name, spider_map):
        self.image(spider_map, 44, 160, 120)
        self.set_font('Montserrat', '', 7)
        self.set_xy(145, 255)
        self.set_draw_color(255)
        self.set_fill_color(239)
        self.rect(self.get_x(), self.get_y(), 40, 14, 'D')
        # BLUES -
        self.set_text_color(10)
        self.set_fill_color(155, 160, 186)
        self.cell(40, 5, client_name, 1, 1, 'C', True)
        # GREEN -
        self.set_fill_color(220, 233, 209)
        self.set_x(145)
        self.cell(40, 5, pg_name, 1, 1, 'C', True)
        # RED -
        self.set_fill_color(224, 202, 196)
        self.set_x(145)
        self.cell(40, 5, 'All Verification Clients', 1, 1, 'C', True)

    # PAGE 2

    # Element C: Principle 4
    # includes Heading 1, Definition Box
    def element_c(self, title_c, txt_file_c, txt_file_c_bullet):
        self.add_page()
        caption = "Definition: Assess the expected impact of each investment based on a systematic approach."
        caption_split = caption.split()
        # Title: "Definition" is in regular font
        caption_1 = caption_split.pop(0)
        # The definition is in italic font
        caption_all = ' '.join(caption_split)
        with open(txt_file_c, 'rb') as fh:
            txt_c = fh.read().decode(encoding='UTF-8')
        self.set_text_color(16, 12, 110)
        self.set_font('Baskerville', '', 22)
        self.write(8, title_c)
        self.ln(16)
        self.set_draw_color(42, 26, 185)
        self.rect(22, self.get_y() - 3, 160, 38, 'D')
        self.set_left_margin(25)
        len_cap_1 = self.get_string_width(caption_1) - 19
        len_cap_2 = self.get_string_width(caption_all) + 0
        self.set_font('Montserrat', '', 9)
        self.set_text_color(42, 26, 185)
        self.cell(len_cap_1, 5, caption_1, ln=0, align='L')
        self.set_font('MontserratItalic', '', 9)
        self.cell(len_cap_2, 5, caption_all, ln=0, align='L')
        self.ln(7)
        self.set_font('Montserrat', '', 9)
        self.multi_cell(0, 5, txt_c, 0, 'J', False)
        self.ln(0)
        self.set_left_margin(25)
        self.bullet_text('number', split_into_sentences(txt_file_c_bullet))
        self.set_left_margin(20)
        self.ln(12.5)

    # Element C.A: Approach to Assessing Expected Impact
    # includes Heading 2, Dynamic Paragraph, Indicator Row, Static Paragraph, Heading 3
    #  and Bar Graph
    # barGraph_filename is the image file
    def element_c_a(self, title_c_a, client_name, ca_indData, txt_file_c_a,
                    txt_file_c_b, barGraph_filename):
        if client_name[0] > 1:
            c_nam = " ".join(client_name[1])
        else:
            c_nam = str(client_name[1][0])
        with open(txt_file_c_a, 'rb') as fh:
            txt_c_a = fh.read().decode(encoding='UTF-8')
        with open(txt_file_c_b, 'rb') as fh:
            txt_c_b = fh.read().decode(encoding='UTF-8')
        txt_final = txt_c_a.replace("client_name", c_nam)
        self.set_text_color(16, 12, 110)
        self.set_font('MontserratBold', '', 16)
        self.write(0, title_c_a)
        self.ln(12)
        self.set_text_color(3, 41, 83)
        self.set_font('Montserrat', '', 9)
        self.multi_cell(0, 5, txt_final, 0, 'J', False)
        self.ln(12)
        # indicator_row is the entire row of check boxes
        # barGraph_labels is the list of x-axis labels
        # ca_indData is the list of metrics specific for element "ca"
        # a is a string to identify the bar graph is specific for element "ca"
        self.indicator_row(ls_labels=barGraph_labels("IndicatorLabels"),
                           data=ca_indData,
                           a="CA")
        self.ln(2)
        self.set_font_size(9)
        self.multi_cell(0, 5, txt_c_b, 0, 'J', False)
        self.ln(6)
        self.set_text_color(16, 12, 110)
        self.set_font('BaskervilleBold', '', 12)
        bg_title = 'Approaches to Assess Expected Impact'
        self.cell(170, 6, bg_title, 0, 2, 'C')
        self.image(barGraph_filename, 30, self.get_y() + 3, 150)

    # PAGE 3

    # Element D: Dimensions of Impact Investment
    # includes Heading 2, Heading 3, Static Paragraph, Data Table
    def element_d(self, title_d, client_name, pg_name, txt_file_d, data):
        self.add_page()
        with open(txt_file_d, 'rb') as fh:
            txt_d = fh.read().decode(encoding='UTF-8')
        self.set_text_color(16, 12, 110)
        self.set_font('MontserratBold', '', 16)
        self.write(8, title_d)
        self.ln(16)
        self.set_text_color(3, 41, 83)
        self.set_font('Montserrat', '', 9)
        self.multi_cell(0, 5, txt_d, 0, 'J', False)
        self.ln(12)
        self.set_text_color(16, 12, 110)
        self.set_font('BaskervilleBold', '', 12)
        self.set_font_size(12)
        table_title = "Which of the following dimensions does the manager consider?"
        self.write(0, table_title)
        self.ln(10)
        # See function display_table below
        # tb1 is a string to define the question column that requires word wrapping
        # col1_values is a function calling a list specific to element "d"
        self.display_table('tb1', client_name, pg_name, self.col1_values('d'),
                           data)
        self.ln(12)

    # Element D.A: Using all Five Dimensions
    # includes Heading 3, Static Paragraph, Indicator Row
    def element_d_a(self, title_d_a, c_name, pg_name, txt_file_d_a, data_d_a):
        with open(txt_file_d_a, 'rb') as fh:
            txt_d_a = fh.read().decode(encoding='UTF-8')
        self.set_text_color(16, 12, 110)
        self.set_font('BaskervilleBold', '', 12)
        self.set_font_size(12)
        self.write(0, title_d_a)
        self.ln(12)
        self.set_text_color(3, 41, 83)
        self.set_font('Montserrat', '', 9)
        self.multi_cell(0, 5, txt_d_a, 0, 'J', False)
        self.ln(12)
        self.set_text_color(16, 12, 110)
        self.set_font('BaskervilleBold', '', 12)
        self.set_font_size(12)
        self.write(0, 'Using all five IMP dimensions')
        self.ln(17)
        self.indicator_row(
            [c_name[1], pg_name[1], ['All Verification', 'Clients']], data_d_a,
            'DA')
        self.ln(10)

    # PAGE 4

    # Element E: Use of Impact Indicators
    # includes Heading 2, Static Paragraph, Heading 3, Indicator Row
    def element_e(self, title_e, c_name, pg_name, txt_file_e, data_e):
        self.add_page()
        with open(txt_file_e, 'rb') as fh:
            txt_e = fh.read().decode(encoding='UTF-8')
        self.set_text_color(16, 12, 110)
        self.set_font('MontserratBold', '', 16)
        self.write(8, title_e)
        self.ln(16)
        self.set_text_color(3, 41, 83)
        self.set_font('Montserrat', '', 9)
        #self.write(5, txt_e)
        self.multi_cell(0, 5, txt_e, 0, 'J', False)
        self.ln(10)
        self.set_text_color(16, 12, 110)
        self.set_font('BaskervilleBold', '', 12)
        self.write(0, 'Using industry-aligned indicators')
        self.ln(17)
        self.indicator_row(
            [c_name[1], pg_name[1], ['All Verification', 'Clients']], data_e,
            'E')
        self.ln(10)

    # Element F: Most Commonly Used Indicator Standards
    # includes Heading 3, Static Paragraph, Data Table
    def element_f(self, client_name, pg_name, txt_file_f, data):
        with open(txt_file_f, 'rb') as fh:
            txt_f = fh.read().decode(encoding='UTF-8')
        self.set_text_color(16, 12, 110)
        self.set_font('BaskervilleBold', '', 12)
        self.write(0, 'Most commonly used indicator standards')
        self.ln(10)
        self.set_text_color(3, 41, 83)
        self.set_font('Montserrat', '', 9)
        # self.write(5, txt_f)
        self.multi_cell(0, 5, txt_f, 0, 'J', False)
        self.ln(15)
        self.display_table('tb2', client_name, pg_name, self.col1_values('f'),
                           data)
        self.set_text_color(3, 41, 83)

    # Functions for Data Tables

    # Function to display table, calls for print_headrow and print_rows
    def display_table(self, tb, client_name, pg_name, col1, data):
        self.set_left_margin(25)
        self.print_headrow(client_name, pg_name)
        for num, q, ea in zip(range(1, 6), col1, data):
            self.print_row(tb, num, q, ea)
        self.set_left_margin(20)

    # Function for Header Row
    def print_headrow(self, client_name, pg_name):
        self.set_font('Baskerville', '', 9)
        self.set_draw_color(205, 205, 205)
        self.set_fill_color(249, 249, 249)
        self.set_text_color(44, 44, 44)
        self.cell(60, 15, '', 0, fill=False)
        if client_name[0] == 1:
            cl_n = str(client_name[1][0])
            self.cell(35, 15, cl_n, 1, align='C', fill=True)
        elif client_name[0] == 2:
            cl_n1 = str(client_name[1][0])
            # if cl_n1 == 'Nuveen':
            #     cl_n2 = str(client_name[1][1])  #.strip('()')
            # else:
            cl_n2 = str(client_name[1][1])
            str_L1 = (35 - self.get_string_width(cl_n1)) / 2
            str_L2 = (35 - self.get_string_width(cl_n2)) / 2
            self.cell(35, 15, ' ', 1, fill=True)
            value_x = self.get_x() - 35
            value_y = self.get_y() + 6.5
            self.text(value_x + str_L1, value_y, cl_n1)
            self.text(value_x + str_L2, value_y + 4, cl_n2)
        else:
            self.cell(35, 15, 'Your Score', 1, align='C', fill=True)
        if pg_name[0] == 1:
            pg_n = str(pg_name[1][0])
            self.cell(35, 15, pg_n, 1, align='C', fill=True)
        elif pg_name[0] == 2:
            pg_n1 = str(pg_name[1][0])
            pg_n2 = str(pg_name[1][1])  #.strip('()')
            str_PG1 = (35 - self.get_string_width(pg_n1)) / 2
            str_PG2 = (35 - self.get_string_width(pg_n2)) / 2
            self.cell(35, 15, '', 1, fill=True)
            pvalue_x = self.get_x() - 35
            pvalue_y = self.get_y() + 6.5
            self.text(pvalue_x + str_PG1, pvalue_y, pg_n1)
            self.text(pvalue_x + str_PG2, pvalue_y + 4, pg_n2)
        else:
            self.cell(35, 15, 'Peer Group', 1, align='C', fill=True)
        self.cell(35, 15, '', 1, align='C', fill=True)
        value_x = self.get_x() - 29
        value_y = self.get_y() + 6.5
        self.text(value_x, value_y, 'All Verification')
        self.text(value_x + 6, value_y + 4, 'Clients')
        self.ln(15)

    # Function for Remaining Rows
    def print_row(self, tb, num, col1, row):
        # Individual Row
        self.set_x(20)  # Align Left
        self.set_y(self.get_y())  # Space to the next line
        # Font for Question Column
        self.set_text_color(0, 0, 0)
        self.set_font('Montserrat', '', 7)
        if tb == 'tb1':
            if num == 1 or num == 2 or num == 3:
                txt_h = 12
                col1_line = col1
            else:
                txt_h = 12
                col1_line = ''
                self.text(self.get_x() + 3, self.get_y() + 5, col1[0])
                self.text(self.get_x() + 3, self.get_y() + 9, col1[1])
        else:
            txt_h = 12
            col1_line = col1
        # Column A Data Cell
        self.multi_cell(60,
                        txt_h,
                        '   {0}'.format(col1_line),
                        'LTB',
                        align='L')
        # Font for Columns B, C & D
        self.set_font('Montserrat', '', 9)
        # Values for Columns B, C & D
        v2 = row[1]
        v3 = row[2]
        # Client Check/X Data Cell
        self.set_xy(self.get_x() + 60, self.get_y() - 12)
        if row[0] == True:
            v1 = staticfiles_storage.path("writePDF/images/check_mark.png")
            self.cell(35, 12, '', 'LTB', align='C')
            self.image(v1, self.get_x() - 20, self.get_y() + 3, h=6)
        else:
            v1 = ''
            self.cell(35, 12, v1, 'LTB', align='C')
        # Fill Colors for Columns C & D
        c2 = self.color_wheel(v2)
        c3 = self.color_wheel(v3)
        # Peer Group Data Cell
        self.set_x(self.get_x())
        self.set_text_color(255, 255, 255)
        self.set_fill_color(c2[0], c2[1], c2[2])
        self.cell(35, 12, '{0}%'.format(str(v2)), 'TBR', align='C', fill=True)
        # All Verification Clients Data Cell
        self.set_x(self.get_x())
        self.set_text_color(255, 255, 255)
        self.set_fill_color(c3[0], c3[1], c3[2])
        self.cell(35,
                  12,
                  '{0}%'.format(str(v3)),
                  'TBR',
                  2,
                  align='C',
                  fill=True)

    # Function to displayt indicator_row

    def indicator_row(self, ls_labels, data, a):
        row = self.get_y()
        self.set_font('Montserrat', '', 12)
        self.set_font_size(10)
        i = 0
        b = 0
        k = 20
        t = 17.5
        # Added variable `b` for unique filenames
        #element_DA
        if a == 'DA':
            b = i
        #element_E
        elif a == 'E':
            b = i + 10
        elif a == 'CA':
            b = i + 20
            k = 14
            self.set_font_size(8)
            t = 16
        #add more `elif`s for other indicator rows
        else:
            b = i + 30
        while i < len(ls_labels):
            data_type = type(data[i])
            self.image(self.retrieve_filename(data[i], data_type, b),
                       k,
                       row - 7,
                       h=12)
            if isinstance(ls_labels[i], list):
                if len(ls_labels[i]) < 2:
                    self.text(k + t, row + 0.5, ls_labels[i][0])
                else:
                    j = 0
                    for ea in ls_labels[i]:
                        ea_text = str(ea)  #.strip('()')
                        self.text(k + t, row + (j * 4) - 1.75, ea_text)
                        j += 1
            i += 1
            b += 1
            if a == 'CA':
                k += 46.5
            else:
                k += 55
        self.ln(10)

    # Function for bulleted text (Definition Box)

    def bullet_text(self, ls_kind, txt_body):
        self.set_font('Montserrat', '', 9)
        for i, line_text in enumerate(txt_body, 1):
            self.set_x(self.get_x() + 5)
            if ls_kind == "number":
                self.write(5, str(i) + ". ")
            else:
                self.write(5, "- ")
            self.set_x(self.get_x() + 5)
            self.multi_cell(140, 5, line_text, 0, 'J', False)
            self.ln(0)

    def col1_values(self, element_letter):
        if element_letter == 'd':
            return [
                'What is the intended impact?',
                'Who experiences the intended impact?',
                'How significant is the intended impact?',
                ['What is the likelihood of achieving', 'expected impact?'],
                [
                    'What are significant risk factors that could',
                    'result in variance from expected impact?'
                ]
            ]
        elif element_letter == 'f':
            return ["HIPSO", "IRIS", "GIIRS", "GRI", "Other"]
        else:
            return ['empty', 'empty', 'empty', 'empty', 'empty']

    def display_cphoto(self, c_num, mock):
        if mock:
            filename = staticfiles_storage.path(
                "writePDF/mock/client/cphoto_{0}.png".format(str(c_num)))
            if os.path.exists(filename):
                return filename
            else:
                return staticfiles_storage.path(
                    "writePDF/mock/client/c_photo_temp.png")
        else:
            filename = staticfiles_storage.path(
                "writePDF/images/client/cphoto_{0}.png".format(str(c_num)))
            if os.path.exists(filename):
                return filename
            else:
                return staticfiles_storage.path(
                    "writePDF/images/client/c_photo_temp.png")

    def retrieve_filename(self, check, data_type, i):
        if data_type is int:
            filename = info_graph(check, i)
            return filename
        elif check == True:
            return staticfiles_storage.path(
                "writePDF/images/check_box_True.png")
        elif check == False:
            return staticfiles_storage.path(
                "writePDF/images/check_box_False.png")
        else:
            filename = info_graph(check, i)
            return filename

    def color_wheel(self, pour_cent):
        r_float = ((100 - pour_cent) * 1.4259259) + 16
        reds = math.floor(r_float)
        g_float = ((100 - pour_cent) * 1.189873418) + 42
        greens = math.floor(g_float)
        blues = 180 - pour_cent
        return [reds, greens, blues]
