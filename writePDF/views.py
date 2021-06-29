import pandas as pd
import numpy as np
import math
import os
from pathlib import Path
#from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.staticfiles.storage import staticfiles_storage
from django.conf import settings
from .cleandata import clean_s1_df1, clean_s1_df2, clean_s2_df1
from .pdf import PDF
from .plot import plot_map, plot_barGraph


# Create your views here.
def home_view(request, *args, **kwargs):
    userName = request.user.username
    mock_bool = True
    if userName == "geanu" or userName == "bluemark":
        mock_bool = False
    stat_dict = load_stat(mock_bool)
    c_1 = clean_s1_df1(pd.read_csv(stat_dict["df1"]))
    c_2 = clean_s1_df2(pd.read_csv(stat_dict["df1"]))
    c_3 = clean_s2_df1(pd.read_csv(stat_dict["df2"]))
    list_dict = load_list(c_1, c_3)

    if request.user.is_authenticated:
        con = {
            "user_name": userName,
            "c_list": list_dict["c_dict"],
            "p_list": list_dict["p_dict"]
        }
        if request.method == "POST":
            client_index = request.POST.get('client_id')
            peerGrp_index = request.POST.get('peerGrp_id')
            output_file = pdf_production(stat=stat_dict,
                                         elem=elem_dict(
                                             c_num=int(client_index),
                                             p_num=int(peerGrp_index),
                                             c_1=c_1,
                                             c_2=c_2,
                                             c_3=c_3),
                                         c_num=int(client_index))
        return render(request, "home.html", con)
    else:
        print("Log in required.")
        return redirect("/login")


def load_stat(mock):
    df1_url = "writePDF/data/verifAll.csv"
    df2_url = "writePDF/data/verifP4.csv"
    if settings.DEBUG == True:
        output_url = os.path.join(
            settings.BASE_DIR, "writePDF/static/writePDF/data/output_doc.pdf")
    else:
        staticfiles_storage.path("writePDF/data/output_doc.pdf")
    if mock == True:
        df1_url = "writePDF/data/mockAll.csv"
        df2_url = "writePDF/data/mockP4.csv"
    return {
        "df1":
        staticfiles_storage.path(df1_url),
        "df2":
        staticfiles_storage.path(df2_url),
        "output":
        output_url,
        "elemHeadtxt":
        staticfiles_storage.path("writePDF/data/element_head.txt"),
        "elemCtxt":
        staticfiles_storage.path("writePDF/data/element_c.txt"),
        "elemCbullettxt":
        staticfiles_storage.path("writePDF/data/element_c_bullet.txt"),
        "elemCAtxt":
        staticfiles_storage.path("writePDF/data/element_c_a.txt"),
        "elemCBtxt":
        staticfiles_storage.path("writePDF/data/element_c_b.txt"),
        "elemDtxt":
        staticfiles_storage.path("writePDF/data/element_d.txt"),
        "elemDAtxt":
        staticfiles_storage.path("writePDF/data/element_d_a.txt"),
        "elemEtxt":
        staticfiles_storage.path("writePDF/data/element_e.txt"),
        "elemFtxt":
        staticfiles_storage.path("writePDF/data/element_f.txt"),
    }


def load_list(c1, c3):
    ls = c1.loc[:, "Client"].tolist()
    c_dict = {i: ls[i] for i in range(0, len(ls), 1)}
    p_l = c3.loc[:, "InvestorType"]
    p_l2 = p_l.value_counts().index
    p_list = list()
    for each in p_l2:
        a = each
        if "Manager" in each:
            a = each.replace("Manager", "Managers")
        if "Allocator" in each:
            a = each.replace("Allocator", "Allocators")
        p_list.append(a)
    p_dict = {i: p_list[i] for i in range(0, len(p_list), 1)}
    return {"c_dict": c_dict, "p_dict": p_dict}


def elem_dict(c_num, p_num, c_1, c_2, c_3):
    def pg_dict():
        piv = c_3.loc[:, ["Client", "InvestorType"]]
        col1 = piv.iloc[:, 1]
        cols = col1.value_counts().reset_index()
        col = cols["index"]
        piv = piv.reset_index()
        piv2 = piv.pivot(columns="InvestorType", values="index")
        piv2 = piv2[col]
        dicta = dict()
        keysa = range(len(piv2.columns))
        for each in keysa:
            serie = piv2.iloc[:, each].squeeze().dropna().astype(int)
            if "Manager" in serie.name:
                serie.name = serie.name.replace("Manager", "Managers")
            if "Allocator" in serie.name:
                serie.name = serie.name.replace("Allocator", "Allocators")
            dicta[each] = {serie.name: serie.to_list()}
        return dicta

    def pg_name(p_num):
        dicta = pg_dict()[p_num]
        for key in dicta:
            return key

    def pg_list(p_num):
        dicta = pg_dict()[p_num]
        for key in dicta:
            return dicta[key]

    p_list = pg_list(p_num)

    elmA_head = ["Client", "Alignment Score"]
    elmB_head = [
        "Principle 1", "Principle 2", "Principle 3", "Principle 4",
        "Principle 5", "Principle 6", "Principle 7", "Principle 8"
    ]
    elmCA_head = ["4C.a.i", "4C.a.ii", "4C.a.v", "4C.a.vi"]
    elmD_head = ["4F_i", "4F_ii", "4F_iii", "4F_iv", "4F_v"]
    elmDA_head = ["Client", "4Fv.a.ii"]
    elmE_head = ["Client", "4E"]
    elmF_head = ["HIPSO", "IRIS", "GIIRS", "GRI", "Other"]
    refeLMHD = {'LOW': 1, 'MODERATE': 2, 'HIGH': 3, 'ADVANCED': 4, 'N/A': 0}
    refeYN = {'Yes': 100, 'No': 0}
    refeTF = {'Yes': True, 'No': False}
    refeXB = {'x': 100, '(blank)': 0}
    refeXB_bool = {'x': True, '(blank)': False}

    def pg_cat():
        p_l = c_3.loc[:, "InvestorType"]
        p_l2 = p_l.value_counts().index
        ls = list()
        for each in p_l2:
            a = each
            if "Manager" in each:
                a = each.replace("Manager", "Managers")
            if "Allocator" in each:
                a = each.replace("Allocator", "Allocators")
            ls.append(a)
        return ls

    def client_list():
        ls = c_1.loc[:, "Client"].tolist()
        res_dct = {i: ls[i] for i in range(0, len(ls), 1)}
        return res_dct

    def peerGrp_list():
        p_l2 = pg_cat()
        peer_dct = {i: p_l2[i] for i in range(0, len(p_l2), 1)}
        return peer_dct

    def c_name(c_num):
        namesung = str(c_1.loc[c_num, "Client"])
        if c_num == 19 or c_num == 20:
            nameList = namesung.split()
            nameList.remove('-')
            namesung = " ".join(nameList)
        return namesung

    def format_name(c_num):
        sp = " "
        grp1 = [28]
        grp2 = [2, 17, 26, 27]
        grp3 = [19, 20]
        a_txt = c_name(c_num)
        num_lines = 2
        name_list = a_txt.split()
        year = name_list.pop(-1)
        word_count = len(name_list)
        name_listed = list()
        if word_count > 2:
            if c_num in grp1:
                name_listed.append(
                    sp.join([str(name_list[0]),
                             str(name_list[1])]))
                name_listed.append(
                    sp.join([str(name_list[2]),
                             str(name_list[3])]))
            elif c_num in grp2:
                name_listed.append(
                    sp.join([str(name_list[0]),
                             str(name_list[1])]))
                name_listed.append(name_list[2])
            elif c_num in grp3:
                name_listed.append(name_list[0])
                name_listed.append("({0} {1})".format(name_list[1],
                                                      name_list[2]))
            else:
                name_listed = [sp.join(name_list)]
                num_lines = 1
        elif word_count <= 2:
            name_listed = [sp.join(name_list)]
            num_lines = 1
        else:
            name_listed = ['Your Score']
            num_lines = 1
        return [num_lines, name_listed, year]

    def format_p_name(pg_index):
        sp = " "
        name = pg_cat()[pg_index]
        name_list = name.split()
        word_count = len(name_list)
        name_listed = list()
        num_lines = 2
        if word_count == 4:
            name_listed.append(sp.join([str(name_list[0]), str(name_list[1])]))
            name_listed.append(sp.join([str(name_list[2]), str(name_list[3])]))
        elif word_count == 3:
            name_listed.append(sp.join([str(name_list[0]), str(name_list[1])]))
            name_listed.append(name_list[2])
        else:
            name_listed = [sp.join(name_list)]
            num_lines = 1
        return [num_lines, name_listed]

    def legend_name(c_num):
        lista = format_name(c_num)
        name_ls = lista[1]
        if len(name_ls) > 1:
            name_str = " ".join(name_ls)
        else:
            name_str = str(name_ls[0])
        return name_str

    def data_elmA(c_num, p_list):
        df_pg = elmA_process(c_2.loc[p_list, elmA_head])
        df_av = elmA_process(c_2.loc[:, elmA_head])
        return [c_2.loc[c_num, "Alignment Score"], df_pg, df_av]

    def elmA_process(df):
        df.loc['Total'] = df.sum()
        return math.floor(int(df.at["Total", "Alignment Score"]) / df.shape[0])

    def data_elmB(c_num, p_list):
        df_pg = elmB_process(c_1.loc[p_list,
                                     elmB_head].replace(refeLMHD).astype(int))
        df_av = elmB_process(c_1.loc[:,
                                     elmB_head].replace(refeLMHD).astype(int))
        return [
            ['P1', 'P2', 'P3', 'P4', 'P5', 'P6', 'P7', 'P8'],
            (
                c_name(c_num),
                [
                    c_1.loc[c_num, elmB_head].replace(refeLMHD).to_list(),
                    df_pg,
                    df_av,
                    # Ignore list below
                    [0, 4, 0, 4, 0, 4, 0, 4]
                ])
        ]

    def elmB_process(df):
        df = df.astype(float).replace(0, np.NaN)
        ls = df.mean(numeric_only=True)
        return ls.round(decimals=0).astype(int).to_list()

    def data_elmCA(c_num=None, p_list=None):
        if c_num == 0 or c_num:
            return c_3.loc[c_num, elmCA_head].replace(refeTF).to_list()
        elif p_list == 0 or p_list:
            return elmCA_process(c_3.loc[p_list, elmCA_head].replace(refeYN))
        else:
            return elmCA_process(c_3.loc[:, elmCA_head].replace(refeYN))

    def elmCA_process(df):
        df.loc["Sum"] = df.sum() / df.shape[0]
        return [int(round(i)) for i in list(df.loc["Sum"])]

    def data_elmD(c_num, p_list):
        ls_cl = c_3.loc[c_num, elmD_head].replace(refeXB_bool).to_list()
        ls_pg = elmD_process(c_3.loc[p_list, elmD_head].replace(refeXB))
        ls_av = elmD_process(c_3.loc[:, elmD_head].replace(refeXB))
        i = 0
        result = []
        while i < len(ls_cl):
            result.append([ls_cl[i], ls_pg[i], ls_av[i]])
            i += 1
        return result

    def elmD_process(df):
        df.loc["Sum"] = df.sum() / df.shape[0]
        return [int(math.floor(i)) for i in (df.loc["Sum"]).to_list()]

    def data_elmDA(c_num, p_list):
        df_pg = elmDA_process(c_3.loc[p_list, elmDA_head].replace(refeYN))
        df_av = elmDA_process(c_3.loc[:, elmDA_head].replace(refeYN))
        return [c_3.loc[c_num, elmDA_head].replace(refeTF)[1], df_pg, df_av]

    def elmDA_process(df):
        d_row = df["4Fv.a.ii"].sum()
        if d_row == 0: return 0
        else: return math.floor(d_row / df.shape[0])

    def data_elmE(c_num, p_list):
        df_pg = elmE_process(c_3.loc[p_list, elmE_head].replace(refeYN))
        df_av = elmE_process(c_3.loc[:, elmE_head].replace(refeYN))
        return [c_3.loc[c_num, elmE_head].replace(refeTF)[1], df_pg, df_av]

    def elmE_process(df):
        d_row = df["4E"].sum()
        if d_row == 0: return 0
        else: return math.floor(d_row / df.shape[0])

    def data_elmF(c_num, p_list):
        ls_cls = c_3.loc[c_num, elmF_head].replace(refeTF)
        ls_cls[ls_cls.values != False] = True
        ls_cl = ls_cls.to_list()
        ls_pg = elmF_process(c_3.loc[p_list, elmF_head])
        ls_av = elmF_process(c_3.loc[:, elmF_head])
        i = 0
        result = []
        while i < len(ls_cl):
            result.append([ls_cl[i], ls_pg[i], ls_av[i]])
            i += 1
        return result

    def elmF_process(df):
        df.loc[(df.Other != "No"), 'Other'] = 100
        dt = df.replace(refeYN)
        dt.loc["Sum"] = dt.sum() / dt.shape[0]
        return [int(math.floor(i)) for i in list(dt.loc["Sum"])]

    return {
        "pName": pg_name(p_num),
        "pList": p_list,
        "pDict": pg_dict(),
        "pCat": pg_cat(),
        "pcList": peerGrp_list(),
        "cName": c_name(c_num),
        "cList": client_list(),
        "formatName": format_name(c_num),
        "formatpName": format_p_name(p_num),
        "legendName": legend_name(c_num),
        "elmA": data_elmA(c_num, p_list),
        "elmB": data_elmB(c_num, p_list),
        "elmCA":
        [data_elmCA(c_num=c_num),
         data_elmCA(p_list=p_list),
         data_elmCA()],
        "elmD": data_elmD(c_num, p_list),
        "elmDA": data_elmDA(c_num, p_list),
        "elmE": data_elmE(c_num, p_list),
        "elmF": data_elmF(c_num, p_list)
    }


def pdf_production(stat, elem, c_num):
    title = 'Practice Verification Client Benchmark Report'
    pdf = PDF()
    pdf.set_title(title)
    pdf.head(c_num, elem["formatName"], stat["elemHeadtxt"])
    pdf.element_a(elem["formatName"], elem["pName"], elem["elmA"])
    pdf.element_b(elem["legendName"], elem["pName"], plot_map(elem["elmB"]))
    pdf.element_c('PRINCIPLE 4: EX-ANTE ASSESSMENT OF IMPACT',
                  stat["elemCtxt"], stat["elemCbullettxt"])
    pdf.element_c_a(
        'APPROACH TO ASSESSING EXPECTED IMPACT', elem["formatName"],
        elem["elmCA"][0], stat["elemCAtxt"], stat["elemCBtxt"],
        plot_barGraph(elem["pName"], elem["elmCA"][1], elem["elmCA"][2]))
    pdf.element_d('DIMENSIONS OF IMPACT INVESTMENT', elem["formatName"],
                  elem["formatpName"], stat["elemDtxt"], elem["elmD"])
    pdf.element_d_a('Does the Manager use all five IMP dimensions?',
                    elem["formatName"], elem["formatpName"], stat["elemDAtxt"],
                    elem["elmDA"])
    pdf.element_e('USE OF IMPACT INDICATORS', elem["formatName"],
                  elem["formatpName"], stat["elemEtxt"], elem["elmE"])
    pdf.element_f(elem["formatName"], elem["formatpName"], stat["elemFtxt"],
                  elem["elmF"])
    pdf.set_author('BlueMark')
    pdf.output(stat["output"])
    return stat["output"]