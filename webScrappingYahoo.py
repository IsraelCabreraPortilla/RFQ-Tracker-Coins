import time
import pandas as pd
import requests
from bs4 import BeautifulSoup
import datetime
import time
from datetime import date
import csv

def extract_close_value(date, coin):
  received_Date = str(date)
  date = received_Date.split(sep='-')
  date_time = datetime.datetime(int(date[0]), int(date[1]), int(date[2]), 00, 00, 00)
  unix_time = time.mktime(date_time.timetuple())
  day_unix = str(unix_time)[0:10]
  coin = coin
  headers={'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'}
  URL = "https://finance.yahoo.com/quote/{}-USD/history?period1={}&period2={}&interval=1d&filter=history&frequency=1d&includeAdjustedClose=true".format(coin, day_unix,day_unix)
  page = requests.get(URL, headers=headers)
  soup = BeautifulSoup(page.content, "html.parser")
  job_elements = list(soup.find_all("td",class_="Py(10px) Pstart(10px)"))
  for i in range(len(job_elements)):
    job_elements[i] = str(job_elements[i])
    job_elements[i] = job_elements[i].replace('<td class="Py(10px) Pstart(10px)"><span>','')
    job_elements[i] = job_elements[i].replace('</span></td>','')
  value_close = float(job_elements[-2].replace(',',''))
  return value_close


#---- Leyendo datos del csv ------ 
def calcula_usd():
  filename = open('coins.csv', 'r')
  file = csv.DictReader(filename)
  coins = []
  values = []
  for col in file:
      if col['Coins'] =='COMP':
          values.append(34)
          coins.append(col["Coins"])
      elif col['Coins'] =='GRT':
          coins.append(col["Coins"])
          values.append(0.05701)
      elif col['Coins'] =='UNI':
          coins.append(col["Coins"])
          values.append(5.35)
      else:
          coins.append(col["Coins"])
          values.append( float(extract_close_value(date.today(), col["Coins"] )))
          #print(col['Coins'], extract_close_value(date.today(), col["Coins"]))
  dict_from_list = dict(zip(coins, values))
  usd_worth = []
  for k in dict_from_list:
    if k == "BTC" or k=="USDT" or k=="ETH" :
      dict_from_list[k] = 100000/dict_from_list[k]
      usd_worth.append(100000)
    elif k =="DAI"  or k=="BAT":
      dict_from_list[k] = 2000/dict_from_list[k]
      usd_worth.append(2000)
    elif k =="BCH" or k=="YFI" or k=="GRT":
      dict_from_list[k] = 5000/dict_from_list[k]
      usd_worth.append(5000)
    else:
      dict_from_list[k] = 10000/dict_from_list[k]
      usd_worth.append(10000)
    
    dict_from_list2 = dict(zip(coins, usd_worth))
    
  return dict_from_list, dict_from_list2

#c = calcula_usd()
#print(c)
#print(len(c[0]))
