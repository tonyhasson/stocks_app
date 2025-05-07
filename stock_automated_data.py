import mysql.connector
from mysql.connector import Error
import pandas as pd
import datetime
import matplotlib.pyplot as plt
import yfinance as yf
import os
from tqdm import tqdm
import requests,bs4,re
from curl_cffi import requests
from requests.packages.urllib3.util.retry import Retry
today=datetime.date.today()

##functions


##creating server connection/database:

##pw=input("enter password")
###connection = create_server_connection("127.0.0.1", "tony", pw)

def create_server_connection(host_name, user_name, user_password,database_name):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            database=database_name
        )
        #print("MySQL Database connection successful")
    except Error as err:
        print(f"Error: '{err}'")

    return connection




##creating database:

##query_type="CREATE DATABASE Stock_DB"
##create_database(connection,query_type)
def create_database(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        #print("Database created successfully")
    except Error as err:
        print(f"Error: '{err}'")



##for feeding data to the table
def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        #print("Query successful")
    except Error as err:
        print(f"Error: '{err}'")

##for reading data from table
def read_query(connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as err:
        print(f"Error: '{err}'")


##specific scrapping for a stock that doesn't appear in yahoo finance
def nadlan_price():

    ##getting USD to ILS ratio

    url = 'https://www.xe.com/currencyconverter/convert/?Amount=1&From=USD&To=ILS'
    req=requests.get(url)
    soup = bs4.BeautifulSoup(req.text, 'html.parser')
    # get dollar to shekel ratio
    data_dollar=soup.find("p",attrs={"class":"result__BigRate-sc-1bsijpp-1 iGrAod"})

    # clean text and cast to float
    without=re.compile('[^0-9.]')
    x=without.sub('',data_dollar.text)
    data_dollar=float(x)

    ##getting nadlan price

    ##this website changes the classes names every day

    # url="https://finance.themarker.com/etf/1148964"
    # req=requests.get(url)
    # soup = bs4.BeautifulSoup(req.text, 'html.parser')
    # # get nadlan stock price
    # data_nadlan=soup.find("span",attrs={"class":"ls ax lt kr fn lu lv"})
    # # clean text and cast to float
    # without=re.compile(',')
    # x=without.sub('',data_nadlan.text)
    # x=float(x)

    ##fixing SSL problem
    requests.packages.urllib3.disable_warnings()
    requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS += ':HIGH:!DH:!aNULL'
    try:
        requests.packages.urllib3.contrib.pyopenssl.util.ssl_.DEFAULT_CIPHERS += ':HIGH:!DH:!aNULL'
    except AttributeError:
        # no pyopenssl support used / needed / available
        pass

    url = "https://finance.sponser.co.il/finance/etf/?s=6"
    req = requests.get(url, verify=False)
    soup = bs4.BeautifulSoup(req.text, 'html.parser')

    table = soup.find("table", attrs={"id": "portfolioTable"})  # Grab the first table

    previous = ""
    now = ""
    found = False
    for tr in table.find_all("tr"):
        if not found:
            for td in tr:
                if not found:
                    for i in td:
                        if not found:
                            for x in i:
                                if x == "\n":
                                    continue
                                previous = now
                                now = x
                                if previous == """הראל סל ת"א נדל"ן""":
                                    found = True
                                    break

    x = without.sub('', now)
    x = float(x)


    return x/data_dollar




def input_daily_data(user_name):

    print("\nNow Updating %s's data\n"%(user_name))


    ##getting data about stock name,price and amount.
    q1 = """
    SELECT Stock_Name,Stock_Amount,Stock_Price FROM stock_db.stock_data_"""+user_name+""";   
    """

    connection = create_server_connection("127.0.0.1", "tony", "tonton12", "stock_db")
    results = read_query(connection, q1)
    arr = []
    for result in results:
        result = result
        arr.append(result)
    columns = ["stock_name", "stock_amount", "stock_price"]
    df = pd.DataFrame(arr, columns=columns)



    stock_price = []
    total_price = 0
    percents = []
    string_for_sql = "INSERT INTO stock_data_"+user_name+" VALUES"
    ##creating new total price and updating prices


    for i in tqdm(range(len(arr)),desc="loading..."):##tqdm is for the loading bar

        stock_name = df['stock_name'][i]
        stock_amount = df['stock_amount'][i]
        if stock_amount > 0:
            session = requests.Session(impersonate="chrome")
            tickerData = yf.Ticker(stock_name,session=session)
            x = tickerData.history(period='1d')
            if not x.empty:
                #current_hour = datetime.datetime.now().hour
                #if current_hour < 16:
                #    stock_price.append(x['Close'][1])
                #else:
                #     stock_price.append(x['Close'][0])
                try:
                    stock_price.append(x['Close'][1])
                except IndexError:
                    stock_price.append(x['Close'][0])
            if x.empty:
                if stock_name=="nadlan":
                    try:
                        stock_price.append(nadlan_price())
                    except:
                        print("error in scrapping nadlan price/dollar price")
                        stock_price.append(df['stock_price'][i])
                else:
                    stock_price.append(df['stock_price'][i])
            total_price += stock_price[i] * stock_amount





    i=0
    ##creating sql strings and inputing the data back to the databases
    while i < len(arr):
        stock_percent = (stock_price[i] * df['stock_amount'][i] * 100) / total_price
        percents.append(stock_percent)
        temp_name = "'"
        temp_name += str(df['stock_name'][i])
        temp_name += "'"
        string_for_sql+="""('"""+str(today)+"""'  , """+ temp_name +""" , """+ str(df['stock_amount'][i]) +""" ,  """+ str(
            stock_price[i]) +""" ,  """+ str(stock_percent) +""" )"""
        if i < len(arr) - 1:
            string_for_sql += ","
        i += 1
    string_for_sql += ';'
    string_truncate="TRUNCATE `stock_db`.`stock_data_"+user_name+"`;"
    connection = create_server_connection("127.0.0.1", "tony", "tonton12", "stock_db")
    execute_query(connection, string_truncate) ##deleting the old data
    execute_query(connection, string_for_sql)  ##inserting the new data
    string_total="""INSERT INTO stock_total_"""+user_name+""" VALUES('"""+str(today)+"""' , """+str(total_price)+""");"""
    execute_query(connection, string_total)  ##inserting the new total price


     ##creating pie chart
    fig1, ax1 = plt.subplots()
    text = "total dollars invested: " + str(total_price) + ""
    plt.title(text, fontdict=None, loc='center', pad=None)
    ax1.pie(percents, labels=df['stock_name'], autopct='%1.1f%%',
            shadow=True, startangle=90)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.



    pie_path = r'C:\Users\tonyh\OneDrive\Desktop\מניות\portfolio photos'
    pie_path+="\\"
    pie_path+=user_name
    pie_path += "\\"
    pie_path += str(today.year)

    ##creates folder if doesn't exist
    if not os.path.exists(pie_path):
           os.makedirs(pie_path)


    pie_path += "\\"
    pie_path += str(today)
    pie_path+=".png"
    plt.savefig(pie_path, bbox_inches='tight')


def main():
    q1 = """
        SELECT idUser_Names,Name,automate FROM stock_db.user_names;   
        """

    connection = create_server_connection("127.0.0.1", "tony", "tonton12", "stock_db")
    results = read_query(connection, q1)
    arr = []
    for result in results:
        result = result
        arr.append(result)
    columns = ["id", "Name","Auto"]
    df = pd.DataFrame(arr, columns=columns)
    i = 0
    while i < len(arr):
        if df["Auto"][i]==1:

            input_daily_data(df["Name"][i])
        i += 1






#connection = create_server_connection("127.0.0.1", "tony", "tonton12","stock_db")
#execute_query(connection, string)


#generic csv table

#create_table = """
#CREATE TABLE stock_data_"""+name+""" (
 # `stock_date` DATETIME NOT NULL,
  #`stock_name` VARCHAR(45) NOT NULL,
  #`stock_amount` DOUBLE NOT NULL,
  #`stock_price` DOUBLE NOT NULL,
  #`stock_percent` DOUBLE NOT NULL)
#ENGINE = CSV;
# """


##"TRUNCATE `stock_db`.`stock_data`;"







main()






