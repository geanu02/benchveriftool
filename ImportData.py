import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd

scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name(
    'client_secret.json', scope)
client = gspread.authorize(creds)

# 'verif' is the workbook filename
sheets = client.open('verif')
sheet_1 = sheets.worksheet("Analysis (all)")
sheet_2 = sheets.worksheet("Analysis (P4)")

df_sheet1 = pd.DataFrame(sheet_1.get_all_values())
df_sheet2 = pd.DataFrame(sheet_2.get_all_values())
