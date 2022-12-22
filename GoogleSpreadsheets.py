from oauth2client.service_account import ServiceAccountCredentials
import gspread
from gspread.exceptions import APIError
from datetime import date
import time

credsPath = 'creds_blotter.json'
scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',
         "https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name(credsPath, scope)
client = gspread.authorize(creds)
sheet = client.open('Spreads RFQ and EXCH - Records').get_worksheet(0)

# Decorator function for failed requests 
def retry(func, retries=7):
  def retry_wrapper(*args, **kwargs):
    attempts = 0
    while attempts < retries:
      try:
        return func(*args, **kwargs)
      except APIError as e:
        print('Esperando a que se libere la cuota: ',e)
        time.sleep(10*(attempts+1))
        attempts += 1
  return retry_wrapper

@retry
def update_row(coin, size, usd_worth, spread, via):
    columna = sheet.get('A:A')
    ren = len(columna) + 1
    sheet.update_acell('A'+str(ren), coin)
    sheet.update_acell('B'+str(ren), size)
    sheet.update_acell('C'+str(ren), usd_worth)
    sheet.update_acell('D'+str(ren), spread)
    sheet.update_acell('E'+str(ren), via)
    sheet.update_acell('F'+str(ren), str(date.today()))
    return True

    

    