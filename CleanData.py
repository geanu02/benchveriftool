import pandas as pd
#from ImportData import df_sheet1, df_sheet2

df_sheet1 = pd.read_csv('data/verifAll.csv')
df_sheet2 = pd.read_csv('data/verifP4.csv')


def s1_df1(dt=df_sheet1):
    df_all_1 = dt.iloc[2:34, :10].drop([3, 4]).reset_index(drop=True)
    df_all_1.columns = df_all_1.iloc[0]
    data_s1_df1 = df_all_1.drop(df_all_1.index[0]).reset_index(drop=True)
    return data_s1_df1


# All Verifications


def s1_df2(dt=df_sheet1):
    df_all_2 = df_sheet1.iloc[2:34, 11:].drop([3, 4]).reset_index(drop=True)
    df_all_2.columns = df_all_2.iloc[0]
    data_s1_df2 = df_all_2.drop(df_all_2.index[0]).reset_index(drop=True)
    data_s1_df2['Alignment Score'] = data_s1_df2['Alignment Score'].astype(int)
    return data_s1_df2


# Statistics Across First 31 Verifications


def s1_df3(dt=df_sheet1):
    df_stat_1 = dt.iloc[42:47, 1:10].reset_index(drop=True)
    df_stat_1.columns = df_stat_1.iloc[0]
    data_s1_df3 = df_stat_1.drop(df_stat_1.index[0]).reset_index(drop=True)
    return data_s1_df3


def s1_df4(dt=df_sheet1):
    df_stat_2 = dt.iloc[48:53, 1:10].reset_index(drop=True)
    df_stat_2.columns = df_stat_2.iloc[0]
    data_s1_df4 = df_stat_2.drop(df_stat_2.index[0]).reset_index(drop=True)
    return data_s1_df4


def s1_df5(dt=df_sheet1):
    df_stat_3 = dt.iloc[55:61, 1:10].reset_index(drop=True)
    df_stat_3.columns = df_stat_3.iloc[0]
    data_s1_df5 = df_stat_3.drop(df_stat_3.index[0]).drop(
        [3]).reset_index(drop=True)
    return data_s1_df5


# Analysis (P4) - Sheet#2

# All Selected


def s2_df1(dt=df_sheet2):
    df_p4_all = dt.iloc[2:33, 1:42].drop([3]).reset_index(drop=True)
    df_p4_all.columns = df_p4_all.iloc[0]
    data_s2_df1 = df_p4_all.drop(df_p4_all.index[0]).reset_index(drop=True)
    return data_s2_df1


# Principle 4 Statistics Across First 30 Verifications


def s2_df2(dt=df_sheet2):
    df_p4_3 = df_sheet2.iloc[43:76, 1:4].drop([59]).reset_index(drop=True)
    df_p4_3.columns = df_p4_3.iloc[0]
    data_s2_df2 = df_p4_3.drop(df_p4_3.index[0]).reset_index(drop=True)
    return data_s2_df2
