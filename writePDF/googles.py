import gspread
from oauth2client.service_account import ServiceAccountCredentials
from django.conf import settings
import pandas as pd

DICTA = settings.SECRET_DICTA

scope = [
    'https://spreadsheets.google.com/feeds',
    'https://www.googleapis.com/auth/drive'
]

cred = ServiceAccountCredentials.from_json_keyfile_dict(DICTA, scope)
client = gspread.authorize(cred)


def gData(sheetName, tabNo):
    sp = client.open(sheetName)
    if tabNo == 1:
        sp1 = sp.worksheet('verifAll').get('A2:T34')
        df = pd.DataFrame(sp1)
    elif tabNo == 2:
        sp2 = sp.worksheet('verifP4').get('A2:AP33')
        df = pd.DataFrame(sp2)
    else:
        df = pd.DataFrame()
    return df
