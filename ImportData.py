import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd

dataSource = "local"

scope = [
    'https://spreadsheets.google.com/feeds',
    'https://www.googleapis.com/auth/drive'
]
creds = ServiceAccountCredentials.from_json_keyfile_name(
    # 'client_secret.json',
    'client_secret_856697970476-3lhgkaen7h5e1i9873reeenvphjfau69.apps.googleusercontent.com',
    scope)
client = gspread.authorize(creds)

# 'verif' is the workbook filename
sheets = client.open('verif')
sheet_1 = sheets.worksheet("Analysis (all)")
sheet_2 = sheets.worksheet("Analysis (P4)")

if dataSource == "cloud":
    df_sheet1 = pd.DataFrame(sheet_1.get_all_values())
    df_sheet2 = pd.DataFrame(sheet_2.get_all_values())
elif dataSource == "local":
    df_sheet1 = pd.DataFrame()
    df_sheet2 = pd.DataFrame()
else:
    df_sheet1 = pd.DataFrame()
    df_sheet2 = pd.DataFrame()
