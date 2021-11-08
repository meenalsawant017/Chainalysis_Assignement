import threading
import requests
import time

#Create Class to store exchange info, bid and ask prices for ticker
class pricing_info:
    def __init__(self, excg, bid_px, bid_sz, ask_px, ask_sz):
        self.excg = excg
        self.bid_px = bid_px
        self.bid_sz = bid_sz
        self.ask_px = ask_px
        self.ask_sz = ask_sz
exchg_price = {} 

#Create function to fetch data from Binance exchange
def binance_book(api_url):

    #Making a get request 
    response = requests.get(api_url)
    ans = response.json()

    #Store Bid Price, Bid Size, Ask Price, Ask Size  
    excg = 'Binance'
    bid_px = ans['bids'][0][0]
    bid_sz = ans['bids'][0][1]
    ask_px = ans['asks'][0][0]
    ask_sz = ans['asks'][0][1]

    #Store the value in the form of Node
    pinfo = pricing_info(excg, bid_px, bid_sz, ask_px, ask_sz)

    # Add into dictionary
    if 'Binance_BTC' not in exchg_price:
        exchg_price['Binance'] = pinfo
    else:
        exchg_price['Binance'] = pinfo
        
    return exchg_price

#Create function to fetch data from Bitstamp exchange
def bitstamp_book(api_url):

    #Making a get request
    response = requests.get(api_url)
    ans = response.json()

    #Store Bid Price, Bid Size, Ask Price, Ask Size  
    excg = "Bitstamp"
    bid_px = ans['bids'][0][0]
    bid_sz = ans['bids'][0][1]
    ask_px = ans['asks'][0][0]
    ask_sz = ans['asks'][0][1]

    #Store the value in the form of Node
    pinfo = pricing_info(excg, bid_px, bid_sz, ask_px, ask_sz)

    # Add into dictionary
    if 'Bitstamp_BTC' not in exchg_price:
        exchg_price['Bitstamp'] = pinfo
    else:
        exchg_price['Bitstamp'] = pinfo

    return exchg_price

# Process the data gathered from both the exchanges using multithreading technique
def sort_BTC(api_url_binance, api_url_bitstamp):
    t = time.time()

    t1= threading.Thread(target=binance_book, args=(api_url_binance,))
    t2= threading.Thread(target=bitstamp_book, args=(api_url_bitstamp,))

    t1.start()
    t2.start()

    t1.join()
    t2.join()
    
    # Sort the bid price in descending order and Ask price in ascending order
    bid_px_sorted   = dict(sorted(exchg_price.items(), key=lambda item: item[1].bid_px, reverse = True))
    ask_px_sorted   = dict(sorted(exchg_price.items(), key=lambda item: item[1].ask_px))
    
    return bid_px_sorted, ask_px_sorted
    
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def webpage():

    # Excahnges URLs for Bitcoin
    api_url_binance_BTC = "https://api1.binance.com/api/v3/depth?symbol=BTCUSDT&limit=1"
    api_url_bitstamp_BTC = "https://www.bitstamp.net/api/v2/order_book/btcusdt/"

    # Call multithreading function to fetch the exachnge data from two exchanges simultanueously
    get_val = sort_BTC(api_url_binance_BTC, api_url_bitstamp_BTC)

    # Data variables
    BTC_Bid = get_val[0]
    BTC_Ask = get_val[1]

    get_bid_px = str(list(BTC_Bid.keys())[0])
    get_bid_excg = exchg_price[get_bid_px].excg
    val_bid_px = exchg_price[get_bid_px].bid_px
    val_bid_sz =exchg_price[get_bid_px].bid_sz

    get_ask_px = str(list(BTC_Ask.keys())[0])
    get_ask_excg = exchg_price[get_ask_px].excg
    val_ask_px = exchg_price[get_ask_px].ask_px
    val_ask_sz =exchg_price[get_ask_px].ask_sz

    
    get_bid_px_2 = str(list(BTC_Bid.keys())[1])
    get_bid_excg_2 = exchg_price[get_bid_px_2].excg
    val_bid_px_2 = exchg_price[get_bid_px_2].bid_px
    val_bid_sz_2 =exchg_price[get_bid_px_2].bid_sz

    get_ask_px_2 = str(list(BTC_Ask.keys())[1])
    get_ask_excg_2 = exchg_price[get_ask_px_2].excg
    val_ask_px_2 = exchg_price[get_ask_px_2].ask_px
    val_ask_sz_2 =exchg_price[get_ask_px_2].ask_sz
    

    # Excahnges URLs for Bitcoin
    api_url_binance_ETH = "https://api1.binance.com/api/v3/depth?symbol=ETHUSDT&limit=1"
    api_url_bitstamp_ETH = "https://www.bitstamp.net/api/v2/order_book/ethusdt/"

    # Call multithreading function to fetch the exachnge data from two exchanges simultanueously
    get_val_ETH  = sort_BTC(api_url_binance_ETH, api_url_bitstamp_ETH)

    # Data variables
    ETH_Bid = get_val_ETH[0]
    ETH_Ask = get_val_ETH[1]
    
    get_ETH_bid_px = str(list(ETH_Bid.keys())[0])
    get_ETH_bid_excg = exchg_price[get_ETH_bid_px].excg
    val_ETH_bid_px = exchg_price[get_ETH_bid_px].bid_px
    val_ETH_bid_sz =exchg_price[get_ETH_bid_px].bid_sz

    get_ETH_ask_px = str(list(ETH_Ask.keys())[0])
    get_ETH_ask_excg = exchg_price[get_ETH_ask_px].excg
    val_ETH_ask_px = exchg_price[get_ETH_ask_px].ask_px
    val_ETH_ask_sz =exchg_price[get_ETH_ask_px].ask_sz
  
    get_ETH_bid_px_2 = str(list(ETH_Bid.keys())[1])
    get_ETH_bid_excg_2 = exchg_price[get_ETH_bid_px_2].excg
    val_ETH_bid_px_2 = exchg_price[get_ETH_bid_px_2].bid_px
    val_ETH_bid_sz_2 =exchg_price[get_ETH_bid_px_2].bid_sz

    get_ETH_ask_px_2 = str(list(ETH_Ask.keys())[1])
    get_ETH_ask_excg_2 = exchg_price[get_ETH_ask_px_2].excg
    val_ETH_ask_px_2 = exchg_price[get_ETH_ask_px_2].ask_px
    val_ETH_ask_sz_2 =exchg_price[get_ETH_ask_px_2].ask_sz
    
    return render_template('webpage.html',
            bid_excg= get_bid_excg, bid_px= val_bid_px, bid_sz= val_bid_sz,
            ask_px=val_ask_px, ask_sz=val_ask_sz, ask_excg= get_ask_excg,
            bid_excg_2= get_bid_excg_2, bid_px_2= val_bid_px_2,bid_sz_2= val_bid_sz_2,
            ask_px_2=val_ask_px_2, ask_sz_2=val_ask_sz_2, ask_excg_2= get_ask_excg_2,
            ETH_bid_excg = get_ETH_bid_excg, ETH_bid_px = val_ETH_bid_px, ETH_bid_sz = val_ETH_bid_sz,
            ETH_ask_px=val_ETH_ask_px, ETH_ask_sz=val_ETH_ask_sz, ETH_ask_excg=get_ETH_ask_excg,
            ETH_bid_excg_2=get_ETH_bid_excg_2, ETH_bid_px_2=val_ETH_bid_px_2, ETH_bid_sz_2=val_ETH_bid_sz_2,
            ETH_ask_px_2=val_ETH_ask_px_2, ETH_ask_sz_2=val_ETH_ask_sz_2, ETH_ask_excg_2= get_ETH_ask_excg_2)
    

if __name__ == "__main__":
    app.run(debug=True, use_debugger=False, use_reloader=False)


