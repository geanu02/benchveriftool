from PlotMap import plot_map
import pandas as pd
import numpy as np
import re
import math
from CleanData import s1_df1, s1_df2, s1_df3, s1_df4, s1_df5, s2_df1, s2_df2

dfi_list = [3, 7, 8, 9, 10, 11, 14]

ques_tb1 = [
    'What is the intended impact?', 'Who experiences the intended impact?',
    'How significant is the intended impact?',
    ['What is the likelihood of achieving', 'expected impact?'],
    [
        'What are significant risk factors that could',
        'result in variance from expected impact?'
    ]
]

col_tb2 = ['HIPSO', 'IRIS', 'GIIRS', 'GRI', 'Other']

bgHeaders = ["Client", "4C.a.i", "4C.a.ii", "4C.a.v", "4C.a.vi"]
bgCols = [0, 28, 29, 32, 33]
refeYN = {'Yes': 100, 'No': 0}
refeTF = {'Yes': True, 'No': False}

df_all_1 = pd.DataFrame(s1_df1())
df_p4_all = pd.DataFrame(s2_df1())
df_all_2 = pd.DataFrame(s1_df2())


def col1_values(element_letter):
    if element_letter == 'd':
        return ques_tb1
    elif element_letter == 'f':
        return col_tb2
    else:
        return ['empty', 'empty', 'empty', 'empty', 'empty']


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
            name_listed.append(sp.join([str(name_list[0]), str(name_list[1])]))
            name_listed.append(sp.join([str(name_list[2]), str(name_list[3])]))
        elif c_num in grp2:
            name_listed.append(sp.join([str(name_list[0]), str(name_list[1])]))
            name_listed.append(name_list[2])
        elif c_num in grp3:
            name_listed.append(name_list[0])
            name_listed.append("({0} {1})".format(name_list[1], name_list[2]))
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
    name = peerGrp_category()[pg_index]
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


def legend_p_name(pg_index):
    lista = format_p_name(pg_index)
    name_ls = lista[1]
    if lista[0] > 1:
        name_str = " ".join(name_ls)
    else:
        name_str = str(name_ls[0])
    return name_str


def list_all_names():
    c_list = df_all_1.iloc[:, 1].tolist()
    return c_list


def return_cnum(clname):
    df = df_all_1.iloc[:, [0, 1]]
    val = df[df["Client"] == clname].index.item()
    return val


def clean_data(d):
    refe = {'LOW': 1, 'MODERATE': 2, 'HIGH': 3, 'ADVANCED': 4, 'N/A': 0}
    replaced = d.replace(refe)
    dt_swap = replaced.swapaxes(0, 1, True)
    dt_crop = dt_swap[1:]
    dicta = dict(dt_crop)
    return dicta


def principle_list():
    return ['P1', 'P2', 'P3', 'P4', 'P5', 'P6', 'P7', 'P8']


def c_name(c_num):
    df = clean_data(df_all_1)[c_num]
    namesung = str(df[0])
    if c_num == 19 or c_num == 20:
        nameList = namesung.split()
        nameList.remove('-')
        namesung = " ".join(nameList)
    return namesung


def c_num_lines(c_num):
    a_txt = format_name(c_num)
    r_value = int(a_txt[0])
    return r_value


def c_name_list(c_num):
    a_txt = format_name(c_num)
    r_value = a_txt[1]
    return r_value


def c_name_year(c_num):
    a_txt = format_name(c_num)
    r_value = int(a_txt[2])
    return r_value


def data_list(c_num):
    df = clean_data(s1_df1())[c_num]
    return list(df[1:])


def peerGrp_category():
    p_l = df_p4_all.iloc[:, 2]
    p_l2 = p_l.value_counts().index
    return p_l2


def peerGrp_dict():
    piv = df_p4_all.iloc[:, [0, 2]]
    col1 = piv.iloc[:, 1]
    cols = col1.value_counts().reset_index()
    col = cols["index"]
    piv = piv.reset_index()
    piv2 = piv.pivot(columns="Investor Type", values="index")
    piv2 = piv2[col]
    dicta = dict()
    keysa = range(len(piv2.columns))
    for each in keysa:
        serie = piv2.iloc[:, each].squeeze().dropna().astype(int)
        dicta[each] = {serie.name: serie.to_list()}
    return dicta


# PlotMap Data


def pg_list(p_list):
    df = df_all_2.iloc[p_list, 1:9].replace('N/A', 0).astype(int)
    df = df.astype(float).replace(0, np.NaN)
    cols = df.columns
    ls = df.mean(numeric_only=True)
    return_ls = ls.round(decimals=0).to_list()
    return return_ls


def av_list():
    df = df_all_2.iloc[:, 1:9].replace('N/A', 0).astype(int)
    df = df.astype(float).replace(0, np.NaN)
    cols = df.columns
    ls = df.mean(numeric_only=True)
    return_ls = ls.round(decimals=0).to_list()
    return return_ls


def heatmap(c_num, p_list):
    data = [
        principle_list(),
        (
            c_name(c_num),
            [
                data_list(c_num),
                pg_list(p_list),
                av_list(),
                # Ignore list below
                [0, 4, 0, 4, 0, 4, 0, 4]
            ])
    ]
    return data


def data_elmA(c_num, p_num):
    val_eacc = elmA_scoreCC(c_num)
    val_eapg = elmA_scorePG(p_num)
    val_eaav = elmA_scoreAV()
    dt_elmA = list()
    dt_elmA.append(val_eacc)
    dt_elmA.append(val_eapg)
    dt_elmA.append(val_eaav)
    return dt_elmA


def elmA_scoreCC(c_num):
    val_score = df_all_2.iloc[c_num, 9]
    return val_score


def elmA_scorePG(p_num):
    dt_raw = df_all_2.iloc[p_num, [0, 9]]
    dt_raw['Alignment Score'] = pd.to_numeric(dt_raw['Alignment Score'])
    dt = dt_raw.swapaxes(0, 1, True)
    new_header = dt.iloc[0]
    dt = dt[1:]
    dt.columns = new_header
    no_cols = len(dt.columns)
    dt["sum"] = dt.sum(axis=1)
    val_peerGrp = math.floor(int(dt["sum"]) / no_cols)
    return val_peerGrp


def elmA_scoreAV():
    dt_raw = df_all_2.iloc[:, [0, 9]]
    dt = dt_raw.swapaxes(0, 1, True)
    new_header = dt.iloc[0]
    dt = dt[1:]
    dt.columns = new_header
    no_cols = len(dt.columns)
    dt["sum"] = dt.sum(axis=1)
    val_allVerif = math.floor(int(dt["sum"]) / no_cols)
    return val_allVerif


def data_elmD(c_num, p_num):
    lst_edcc = elmD_custCheck(c_num)
    lst_edpg = elmD_peerGrp(p_num)
    lst_edav = elmD_allVerif()
    i = 0
    dt_elmD = list()
    while i < len(lst_edcc):
        new_row = [lst_edcc[i], lst_edpg[i], lst_edav[i]]
        dt_elmD.append(new_row)
        i += 1
    return dt_elmD


def elmD_custCheck(c_num):
    refe = {'x': True, '(blank)': False}
    dataseries = df_p4_all.iloc[c_num, 13:18]
    ds = dataseries.replace(refe)
    ls_edcc = list(ds)
    return ls_edcc


def elmD_peerGrp(p_num):
    refe = {'x': 100, '(blank)': 0}
    dataset = df_p4_all.iloc[p_num, 13:18]
    dt_raw = dataset.replace(refe)
    dt = dt_raw.swapaxes(0, 1, True)
    no_cols = len(dt.columns)
    dt["sum"] = dt.sum(axis=1)
    dt["pour_cent"] = dt["sum"] / no_cols
    a = list(dt["pour_cent"])
    ls_edpg = [int(math.floor(i)) for i in a]
    return ls_edpg


def elmD_allVerif():
    refe = {'x': 100, '(blank)': 0}
    dataset = df_p4_all.iloc[:, 13:18]
    dt_raw = dataset.replace(refe)
    dt = dt_raw.swapaxes(0, 1, True)
    no_cols = len(dt.columns)
    dt["sum"] = dt.sum(axis=1)
    dt["pour_cent"] = dt["sum"] / no_cols
    a = list(dt["pour_cent"])
    ls_edav = [int(math.floor(i)) for i in a]
    return ls_edav


def data_elmDA(c_num, p_list):
    val1 = elmDA_cust(c_num)
    val2 = elmDA_peerGrp(p_list)
    val3 = elmDA_allVerif()
    result = list()
    result.append(val1)
    result.append(val2)
    result.append(val3)
    return result


def elmDA_cust(client_index):
    dt = df_p4_all.iloc[client_index, [0, -1]]
    dt = dt.replace({'Yes': True, 'No': False})
    val = dt[1]
    if val == True:
        return True
    elif val == False:
        return False
    else:
        return False


def elmDA_peerGrp(p_list):
    df = df_p4_all.iloc[:, [0, -1]]
    df.iloc[16, 1] = 'No'  # LeapFrog 2019 is empty: assign "NO"
    dt = df.iloc[p_list, :]
    dt.columns = ['Client', '4FVII']
    dt = dt.replace({'Yes': 100, 'No': 0})
    no_cols = len(dt.index)
    d_row = dt['4FVII'].sum()
    if d_row == 0:
        result = 0
    else:
        result = math.floor(d_row / no_cols)
    return result


def elmDA_allVerif():
    dt = df_p4_all.iloc[:, [0, -1]]
    dt.iloc[16, 1] = 'No'  # LeapFrog 2019 has no value
    dt.columns = ['Client', '4FVII']
    dt = dt.replace({'Yes': 100, 'No': 0})
    no_cols = len(dt.index)
    d_row = dt['4FVII'].sum()
    if d_row == 0:
        result = 0
    else:
        result = math.floor(d_row / no_cols)
    return result


def data_elmE(c_num, p_list):
    val_eecc = elmE_cust(c_num)
    val_eepg = elmE_peerGrp(p_list)
    val_eeav = elmE_allVerif()
    val_elmE = list()
    val_elmE.append(val_eecc)
    val_elmE.append(val_eepg)
    val_elmE.append(val_eeav)
    return val_elmE


def elmE_cust(c_num):
    dt = df_p4_all.iloc[c_num, [0, 11]]
    dt = dt.replace({'Yes': True, 'No': False})
    val_eec = dt[1]
    return val_eec


def elmE_peerGrp(p_list):
    dt = df_p4_all.iloc[p_list, [0, 11]]
    dt = dt.replace({'Yes': 100, 'No': 0})
    no_cols = len(dt.index)
    d_row = dt["4E"].sum()
    if d_row == 0:
        result = 0
    else:
        result = math.floor(d_row / no_cols)
    return result


def elmE_allVerif():
    dt = df_p4_all.iloc[:, [0, 11]]
    dt = dt.replace({'Yes': 100, 'No': 0})
    no_cols = len(dt.index)
    d_row = dt["4E"].sum()
    if d_row == 0:
        result = 0
    else:
        result = math.floor(d_row / no_cols)
    return result


def data_elmF(c_num, p_num):
    lst_efcc = elmF_custCheck(c_num)
    lst_efpg = elmF_peerGrp(p_num)
    lst_efav = elmF_allVerif()
    i = 0
    dt_elmF = list()
    while i < len(lst_efcc):
        new_row = [lst_efcc[i], lst_efpg[i], lst_efav[i]]
        dt_elmF.append(new_row)
        i += 1
    return dt_elmF


def elmF_custCheck(c_num):
    refe = {'Yes': True, 'No': False}
    dataseries = df_p4_all.iloc[c_num, -7:-2]
    ds = dataseries.replace(refe)
    ds[ds.values != False] = True
    ls_efcc = list(ds)
    return ls_efcc


def elmF_peerGrp(p_num):
    refe = {'Yes': 100, 'No': 0}
    dataset = df_p4_all.iloc[p_num, -7:-2]
    dt_raw = dataset.replace(refe)
    dt_raw.columns = ['HIPSO', 'IRIS', 'GIIRS', 'GRI', 'Other']
    dt_raw[dt_raw['Other'].values != 0] = 100
    dt = dt_raw.swapaxes(0, 1, True)
    no_cols = len(dt.columns)
    dt["sum"] = dt.sum(axis=1)
    dt["pour_cent"] = dt["sum"] / no_cols
    a = list(dt["pour_cent"])
    ls_efpg = [int(math.floor(i)) for i in a]
    return ls_efpg


def elmF_allVerif():
    refe = {'Yes': 100, 'No': 0}
    dataset = df_p4_all.iloc[:, -7:-2]
    dt_raw = dataset.replace(refe)
    dt_raw.columns = ['HIPSO', 'IRIS', 'GIIRS', 'GRI', 'Other']
    dt_raw[dt_raw['Other'].values != 0] = 100
    dt = dt_raw.swapaxes(0, 1, True)
    no_cols = len(dt.columns)
    dt["sum"] = dt.sum(axis=1)
    dt["pour_cent"] = dt["sum"] / no_cols
    a = list(dt["pour_cent"])
    ls_efav = [int(math.floor(i)) for i in a]
    return ls_efav


def elmCA_indicatorData(c_num):
    dataset = df_p4_all.iloc[c_num, bgCols]
    dataset = dataset.replace(refeTF)
    return_ls = dataset.to_list()[1:]
    return return_ls


def peerGrp_bgData(pg_indices):
    dataset = df_p4_all.iloc[pg_indices, bgCols]
    dataset.columns = bgHeaders
    dataset = dataset.replace(refeYN)
    no_cols = len(dataset.index)
    dataset = dataset.append(dataset.sum(numeric_only=True), ignore_index=True)
    dt = dataset.iloc[no_cols, 1:5] / no_cols
    return dt


def allVerif_bgData():
    dataset = df_p4_all.iloc[:, bgCols]
    dataset.columns = bgHeaders
    dataset = dataset.replace(refeYN)
    no_cols = len(dataset.index)
    dataset = dataset.append(dataset.sum(numeric_only=True), ignore_index=True)
    dt = dataset.iloc[no_cols, 1:5] / no_cols
    return dt
