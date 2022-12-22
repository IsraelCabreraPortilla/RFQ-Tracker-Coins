import webScrappingYahoo as webScrapping
import pandas as pd
import requests
from GoogleSpreadsheets import update_row
from rfq import get_rfq_price
import numpy
import time
import dataframe_image as dfi
from datetime import datetime


def envio_msjIMG(symbol, time1, time2):
        r = requests.post(f'https://api.telegram.org/bot5363622455:AAEoFyCSHrhOZhQzxSGD6MxOWKw9h9aoQqY/sendPhoto',
                        files = {'photo':(r'table.png', open(r'table.png', 'rb'))},
                        data={'chat_id': '-614042061', 'parse_mode':'markdown','caption': '*{}* Analysis from {} to {} '.format(symbol,time1,time2)})
def envio_msj_still_here():
    r = requests.post('https://api.telegram.org/bot5363622455:AAEoFyCSHrhOZhQzxSGD6MxOWKw9h9aoQqY/sendMessage',
                data= {'chat_id': "-614042061",'text': "Still pulling up data..."})
def envio_msj_spreads_send():
 r = requests.post('https://api.telegram.org/bot5363622455:AAEoFyCSHrhOZhQzxSGD6MxOWKw9h9aoQqY/sendMessage',
                data= {'chat_id': "-614042061",'text': "Data successfully send to --> Spreads Exchange and RFQ..."})
 return r.json()
 
time1_ = str(datetime.now().strftime("%H:%M:%S"))
#Prices extracted from WebScrapping
global current_prices, usd_worth
c = webScrapping.calcula_usd()
current_prices = c[0]
usd_worth = c[1]
dictionary_spreads = {'BTC':[],'ETH':[],'USDT':[],'BCH':[],'LTC':[], 'AAVE': [], 'BAND': [], 'BAT': [], 'COMP': [], 'DAI': [], 'ENJ': [], 'FTM': [], 'GRT': [], 'LINK': [], 'LTC': [], 'MANA': [], 'MATIC': [], 'OGN': [],'SNX': [], 'SUSHI': [], 'UNI': [], 'YFI': []}
dictionary_spreads_mean = {'BTC':0,'ETH':0,'USDT':0,'BCH':0,'LTC':0, 'AAVE': 0, 'BAND': 0, 'BAT': 0, 'COMP': 0, 'DAI': 0, 'ENJ': 0, 'FTM': 0, 'GRT': 0, 'LINK': 0, 'LTC': 0, 'MANA': 0, 'MATIC': 0, 'OGN': 0,'SNX': 0, 'SUSHI': 0, 'UNI': 0, 'YFI': 0}
datos_generales = []
df_resumen_general = ""
def run():
    i = 0
    while i < 10:
        if i == 50 or i==50 or i==100 or i ==150:
            envio_msj_still_here()
        for k in current_prices:
            cant = get_rfq_price(k,current_prices[k])
            print(i, k, cant)
            if cant[0] != 0 and cant[1] !=0:
            #spreads_LINKUSD["Spreads"] = ((spreads_LINKUSD['Ask'] - spreads_LINKUSD['Bid'])/spreads_LINKUSD['Ask'])*10000
                spread = ((cant[1]-cant[0])/cant[1])*10000
                dictionary_spreads[k].append(spread)
        i = i + 1
        
    for k in dictionary_spreads:
         if len(dictionary_spreads[k]) > 0:
            dictionary_spreads_mean[k] = numpy.mean(dictionary_spreads[k])
       
    
    for k in dictionary_spreads_mean:
        time.sleep(5)
        if dictionary_spreads_mean[k] !=0:
            mean = dictionary_spreads_mean[k]
            size = str(current_prices[k])
            usd = str(usd_worth[k])
            r = update_row(k,size,usd,mean,"RFQ")
            print(k, r)
            mean_ = float(mean)
            size_ =  float(size)
            usd_ = int(usd)
            mean = f'{mean_:,.2f}'
            size = f'{size_:,.2f}'
            usd = f'{usd_:,}'
            datos_generales.append([k, size, usd, mean, "RFQ"])
            
    time2_ = str(datetime.now().strftime("%H:%M:%S"))
    
    df_resumen_general = pd.DataFrame(datos_generales, columns=('Coin', 'Size', 'USD_Worth','Spread','Via'))
    print(df_resumen_general)
    dfi.export(
            df_resumen_general,
            "table.png",
            table_conversion="matplotlib"
        )
    envio_msjIMG('Spreads RFQ', time1_, time2_)
    envio_msj_spreads_send()

    
