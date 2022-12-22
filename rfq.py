import pandas as pd
import json
import dataframe_image as dfi
import requests
import base64
import time
import hashlib
import hmac
base = 'https://trade-am.osl.com/'
key = '55ea46ea-c7a0-4cb3-9f47-4644f3ae12ee'
secret = b'FM8i+kK6RIj3dsM5atLiZAVTkQyJjuLEUnmOiczt1LBZ7WIynJDxpkqvsXan1WF30/BJz5aKHW8NFXNXMgtEAg=='
secret = base64.b64decode(secret)
path = 'api/3/retail/quote'

def get_rfq_price(coin, qty):
    qty = round(qty,2)
    
    def gen_tonce():
        return str(int(time.time() * 1000 * 1000))

    #-----------------------------> Buy Price
    params = {
            "quoteRequest": {
                "buyTradedCurrency": False,
                "tradedCurrency": str(coin),
                "settlementCurrency": "USD",
                "tradedCurrencyAmount": float(qty),
                "isIndicativeQuote": False
                            }           
                }
    params = dict(params)
    params['tonce'] = gen_tonce()
    data = json.dumps(params)
    hmac_obj = hmac.new(secret, (path + chr(0) + data).encode(), hashlib.sha512)
    hmac_sign = base64.b64encode(hmac_obj.digest())

    headers = {
        'Content-Type': 'application/json',
        'Rest-Key': key,
        'Rest-Sign': hmac_sign,
        'User-Agent': 'Americas Test Client'
    }
    response = requests.post(base + path, headers=headers, data=data)
    result_buy = response.json()
    buyPrice = 0
    if result_buy['resultCode'] == 'OK':
        buyPrice = float(result_buy['quoteResponse']['retailRateInSettlementCurrency'])
    
    #-----------------------------> Sell Price
    params = {
            "quoteRequest": {
            "buyTradedCurrency": True,
            "tradedCurrency": str(coin),
            "settlementCurrency": "USD",
            "tradedCurrencyAmount": float(qty),
            "isIndicativeQuote": False
            } 
        }        
                    
    params = dict(params)
    params['tonce'] = gen_tonce()
    data = json.dumps(params)
    hmac_obj = hmac.new(secret, (path + chr(0) + data).encode(), hashlib.sha512)
    hmac_sign = base64.b64encode(hmac_obj.digest())

    headers = {
        'Content-Type': 'application/json',
        'Rest-Key': key,
        'Rest-Sign': hmac_sign,
        'User-Agent': 'Americas Test Client'
    }
    response = requests.post(base + path, headers=headers, data=data)
    result_sell = response.json()
    sellPrice = 0
    if result_sell['resultCode'] == 'OK':
        sellPrice = float(result_sell['quoteResponse']['retailRateInSettlementCurrency'])
        
    return [qty*buyPrice, qty*sellPrice]

