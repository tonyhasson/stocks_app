
import matplotlib.pyplot as plt
import yfinance as yf
import shelve
from selenium import webdriver
from bs4 import BeautifulSoup
import requests as rq
import pandas as pd
import plotly.express as px


import mysql.connector
from mysql.connector import Error
import datetime




##classes:

class stock(object):
    def __init__(self, name, price,amount):
        self.name = name
        self.price = price
        self.amount=amount
        self.percent=0






##sql functions:

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


##creating database
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

today=datetime.date.today()




##functions:


def create_stock_portfolio():
    q1 = """
            SELECT idUser_Names,Name,automate,portfolio FROM stock_db.user_names;   
            """

    connection = create_server_connection("127.0.0.1", "tony", "tonton12", "stock_db")
    results = read_query(connection, q1)
    arr = []
    for result in results:
        result = result
        arr.append(result)
    columns = ["id", "Name", "Auto","portfolio"]
    df = pd.DataFrame(arr, columns=columns)
    if df["portfolio"][id_global] == 0:
        create_table_data = """
                 CREATE TABLE stock_data_""" + name + """ (
                 `stock_date` DATETIME NOT NULL,
                 `stock_name` VARCHAR(45) NOT NULL,
                 `stock_amount` DOUBLE NOT NULL,
                 `stock_price` DOUBLE NOT NULL,
                 `stock_percent` DOUBLE NOT NULL)
                 ENGINE = InnoDB;
                 """
        create_table_total = """
                     CREATE TABLE stock_total_""" + name + """ (
                     `stock_date` DATETIME NOT NULL,
                     `stock_total` DOUBLE NOT NULL)
                     ENGINE = CSV;
                     """

        input_data_to_table = "INSERT INTO stock_data_" + name + " VALUES"
        execute_query(connection, create_table_data)
        execute_query(connection, create_table_total)
        i = 0
        total_price = 0
        a = []
        amount_of_stocks = int(input("enter amount of stocks you want to enter: "))

        while i < amount_of_stocks:
            stock_name = input("enter a stock exact ticker(if the stock is international,if not enter 0): ")
            if stock_name != '0':
                tickerData = yf.Ticker(stock_name)
                x = tickerData.history(period='1s')
                stock_price = x['Close'][1]
            else:
                stock_name = input("enter israeli stock name: ")
                stock_price = float(input("enter a stock price: "))

            stock_amount = float(input("enter amount of stocks owned: "))
            total_price += stock_price * stock_amount
            new_stock = stock(stock_name, stock_price, stock_amount)
            a.append(new_stock)
            if i < amount_of_stocks - 1:
                print("new stock ")
            i += 1

        print("total price is :" + str(total_price) + "")

        i = 0
        while i < amount_of_stocks:
            a[i].percent = float((a[i].price * a[i].amount * 100) / total_price)
            temp_name = "'"
            temp_name += str(a[i].name)
            temp_name += "'"
            input_data_to_table += """('""" + str(today) + """'  , """ + temp_name + """ , """ + str(
                a[i].amount) + """ ,  """ + str(
                a[i].price) + """ ,  """ + str(a[i].percent) + """ )"""
            if i < amount_of_stocks - 1:
                input_data_to_table += ","
            print("name:" + str(a[i].name) + "   price: " + str(a[i].price) + "   amount: " + str(
                a[i].amount) + "  percent: " + str(a[i].percent) + "%")
            i += 1

        input_data_to_table += ";"
        str_portfolio = """UPDATE `stock_db`.`user_names` SET `portfolio` = '1' WHERE (`Name` = '""" + name + """');"""
        string_total = """INSERT INTO stock_total_""" + name + """ VALUES('""" + str(today) + """' , """ + str(
            total_price) + """);"""
        execute_query(connection, string_total)  ##updating the total price
        execute_query(connection, input_data_to_table)  ##updating stock data
        execute_query(connection, str_portfolio)  ##updating portfolio created(turn 0 to 1)


    elif df["portfolio"][id_global] == 1:
        print("portfolio already created!")





def ftr_st_clc():
    q1 = """
               SELECT idUser_Names,Name,automate,portfolio FROM stock_db.user_names;   
               """

    connection = create_server_connection("127.0.0.1", "tony", "tonton12", "stock_db")
    results = read_query(connection, q1)
    arr = []
    for result in results:
        result = result
        arr.append(result)
    columns = ["id", "Name", "Auto", "portfolio"]
    df = pd.DataFrame(arr, columns=columns)
    if df["portfolio"][id_global] == 1:

        q1 = """
                    SELECT stock_total FROM stock_db.stock_total_""" + name + """;   
                    """

        connection = create_server_connection("127.0.0.1", "tony", "tonton12", "stock_db")
        results = read_query(connection, q1)
        arr_data = []
        for result in results:
            result = result
            arr_data.append(result)
        columns = ["stock_total"]
        df = pd.DataFrame(arr_data, columns=columns)

        amount_rn =df["stock_total"][len(arr_data)-1]

        print("current balance:",amount_rn)
        mnths=12
        i=0
        percent=6
        while(percent<=20):

            print("current precent: "+str(percent))
            yrs = 25
            amount_pm = 600
            amount_temp=amount_rn
            count = 0
            while yrs <= 60:

                if yrs>30:
                    amount_pm=2000


                prcnt = 1 +percent*0.01
                amount_temp += amount_pm * mnths
                amount_temp*=prcnt
                if amount_temp>=1000000:
                    if count==0:
                        print("year of the million: "+str(yrs))
                        print("")
                        count+=1



                if yrs % 5 == 0:

                    print("age: "+str(yrs)+"future balance: "+str(amount_temp)+" ")
                yrs+=1
            percent+=5
            i+=1
            print("")
            print("")
            print("")

    else:
        print("you need to create a portfolio first!")




def show_stk_prtlfo():
    q1 = """
                SELECT idUser_Names,Name,automate,portfolio FROM stock_db.user_names;   
                """

    connection = create_server_connection("127.0.0.1", "tony", "tonton12", "stock_db")
    results = read_query(connection, q1)
    arr_user = []
    for result in results:
        result = result
        arr_user.append(result)
    columns = ["id", "Name", "Auto", "Portfolio"]
    df_user = pd.DataFrame(arr_user, columns=columns)
    if df_user["Portfolio"][id_global] == 1:
        ##getting data about stock name,price and amount.
        q1 = """
            SELECT Stock_Name,Stock_Amount,Stock_Price FROM stock_db.stock_data_""" + name + """;   
            """

        connection = create_server_connection("127.0.0.1", "tony", "tonton12", "stock_db")
        results = read_query(connection, q1)
        arr_data = []
        for result in results:
            result = result
            arr_data.append(result)
        columns = ["stock_name", "stock_amount", "stock_price"]
        df = pd.DataFrame(arr_data, columns=columns)
        i = 0


        stock_price = []
        total_price = 0
        percents = []
        string_for_sql = "INSERT INTO stock_data_" + name + " VALUES"
        ##creating new total price and updating prices
        while i < len(arr_data):
            stock_name = df['stock_name'][i]
            stock_amount = df['stock_amount'][i]
            tickerData = yf.Ticker(stock_name)
            x = tickerData.history(period='1s')

            if not x.empty:
                 current_hour = datetime.datetime.now().hour
                 if current_hour<16:
                    stock_price.append(x['Close'][1])
                 else:
                     stock_price.append(x['Close'][0])
            if x.empty:
                stock_price.append(df['stock_price'][i])

            total_price += stock_price[i] * stock_amount

            i += 1

        i = 0
        ##creating sql strings and inputing the data back to the databases
        while i < len(arr_data):
            stock_percent = (stock_price[i] * df['stock_amount'][i] * 100) / total_price
            percents.append(stock_percent)

            print("name :" + str(df['stock_name'][i]) + "  amount: " + str(
                df['stock_amount'][i]) + "  price: " + str(
                stock_price[i]) + " percent: " + str(stock_percent))

            temp_name = "'"
            temp_name += str(df['stock_name'][i])
            temp_name += "'"
            string_for_sql += """('""" + str(today) + """'  , """ + temp_name + """ , """ + str(
                df['stock_amount'][i]) + """ ,  """ + str(
                stock_price[i]) + """ ,  """ + str(stock_percent) + """ )"""
            if i < len(arr_data) - 1:
                string_for_sql += ","
            i += 1
        string_for_sql += ';'
        string_truncate = "TRUNCATE `stock_db`.`stock_data_" + name + "`;"
        connection = create_server_connection("127.0.0.1", "tony", "tonton12", "stock_db")
        execute_query(connection, string_truncate)  ##deleting the old data
        execute_query(connection, string_for_sql)  ##updating the new data
        if df_user["Auto"][id_global]==0:

            string_truncate = "TRUNCATE `stock_db`.`stock_total_" + name + "`;"
            execute_query(connection, string_truncate)  ##deleting the old data
            string_total = """INSERT INTO stock_total_""" + name + """ VALUES('""" + str(today) + """' , """ + str(
                total_price) + """);"""
            execute_query(connection, string_total)  ##inserting the new total price

        ##showing pie chart
        fig1, ax1 = plt.subplots()
        text = "total dollars invested: " + str(total_price) + ""
        plt.title(text, fontdict=None, loc='center', pad=None)
        ax1.pie(percents, labels=df['stock_name'], autopct='%1.1f%%',
                shadow=True, startangle=90)
        ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        plt.show()


    else:
        print("you need to create a stock portfolio first!")








##updating amount of a specific stock
def update_amount():
    q1 = """
                               SELECT idUser_Names,Name,automate,portfolio FROM stock_db.user_names;   
                               """

    connection = create_server_connection("127.0.0.1", "tony", "tonton12", "stock_db")
    results = read_query(connection, q1)
    arr_user = []
    for result in results:
        result = result
        arr_user.append(result)
    columns = ["id", "Name", "Auto", "Portfolio"]
    df = pd.DataFrame(arr_user, columns=columns)

    if df["Portfolio"][id_global] == 1:

        stock_name = ""
        tmp = -1
        while stock_name != "stop":
            stock_name = input(
                "enter existing stock in your portfolio or a new stock you wish to add or stop to quit the function: ")
            if stock_name != "stop":

                    i = 0
                    tmp = -1

                    q1 = """
                                        SELECT Stock_Name,Stock_Amount,Stock_Price FROM stock_db.stock_data_""" + name + """;   
                                        """

                    connection = create_server_connection("127.0.0.1", "tony", "tonton12", "stock_db")
                    results = read_query(connection, q1)
                    arr_data = []
                    for result in results:
                        result = result
                        arr_data.append(result)
                    columns = ["stock_name", "stock_amount", "stock_price"]
                    df = pd.DataFrame(arr_data, columns=columns)

                    while i<len(arr_data):
                        if df["stock_name"][i]==stock_name:
                            tmp=i
                        i+=1


                    if tmp!=-1:
                         new_amount=float(input("enter new amount:"))
                         string_update_amount = """UPDATE stock_data_""" + name + """
                         SET
                         stock_amount = """ + str(new_amount) + """
                         WHERE stock_name='"""+str(stock_name)+"""';
                         """
                         execute_query(connection, string_update_amount)
                         print("amount is updated!")



                    else: ##stock not in portfolio
                        tickerData = yf.Ticker(stock_name)
                        x = tickerData.history(period='1s')

                        if not x.empty: ##stock is in yahoo finance
                            new_amount = float(input("enter new amount:"))
                            string_new_stock="""INSERT INTO stock_data_"""+str(name)+""" VALUES('"""+str(today)+"""' ,'"""+str(stock_name)+"""',"""+str(new_amount)+""", 0, 0);"""
                            execute_query(connection, string_new_stock)
                            print("amount is updated!")


                        if x.empty: ##stock is not in yahoo finance
                            stock_name = input("enter israeli stock name: ")
                            stock_price = float(input("enter a stock price: "))
                            new_amount = float(input("enter new amount:"))
                            string_new_stock = """INSERT INTO stock_data_"""+str(name)+""" VALUES('""" + str(today) + """' ,'""" + str(
                                stock_name) + """',""" + str(new_amount) + """, """+str(stock_price)+""", 0);"""
                            execute_query(connection, string_new_stock)

                            print("amount is updated!")

                    if new_amount==0:
                        string_d2="SET SQL_SAFE_UPDATES = 0;"
                        string_d3="""DELETE FROM stock_data_"""+str(name)+"""
                                        WHERE stock_name='"""+str(stock_name)+"""';"""
                        string_d4="SET SQL_SAFE_UPDATES = 1;"
                        execute_query(connection, string_d2)
                        execute_query(connection, string_d3)
                        execute_query(connection, string_d4)

    else:
        print("you need to create a stock portfolio first!")



##adding a new user to the automated daily function
def auto_func():
    q1 = """
            SELECT idUser_Names,Name,automate,portfolio FROM stock_db.user_names;   
            """

    connection = create_server_connection("127.0.0.1", "tony", "tonton12", "stock_db")
    results = read_query(connection, q1)
    arr = []
    for result in results:
        result = result
        arr.append(result)
    columns = ["id", "Name", "Auto","Portfolio"]
    df = pd.DataFrame(arr, columns=columns)
    if df["Auto"][id_global] == 0 and df["Portfolio"][id_global] == 1:
        str_insert="""UPDATE user_names
                         SET
                         automate = """+str(1)+"""
                         WHERE Name='"""+str(name)+"""';
                         """
        execute_query(connection, str_insert)
    else:
        if df["Auto"][id_global] == 1:
             print("you are already using the daily function!")
        if df["Portfolio"][id_global] == 0:
            print("you need to create a stock portfolio first!")


def graph():
    q1 = """
               SELECT idUser_Names,Name,automate,portfolio FROM stock_db.user_names;   
               """

    connection = create_server_connection("127.0.0.1", "tony", "tonton12", "stock_db")
    results = read_query(connection, q1)
    arr = []
    for result in results:
        result = result
        arr.append(result)
    columns = ["id", "Name", "Auto", "Portfolio"]
    df = pd.DataFrame(arr, columns=columns)
    if df["Auto"][id_global]==1:

        q1 = """
                   SELECT stock_date,stock_total FROM stock_db.stock_total_"""+name+""";   
                   """

        connection = create_server_connection("127.0.0.1", "tony", "tonton12", "stock_db")
        results = read_query(connection, q1)
        arr = []
        for result in results:
            result = result
            arr.append(result)
        columns = ["date", "price"]
        df = pd.DataFrame(arr, columns=columns)


        fig = px.line(df, x='date', y='price', title='Time Series with Range Slider and Selectors')

        fig.update_xaxes(
            rangeslider_visible=True,
            rangeselector=dict(
                buttons=list([
                    dict(count=1, label="1m", step="month", stepmode="backward"),
                    dict(count=6, label="6m", step="month", stepmode="backward"),
                    dict(count=1, label="YTD", step="year", stepmode="todate"),
                    dict(count=1, label="1y", step="year", stepmode="backward"),
                    dict(step="all")
                ])
            )
        )
        fig.show()

    else:
        print("you need to use the automated portfolio function to see the graph!")
##main function
def main_menu():
    option=0
    print("hello " + name + "!")
    while option!=-1:
        print("")
        print("choose a number:")
        print("create stock portfolio:1")
        print("future stock calculator:2")
        print("show saved stock portfolio:3 ")
        print("update stock amount/add new stock:4")
        print("start using daily automated portfolio function:5")
        print("show graph of total portfolio by date:6")
        print("to quit program:-1")
        option=int(input(""))
        if option==1:
            create_stock_portfolio()
        if option==2:
            ftr_st_clc()
        if option==3:
            show_stk_prtlfo()
        if option==4:
            update_amount()
        if option ==5:
            auto_func()
        if option ==6:
            graph()
    print("good bye " + name + "!")

def init(): ##logging in user name/creating a new user name
    q1 = """
            SELECT idUser_Names,Name FROM stock_db.user_names;   
            """
    i = 0
    tf = 0
    global name,id_global
    name = input("enter your name: ")

    results = read_query(connection, q1)
    arr = []
    for result in results:
        result = result
        arr.append(result)
    columns = ["id", "Name"]
    df = pd.DataFrame(arr, columns=columns)
    i = 0
    while i < len(arr):
        if df["Name"][i]==name:
            tf=1
            id_global=i
        i += 1
    if tf==0:
        string_for_sql = """INSERT INTO `stock_db`.`user_names` (`idUser_Names`, `Name`, `automate`,`portfolio`) VALUES ('"""+str(i)+"""', '"""+name+"""', '0','0');"""
        execute_query(connection, string_for_sql)
        id_global=i




connection = create_server_connection("127.0.0.1", "tony", "tonton12", "stock_db")
init()
main_menu()







