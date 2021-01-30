import mysql.connector
from mysql.connector import Error
import pandas as pd
import datetime
import matplotlib.pyplot as plt
import yfinance as yf

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
        print("MySQL Database connection successful")
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
        print("Database created successfully")
    except Error as err:
        print(f"Error: '{err}'")



##for feeding data to the table
def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("Query successful")
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

def input_daily_data(user_name):
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


    i = 0
    stock_price = []
    total_price = 0
    percents = []
    string_for_sql = "INSERT INTO stock_data_"+user_name+" VALUES"
    ##creating new total price and updating prices
    while i < len(arr):
        stock_name = df['stock_name'][i]
        stock_amount = df['stock_amount'][i]
        if stock_amount > 0:
            tickerData = yf.Ticker(stock_name)
            x = tickerData.history(period='1s')
            if not x.empty:
                stock_price.append(x['Close'][1])
            if x.empty:
                stock_price.append(df['stock_price'][i])
            total_price += stock_price[i] * stock_amount

        i += 1
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
    execute_query(connection, string_for_sql)  ##updating the new data
    string_total="""INSERT INTO stock_total_"""+user_name+""" VALUES('"""+str(today)+"""' , """+str(total_price)+""");"""
    execute_query(connection, string_total)  ##updating the total price
def main():
    q1 = """
        SELECT idUser_Names,Name FROM stock_db.user_names;   
        """

    connection = create_server_connection("127.0.0.1", "tony", "tonton12", "stock_db")
    results = read_query(connection, q1)
    arr = []
    for result in results:
        result = result
        arr.append(result)
    columns = ["id", "Name"]
    df = pd.DataFrame(arr, columns=columns)
    i = 0
    while i < len(arr):
        input_daily_data(df["Name"][i])
        i += 1




#string="""INSERT INTO stock_data VALUES('"""+str(today)+"""' ,'tsla',2.168765, 846.6400146484375, 10.540399775143548),
#('"""+str(today)+"""' ,'msft',4.227177, 225.9499969482422, 5.482877833693618),('"""+str(today)+"""' ,'fb',3.496403, 274.5,
#5.509467550653445),('"""+str(today)+"""' ,'googl',1.246987, 1892.56005859375, 13.547444882800088),('"""+str(today)+"""' ,'dis',11.337674,
#172.77999877929688, 11.245097580014473),('"""+str(today)+"""' ,'qqq',2.561224, 325.4200134277344, 4.784511666942775),
#('"""+str(today)+"""' ,'cgc',11.0, 33.79999923706055, 2.134298563977845),('"""+str(today)+"""' ,'baba',7.0, 258.6199951171875,
#10.392162658893206),('"""+str(today)+"""' ,'v',4.0, 202.02000427246094, 4.638741417385458),('"""+str(today)+"""' ,'hexo',42.0,
#6.690000057220459, 1.6129511274131048),('"""+str(today)+"""' ,'arkk',6.0, 146.0800018310547, 5.031388033965828),('"""+str(today)+"""' ,
#'tan',15.0, 120.97000122070312, 10.416330246808755),('"""+str(today)+"""' ,'nadlan',4.99, 244.673, 7.008617991430818),
#('"""+str(today)+"""' ,'electreon',7.0, 83.49, 3.3548900965597905),('"""+str(today)+"""' ,'voo',2.129052, 351.8999938964844,
#4.300820574317238); """

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



