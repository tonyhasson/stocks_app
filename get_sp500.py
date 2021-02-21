import mysql.connector
from mysql.connector import Error
import bs4 as bs
import requests
import yfinance as yf
import datetime



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


##for feeding data to the table
def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        #print("Query successful")
    except Error as err:
        print(f"Error: '{err}'")





connection = create_server_connection("127.0.0.1", "tony", "tonton12", "stock_db")

resp = requests.get('http://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
soup = bs.BeautifulSoup(resp.text, 'lxml')
table = soup.find('table', {'class': 'wikitable sortable'})
tickers = []
for row in table.findAll('tr')[1:]:
    ticker = row.findAll('td')[0].text
    tickers.append(ticker)

tickers = [s.replace('\n', '') for s in tickers]

#start = datetime.datetime(2019,1,1) ##you can choose a range of dates
#end = datetime.datetime(2019,7,17)

data = yf.download(tickers, period="5d")##you can change period of dates

data["Date"] = data.index##add Date as a column
i=0

while i<len(tickers):
    j=0
    t=tickers[i]
    print(t)

    while j<len(data['Date']):
        q1="""INSERT INTO `stock_db`.`fl_test`
            (`stock_name`,
            `stock_price`,
            `stock_date`)
            VALUES
            ('"""+t+"""',
            """+str(data['Close'][t][j])+""",
            '"""+str(data['Date'][j])+"""');"""
        execute_query(connection,q1)

        j+=1
    i+=1
