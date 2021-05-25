from re import split
from fpdf import FPDF
from PIL import Image
from matplotlib.pyplot import legend
from TransformData import col1_values, format_name, format_p_name, legend_name, legend_p_name, c_name, list_all_names, return_cnum, heatmap, data_elmA, data_elmD, data_elmDA, data_elmE, data_elmF, peerGrp_bgData, allVerif_bgData, peerGrp_category, peerGrp_dict, elmCA_indicatorData
from RetrievePhoto import display_cphoto, retrieve_filename
from PlotMap import plot_map, barGraph_labels, plot_barGraph
from FormatText import split_into_sentences, split_into_sentences_2
from ColorWheel import color_wheel


class PDF(FPDF):
    def header(self):
        self.set_margins(20, 5, 20)
        # Import Fonts
        self.add_font('Baskerville',
                      '',
                      './assets/fonts/Baskervville-Regular.ttf',
                      uni=True)
        self.add_font('BaskervilleLight',
                      '',
                      './assets/fonts/Baskerville-Light.ttf',
                      uni=True)
        self.add_font('BaskervilleItalic',
                      '',
                      './assets/fonts/Baskerville-Italic.ttf',
                      uni=True)
        self.add_font('BaskervilleBold',
                      '',
                      './assets/fonts/Baskerville-Bold.ttf',
                      uni=True)
        self.add_font('Optician-Sans',
                      '',
                      './assets/fonts/Optiker-K.ttf',
                      uni=True)
        self.add_font('Montserrat',
                      '',
                      './assets/fonts/Montserrat-Regular.ttf',
                      uni=True)
        self.add_font('MontserratItalic',
                      '',
                      './assets/fonts/Montserrat-Italic.ttf',
                      uni=True)
        self.add_font('MontserratBold',
                      '',
                      './assets/fonts/Montserrat-Bold.ttf',
                      uni=True)
        # self.set_y(10)
        self.set_font('BaskervilleItalic', '', 12)
        self.set_text_color(234)
        if self.page_no() != 1:
            self.cell(0, 10, "BlueMark Practice Verification Benchmark Report",
                      0, 0, 'R')
        self.ln(15)

    def footer(self):
        # Position at 1.5 cm from bottom
        self.image('./assets/images/foot.png', 0, 280, 211)
        self.set_y(-15)
        self.set_text_color(254)
        self.set_font('Baskerville', '', 8)
        # Page number
        self.cell(0, 10, 'Page ' + str(self.page_no()), 0, 0, 'C')

    def head(self, client_index, client_name, head_txt):
        self.add_page()
        # self.set_margins(20, 10, 20)
        self.image('./assets/images/head.png', 20, 20, 170)
        self.set_font('Montserrat', '', 7)
        self.set_text_color(254)
        self.text(151, 53, "P R E P A R E D  F O R")
        self.image(display_cphoto(client_index), 151, 55, w=26)
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

    def element_a(self, client_name, pg_name, score):
        self.set_text_color(254)
        if client_name[0] > 1:
            var1 = " ".join(client_name[1])
        else:
            var1 = str(client_name[1][0])
        var2 = pg_name
        var3 = 'All Verification Clients'
        self.set_xy(21, 118)
        self.set_draw_color(202, 206, 207)
        # self.rect(self.get_x() - 1, self.get_y() - 1, 170, 48, 'D')
        self.set_xy(21, self.get_y() + 5)
        self.set_text_color(16, 12, 110)
        self.set_font('Montserrat', '', 14)
        self.cell(168, 10, "A L I G N M E N T   S C O R E", 0, 2, 'C')
        self.ln(1)
        self.set_x(21)
        self.set_fill_color(239)
        self.set_text_color(17, 36, 74)
        self.set_font('Baskerville', '', 11)
        self.cell(56, 8, var1, 0, 0, 'C', True)
        self.cell(56, 8, var2, 0, 0, 'C', True)
        self.cell(56, 8, var3, 0, 2, 'C', True)
        self.set_font('MontserratBold', '', 30)
        self.set_text_color(3, 41, 83)
        self.set_x(21)
        self.set_fill_color(244)
        self.cell(56, 16, str(score[0]), 0, 0, 'C', True)
        self.cell(56, 16, str(score[1]), 0, 0, 'C', True)
        self.cell(56, 16, str(score[2]), 0, 0, 'C', True)
        '''
        self.set_x(45)
        self.cell(self.get_string_width(score1) + 6, 18, score1, 1, 0, 'C')
        self.set_x(100)
        self.cell(self.get_string_width(score2) + 6, 18, score2, 1, 0, 'C')
        self.set_x(-45-(self.get_string_width(score3) + 6))
        self.cell(self.get_string_width(score3) + 6, 18, score3, 1, 0, 'C')
        '''

    def element_b(self, client_name, pg_name, spider_map):
        self.image(spider_map, 44, 160, 120)
        self.set_font('Montserrat', '', 7)
        self.set_xy(145, 255)
        self.set_draw_color(255)
        self.set_fill_color(239)
        self.rect(self.get_x(), self.get_y(), 40, 14, 'D')
        self.set_draw_color(239)
        self.set_text_color(255)
        self.set_fill_color(74, 79, 108)
        self.cell(40, 5, client_name, 1, 1, 'C', True)
        self.set_fill_color(153, 155, 105)
        self.set_text_color(5)
        self.set_x(145)
        self.cell(40, 5, pg_name, 1, 1, 'C', True)
        self.set_fill_color(191, 142, 130)
        self.set_x(145)
        self.cell(40, 5, 'All Verification Clients', 1, 1, 'C', True)

    def element_c(self, title_c, txt_file_c, txt_file_c_bullet):
        self.add_page()
        caption = "Definition: Assess the expected impact of each investment based on a systematic approach."
        caption_split = caption.split()
        caption_1 = caption_split.pop(0)
        caption_all = ' '.join(caption_split)
        # self.set_margins(20, 10, 20)
        with open(txt_file_c, 'rb') as fh:
            txt_c = fh.read().decode(encoding='UTF-8')
        self.set_text_color(16, 12, 110)
        self.set_font('Baskerville', '', 22)
        self.write(8, title_c)
        self.ln(16)
        len_cap_1 = self.get_string_width(caption_1) - 19
        len_cap_2 = self.get_string_width(caption_all) + 0
        self.set_font('Montserrat', '', 9)
        self.set_text_color(3, 41, 83)
        self.cell(len_cap_1, 5, caption_1, ln=0, align='L')
        self.set_font('MontserratItalic', '', 9)
        self.cell(len_cap_2, 5, caption_all, ln=0, align='L')
        self.ln(7)
        # self.write(5, txt_c)
        self.set_font('Montserrat', '', 9)
        self.multi_cell(0, 5, txt_c, 0, 'J', False)
        self.ln(0)
        self.set_left_margin(25)
        self.bullet_text('number', split_into_sentences(txt_file_c_bullet))
        self.set_left_margin(20)
        self.ln(7.5)

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
        self.set_font('BaskervilleBold', '', 12)
        self.write(0, title_c_a)
        self.ln(8)
        self.set_text_color(3, 41, 83)
        self.set_font('Montserrat', '', 9)
        # self.write(5, txt_final)
        self.multi_cell(0, 5, txt_final, 0, 'J', False)
        self.ln(10)
        self.indicator_row(ls_labels=barGraph_labels("IndicatorLabels"),
                           data=ca_indData,
                           a="CA")
        self.ln(0)
        self.set_font_size(10)
        self.multi_cell(0, 5, txt_c_b, 0, 'J', False)
        self.ln(4)
        self.set_text_color(16, 12, 110)
        self.set_font('BaskervilleBold', '', 12)
        bg_title = 'Approaches to Assess Expected Impact'
        self.cell(170, 6, bg_title, 0, 2, 'C')
        self.image(barGraph_filename, 20, self.get_y() + 3, 170)

    def element_d(self, title_d, client_name, pg_name, txt_file_d, data):
        self.add_page()
        with open(txt_file_d, 'rb') as fh:
            txt_d = fh.read().decode(encoding='UTF-8')
        self.set_text_color(16, 12, 110)
        self.set_font('Baskerville', '', 22)
        self.write(8, title_d)
        self.ln(16)
        self.set_text_color(3, 41, 83)
        self.set_font('Montserrat', '', 9)
        # self.write(5, txt_d)
        self.multi_cell(0, 5, txt_d, 0, 'J', False)
        self.ln(10)
        self.display_table('tb1', client_name, pg_name, col1_values('d'), data)
        self.ln(12)

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
        # self.write(5, txt_d)
        self.multi_cell(0, 5, txt_d_a, 0, 'J', False)
        self.ln(12)
        self.set_text_color(16, 12, 110)
        self.set_font('BaskervilleBold', '', 12)
        self.set_font_size(12)
        self.write(0, 'Using all 5 IMP dimensions')
        self.ln(17)
        self.indicator_row(
            [c_name[1], pg_name[1], ['All Verification', 'Clients']], data_d_a,
            'DA')
        self.ln(10)

    def element_e(self, title_e, c_name, pg_name, txt_file_e, data_e):
        self.add_page()
        with open(txt_file_e, 'rb') as fh:
            txt_e = fh.read().decode(encoding='UTF-8')
        self.set_text_color(16, 12, 110)
        self.set_font('Baskerville', '', 16)
        self.set_font_size(22)
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
        self.ln(14)
        self.indicator_row(
            [c_name[1], pg_name[1], ['All Verification', 'Clients']], data_e,
            'E')
        self.ln(10)

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
        self.display_table('tb2', client_name, pg_name, col1_values('f'), data)
        self.set_text_color(3, 41, 83)

    def display_table(self, tb, client_name, pg_name, col1, data):
        self.set_left_margin(25)
        self.print_headrow(client_name, pg_name)
        for num, q, ea in zip(range(1, 6), col1, data):
            self.print_row(tb, num, q, ea)
        self.set_left_margin(20)

    def print_headrow(self, client_name, pg_name):
        self.set_font('Baskerville', '', 9)
        # self.set_stretching(90)
        self.set_draw_color(205, 205, 205)
        self.set_fill_color(249, 249, 249)
        self.set_text_color(44, 44, 44)
        self.cell(60, 15, '', 0, fill=False)
        if client_name[0] == 1:
            cl_n = str(client_name[1][0])
            self.cell(35, 15, cl_n, 1, align='C', fill=True)
        elif client_name[0] == 2:
            cl_n1 = str(client_name[1][0])
            if cl_n1 == 'Nuveen':
                cl_n2 = str(client_name[1][1]).strip('()')
            else:
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
            pg_n2 = str(pg_name[1][1]).strip('()')
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
        self.set_stretching(100)

    def print_row(self, tb, num, col1, row):
        # Individual Row
        self.set_x(20)  # Align Left
        self.set_y(self.get_y())  # Space to the next line
        # Font for Question Column
        self.set_text_color(0, 0, 0)
        self.set_font('Montserrat', '', 7)
        # self.write(3.3, ques) <- deleted code
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
        self.set_xy(self.get_x(), self.get_y() - 12)
        if row[0] == True:
            v1 = './assets/images/check_mark.png'
            self.cell(35, 12, '', 'LTB', align='C')
            self.image(v1, self.get_x() - 20, self.get_y() + 3, h=6)
        else:
            v1 = ''
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
        self.cell(35,
                  12,
                  '{0}%'.format(str(v3)),
                  'TBR',
                  2,
                  align='C',
                  fill=True)

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
            self.image(retrieve_filename(data[i], data_type, b),
                       k,
                       row - 7,
                       h=12)
            if isinstance(ls_labels[i], list):
                if len(ls_labels[i]) < 2:
                    self.text(k + t, row + 0.5, ls_labels[i][0])
                else:
                    j = 0
                    for ea in ls_labels[i]:
                        ea_text = str(ea.strip('()'))
                        self.text(k + t, row + (j * 4) - 1.75, ea_text)
                        j += 1
            i += 1
            b += 1
            if a == 'CA':
                k += 46.5
            else:
                k += 55
        self.ln(10)

    def bullet_text(self, ls_kind, txt_body):
        self.set_text_color(3, 41, 83)
        self.set_font('Montserrat', '', 9)
        for i, line_text in enumerate(txt_body, 1):
            self.set_x(self.get_x() + 5)
            if ls_kind == "number":
                self.write(5, str(i) + ". ")
            else:
                self.write(5, "- ")
            self.set_x(self.get_x() + 5)
            self.multi_cell(150, 5, line_text, 0, 'J', False)
            self.ln(0)


def produce_pdf(client_index, peerGrp_index):
    title = 'Practice Verification Client Benchmark Report'
    body = ''
    pdf = PDF()
    pdf.set_title(title)
    client_name = legend_name(client_index)
    format_name_array = format_name(client_index)
    format_p_name_array = format_p_name(peerGrp_index)
    pg_name = peerGrp_name(peerGrp_index)
    pg_indices = peerGrp_indices(peerGrp_index)
    pdf.head(client_index, format_name_array, "element_head.txt")
    pdf.element_a(format_name_array, pg_name,
                  data_elmA(client_index, pg_indices))
    pdf.element_b(client_name, pg_name,
                  plot_map(heatmap(client_index, pg_indices)))
    pdf.element_c('PRINCIPLE 4: EX-ANTE ASSESSMENT OF IMPACT', 'element_c.txt',
                  'element_c_bullet.txt')
    pdf.element_c_a(
        'Approach to assessing expected impact', format_name_array,
        elmCA_indicatorData(client_index), 'element_c_a.txt',
        'element_c_b.txt',
        plot_barGraph(pg_name, peerGrp_bgData(pg_indices), allVerif_bgData()))
    pdf.element_d('DIMENSIONS OF IMPACT INVESTMENT', format_name_array,
                  format_p_name_array, 'element_d.txt',
                  data_elmD(client_index, pg_indices))
    pdf.element_d_a('Does the Manager use all five IMP dimensions?',
                    format_name_array, format_p_name_array, 'element_d_a.txt',
                    data_elmDA(client_index, pg_indices))
    pdf.element_e('USE OF IMPACT INDICATORS', format_name_array,
                  format_p_name_array, 'element_e.txt',
                  data_elmE(client_index, pg_indices))
    pdf.element_f(format_name_array, format_p_name_array, 'element_f.txt',
                  data_elmF(client_index, pg_indices))
    pdf.set_author('BlueMark')
    pdf.output('./writePDF/static/001_sample.pdf')
    return "001_sample.pdf"


def client_list():
    ls = list_all_names()
    res_dct = {i: ls[i] for i in range(0, len(ls), 1)}
    return res_dct


def peerGrp_list():
    p_l2 = peerGrp_category()
    peer_dct = {i: p_l2[i] for i in range(0, len(p_l2), 1)}
    return peer_dct


def return_c_num(clnum):
    return return_cnum(clnum)


def peerGrp_name(pg_index):
    dicta = peerGrp_dict()[pg_index]
    for key in dicta:
        return key


def peerGrp_indices(pg_index):
    dicta = peerGrp_dict()[pg_index]
    for key in dicta:
        return dicta[key]
