import pandas as pd
import numpy as np
import math

from CleanData import s2_df1
from TransformData import peerGrp_bgData
from chrisproject import peerGrp_indices

df_p4_all = pd.DataFrame(s2_df1())
bgHeaders = ["Client", "4C.a.i", "4C.a.ii", "4C.a.v", "4C.a.vi"]
bgCols = [0, 28, 29, 32, 33]
refeYN = {'Yes': 100, 'No': 0}
pg_indices = peerGrp_indices(0)


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


p_list = [0, 4, 17, 27]

caption = "Definition: Assess the expected impact of each investment based on a systematic approach."
caption_split = caption.split()
caption_1 = caption_split.pop(0)

print(caption_1)
print(' '.join(caption_split))