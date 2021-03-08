import bs4 as bs
import requests
import yfinance as yf
import datetime
from pymongo import MongoClient


client = MongoClient(r'mongodb+srv://stockin_user:tonton12@cluster0.vorak.mongodb.net/test')
db = client.stock_info

stock_exchange_full_name = ['American Stock Exchange', 'London Stock Exchange', 'Nasdaq Stock Exchange',
                            'New York Stock Exchange', 'Torontro Stock Exchange']
stock_exchange_name = ['AMEX', 'LSE', 'NASDAQ', 'NYSE', 'TSX']
tickers = []
full_names = []
pos = 0
for exchange_name in stock_exchange_name:##run on all exchange names
    print("now scraping stock exchange: " + exchange_name)
    temp_exchange = stock_exchange_full_name[pos]
    string_stock_exchange = 'https://www.eoddata.com/stocklist/'  ##website to scrap stock data
    string_stock_exchange += exchange_name
    string_stock_exchange += "/"
    string_check_letters = string_stock_exchange
    string_check_letters += '.htm'
    resp = requests.get(string_check_letters)  ##scrapping for first letters
    soup = bs.BeautifulSoup(resp.text, 'lxml')
    table = soup.find('table', {'class': 'lett'})
    first_letter = []
    i = 0
    for row in table.findAll('td')[0:]:
        letter = table.findAll('td')[i].text
        i += 1
        first_letter.append(letter)

    for letter in first_letter:##run on all letters in exchange name
        print("now scraping letter: " + letter +" in stock exchange: "+temp_exchange)

        string_scrap = string_stock_exchange
        string_scrap += letter
        string_scrap += '.htm'
        resp = requests.get(string_scrap)
        soup = bs.BeautifulSoup(resp.text, 'lxml')
        table = soup.find('table', {'class': 'quotes'})

        tickers = []
        full_names = []

        ##get ticker
        for row in table.findAll('tr')[1:]:
            ticker = row.findAll('td')[0].text
            tickers.append(ticker)

        ##get full name
        for row in table.findAll('tr')[1:]:
            name = row.findAll('td')[1].text
            full_names.append(name)


        if len(tickers) <= 500:  ##if amount of tickers is less than 500
            tickers = [s.replace('\n', '') for s in tickers]
            full_names = [s.replace('\n', '') for s in full_names]
            data = yf.download(tickers, period="5d")  ##you can change period of dates
            data["Date"] = data.index  ##add Date as a column

            i = 0
            while i < len(tickers):
                j = 0
                arr_date_price = []
                t = tickers[i]
                try:
                    if str(data['Close'][t][j]) != 'nan' and data['Close'][t][j]>=1:
                        while j < len(data['Date']):
                            if str(data['Close'][t][j]) != 'nan' and data['Close'][t][j]>=1:##checking for every date if it is relevant
                                obj = {
                                    'stock_date': data['Date'][j],
                                    'stock_price': str(data['Close'][t][j])
                                }
                                arr_date_price.append(obj)
                            j += 1

                        send_arr = {

                            'stock_ticker': t,
                            'stock_full_name': full_names[i],
                            'stock_exchange': temp_exchange,
                            'date_price_info': arr_date_price
                        }
                        db.history.insert_one(send_arr)

                    i += 1
                except:
                    i += 1
            print("finished inserting letter :" + letter)
        else:##if amount of tickers bigger than 500
            count = 1
            temp = len(tickers)
            while temp > 500:
                temp -= 500
                count += 1

            start_index = 0
            end_index = 500
            while count > 0:
                new_arr = tickers[start_index:end_index]
                name_arr = full_names[start_index:end_index]
                new_arr = [s.replace('\n', '') for s in new_arr]
                name_arr = [s.replace('\n', '') for s in full_names]
                data = yf.download(new_arr, period="5d")  ##you can change period of dates
                data["Date"] = data.index  ##add Date as a column

                i = 0
                while i < len(new_arr):
                    j = 0
                    arr_date_price = []
                    t = new_arr[i]
                    try:
                        if str(data['Close'][t][j]) != 'nan' and data['Close'][t][j]>=1:
                            while j < len(data['Date']):
                                if str(data['Close'][t][j]) != 'nan' and data['Close'][t][j] >= 1:  ##checking for every date if it is relevant
                                    obj = {
                                        'stock_date': data['Date'][j],
                                        'stock_price': str(data['Close'][t][j])
                                    }
                                    arr_date_price.append(obj)
                                j += 1

                            send_arr = {

                                'stock_ticker': t,
                                'stock_full_name': name_arr[i],
                                'stock_exchange': temp_exchange,
                                'date_price_info': arr_date_price
                            }
                            db.history.insert_one(send_arr)
                        i += 1

                    except:
                        i += 1

                start_index += 500
                if end_index + 500 > len(tickers):
                    end_index = len(tickers)
                else:
                    end_index += 500
                count -= 1
            print("finished inserting letter :" + letter)

    pos += 1

print("finished all!!")
