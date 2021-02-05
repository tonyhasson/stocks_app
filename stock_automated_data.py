import mysql.connector
from mysql.connector import Error
import pandas as pd
import datetime
import matplotlib.pyplot as plt
import yfinance as yf
import os
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
                current_hour = datetime.datetime.now().hour
                if current_hour < 16:
                    stock_price.append(x['Close'][1])
                else:
                    stock_price.append(x['Close'][0])
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


