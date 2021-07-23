import pandas as pd
import numpy as np
from .googles import gData

verifP4ColDrop = [
    "4A_Comment", "4B_Comment", "4C_Comment", "4D_Comment", "4E_Comment",
    "4F_Comment", "4G_Comment", "Nada"
]

verifP4ColNames = [
    'Client', 'Principle4', 'InvestorType', '4A', '4A_Comment', '4B',
    "4B_Comment", '4C', "4C_Comment", '4D', "4D_Comment", '4E', "4E_Comment",
    '4F_i', '4F_ii', '4F_iii', '4F_iv', '4F_v', '4F_total', "4F_Comment",
    '4G_i', '4G_ii', '4G_iii', '4G_iv', '4G_v', '4G_total', "4G_Comment",
    "Nada", '4C.a.i', '4C.a.ii', '4C.a.iii', '4C.a.iv', '4C.a.v', '4C.a.vi',
    'HIPSO', 'IRIS', 'GIIRS', 'GRI', 'Other', '4Fv.a.i', '4Fv.a.ii'
]


def clean_s1_df1(dt):
    df_all_1 = dt.iloc[1:32, :9].drop([2]).reset_index(drop=True)
    df_all_1.columns = df_all_1.iloc[0]
    data_s1_df1 = df_all_1.drop(df_all_1.index[0]).reset_index(drop=True)
    dataa = data_s1_df1.replace(np.NaN, "N/A")
    return dataa


def clean_s1_df2(dt):
    df_all_2 = dt.iloc[0:32, 10:20].drop([1, 2]).reset_index(drop=True)
    df_all_2.columns = df_all_2.iloc[0]
    data_s1_df2 = df_all_2.drop(df_all_2.index[0]).reset_index(drop=True)
    data_s1_df2 = data_s1_df2.replace(np.NaN, 0)
    data_s1_df2 = data_s1_df2.replace("N/A", 0)
    data_s1_df2['Alignment Score'] = data_s1_df2['Alignment Score'].astype(int)
    return data_s1_df2


def clean_s2_df1(dt):
    df_p4_all = dt.iloc[0:31, 1:42].drop([1]).reset_index(drop=True)
    df_p4_all.columns = verifP4ColNames
    data_s2_df1 = df_p4_all.drop(df_p4_all.index[0]).reset_index(drop=True)
    data_s2_df1 = data_s2_df1.drop(verifP4ColDrop, axis=1)
    return data_s2_df1
