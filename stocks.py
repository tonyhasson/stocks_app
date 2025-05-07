
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import yfinance as yf
from plotly.graph_objs import Figure
from bs4 import BeautifulSoup
import requests as rq
import pandas as pd
import plotly.express as px
import tkinter as tk
import tksheet
from tkinter import ttk
import sys
import mysql.connector
from mysql.connector import Error
import datetime
from curl_cffi import requests












##classes:
class PrintToT1(object):
    def write(self, s):
        t1.insert(tk.END, s)


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


##for showing sql table in tkinter
def View_Stock_Data_Table():


    q1 = """
                        SELECT Stock_Name,Stock_Amount,Stock_Price,Stock_Percent FROM stock_db.stock_data_""" + name + """;   
                        """
    tree = ttk.Treeview(show_stk_prtlfo_window, column=("c1", "c2", "c3", "c4"), show='headings')
    tree.column("#1", anchor=tk.CENTER)
    tree.heading("#1", text="stock name")
    tree.column("#2", anchor=tk.CENTER)
    tree.heading("#2", text="stock amount")
    tree.column("#3", anchor=tk.CENTER)
    tree.heading("#3", text="stock price")
    tree.column("#4", anchor=tk.CENTER)
    tree.heading("#4", text="stock percent")
    tree.pack()


    connection = create_server_connection("127.0.0.1", "tony", "tonton12", "stock_db")
    results = read_query(connection, q1)
    for result in results:
        tree.insert("", tk.END, values=result)


def openNewWindow():
    # Toplevel object which will
    # be treated as a new window
    newWindow = tk.Toplevel(root)

    # sets the title of the
    # Toplevel widget
    newWindow.title("New Window")

    # sets the geometry of toplevel
    newWindow.geometry("800x600")

    # A Label widget to show in toplevel
    tk.Label(newWindow, text="This is a new window").pack()


def messagebox(text):
    window = tk.Toplevel(root)
    window.title("Message")
    window.geometry("300x100")


    l2 = tk.Label(window, text=text)
    l2.grid(row=0, column=1, columnspan=3, pady=(30, 10),padx=(40,10))



##functions:

##not used anymore

# def create_stock_portfolio():
#     q1 = """
#             SELECT idUser_Names,Name,automate,portfolio FROM stock_db.user_names;
#             """
#
#     connection = create_server_connection("127.0.0.1", "tony", "tonton12", "stock_db")
#     results = read_query(connection, q1)
#     arr = []
#     for result in results:
#         result = result
#         arr.append(result)
#     columns = ["id", "Name", "Auto","portfolio"]
#     df = pd.DataFrame(arr, columns=columns)
#     if df["portfolio"][id_global] == 0:
#         create_table_data = """
#                  CREATE TABLE stock_data_""" + name + """ (
#                  `stock_date` DATETIME NOT NULL,
#                  `stock_name` VARCHAR(45) NOT NULL,
#                  `stock_amount` DOUBLE NOT NULL,
#                  `stock_price` DOUBLE NOT NULL,
#                  `stock_percent` DOUBLE NOT NULL)
#                  ENGINE = InnoDB;
#                  """
#         create_table_total = """
#                      CREATE TABLE stock_total_""" + name + """ (
#                      `stock_date` DATETIME NOT NULL,
#                      `stock_total` DOUBLE NOT NULL)
#                      ENGINE = CSV;
#                      """
#
#         input_data_to_table = "INSERT INTO stock_data_" + name + " VALUES"
#         execute_query(connection, create_table_data)
#         execute_query(connection, create_table_total)
#         i = 0
#         total_price = 0
#         a = []
#         amount_of_stocks = int(input("enter amount of stocks you want to enter: "))
#
#         while i < amount_of_stocks:
#             stock_name = input("enter a stock exact ticker(if the stock is international,if not enter 0): ")
#             if stock_name != '0':
#                 tickerData = yf.Ticker(stock_name)
#                 x = tickerData.history(period='1d')
#                 stock_price = x['Close'][1]
#             else:
#                 stock_name = input("enter israeli stock name: ")
#                 stock_price = float(input("enter a stock price: "))
#
#             stock_amount = float(input("enter amount of stocks owned: "))
#             total_price += stock_price * stock_amount
#             new_stock = stock(stock_name, stock_price, stock_amount)
#             a.append(new_stock)
#             if i < amount_of_stocks - 1:
#                 print("new stock ")
#             i += 1
#
#         print("total price is :" + str(total_price) + "")
#
#         i = 0
#         while i < amount_of_stocks:
#             a[i].percent = float((a[i].price * a[i].amount * 100) / total_price)
#             temp_name = "'"
#             temp_name += str(a[i].name)
#             temp_name += "'"
#             input_data_to_table += """('""" + str(today) + """'  , """ + temp_name + """ , """ + str(
#                 a[i].amount) + """ ,  """ + str(
#                 a[i].price) + """ ,  """ + str(a[i].percent) + """ )"""
#             if i < amount_of_stocks - 1:
#                 input_data_to_table += ","
#             print("name:" + str(a[i].name) + "   price: " + str(a[i].price) + "   amount: " + str(
#                 a[i].amount) + "  percent: " + str(a[i].percent) + "%")
#             i += 1
#
#         input_data_to_table += ";"
#         str_portfolio = """UPDATE `stock_db`.`user_names` SET `portfolio` = '1' WHERE (`Name` = '""" + name + """');"""
#         string_total = """INSERT INTO stock_total_""" + name + """ VALUES('""" + str(today) + """' , """ + str(
#             total_price) + """);"""
#         execute_query(connection, string_total)  ##updating the total price
#         execute_query(connection, input_data_to_table)  ##updating stock data
#         execute_query(connection, str_portfolio)  ##updating portfolio created(turn 0 to 1)
#
#
#     elif df["portfolio"][id_global] == 1:
#         print("portfolio already created!")




##need to add it to tkinter
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

    ##creating new window
    global show_stk_prtlfo_window
    show_stk_prtlfo_window = tk.Toplevel(root)
    show_stk_prtlfo_window.geometry("800x600")



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
            session = requests.Session(impersonate="chrome")
            tickerData = yf.Ticker(stock_name,session=session)
            x = tickerData.history(period='1d')

            if not x.empty:
                 try:
                    stock_price.append(x['Close'][1])
                 except:
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

            #print("name :" + str(df['stock_name'][i]) + "  amount: " + str(
                #df['stock_amount'][i]) + "  price: " + str(
                #stock_price[i]) + " percent: " + str(stock_percent))

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

        ##creating stock data table
        show_stk_prtlfo_window.title("Stock Portfolio Data,Total Amount In Dollars: "+str(total_price))##title
        View_Stock_Data_Table()

        ##showing pie chart


        #fig1, ax1 = plt.subplots()
        #text = "total dollars invested: " + str(total_price) + ""
        #plt.title(text, fontdict=None, loc='center', pad=None)
        #ax1.pie(percents, labels=df['stock_name'], autopct='%1.1f%%',
                #shadow=True, startangle=90)
        #ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        #plt.show()



        figure2 = plt.Figure(figsize=(5,5), dpi=100)
        ax1 = figure2.add_subplot(111)
        text = "total dollars invested: " + str(total_price) + ""
        plt.title(text, fontdict=None, loc='center', pad=None)
        ax1.pie(percents, labels=df['stock_name'], autopct='%1.1f%%',
                 shadow=True, startangle=90)
        ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        pie2 = FigureCanvasTkAgg(figure2, show_stk_prtlfo_window)
        pie2.get_tk_widget().pack()






    else:
        messagebox("you need to create a stock portfolio first!")


    main_menu()





##updating amount of a specific stock

def init_update():
    global show_update_amount,entry_amount,entry_stock_name,ch
    show_update_amount = tk.Toplevel(root)
    show_update_amount.geometry("800x600")
    show_update_amount.title("Update Stock Amount ")

    l1=tk.Label(show_update_amount, text="Enter Stock Name",font=('Arial', 20))
    l1.grid(row=0, column=0, pady=(0, 300), padx=(280, 30))

    entry_stock_name = tk.Entry(show_update_amount)
    entry_stock_name.grid(row=0, column=0, pady=(0, 210), padx=(280, 30))

    l2 = tk.Label(show_update_amount, text="Enter Stock Amount", font=('Arial', 20))
    l2.grid(row=0, column=0, pady=(0, 120), padx=(280, 30))

    entry_amount = tk.Entry(show_update_amount)
    entry_amount.grid(row=0, column=0, pady=(0, 30), padx=(280, 30))

    ch=tk.StringVar()

    rb1 = tk.Radiobutton(show_update_amount, text="add to existing amount",value="add",variable=ch)
    rb1.grid(row=0, column=0, pady=(60, 0), padx=(280, 30))

    rb2 = tk.Radiobutton(show_update_amount, text="subtract from existing amount",value="sub",variable=ch)
    rb2.grid(row=0, column=0, pady=(150,0), padx=(280, 30))

    rb3 = tk.Radiobutton(show_update_amount, text="enter new amount", value="new", variable=ch)
    rb3.grid(row=0, column=0, pady=(240, 0), padx=(280, 30))

    button_continue = tk.Button(show_update_amount, text='continue', command=update_amount, bg='lightsteelblue2',
                                font=('Arial', 11, 'bold'))
    button_continue.grid(row=0, column=0, pady=(330, 0), padx=(280, 30))




def update_amount():
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
    if df["portfolio"][id_global] == 0:##create stock portfolio if not created
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

        execute_query(connection, create_table_data)
        execute_query(connection, create_table_total)
        str_portfolio = """UPDATE `stock_db`.`user_names` SET `portfolio` = '1' WHERE (`Name` = '""" + name + """');"""
        execute_query(connection, str_portfolio)  ##updating portfolio created(turn 0 to 1)

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

    if entry_stock_name.get() != '' and entry_amount.get() != '':
        stock_name = str(entry_stock_name.get())  ##getting stock name from input

        try:
            input_amount = float(entry_amount.get())
            tf = 0
        except:
            tf = 1
            messagebox("enter valid input amount!")
        if tf == 0:

            new_amount = 1  ##initilazing data for last if
            if input_amount > 0:
                while i < len(arr_data):
                    if df["stock_name"][i] == stock_name:
                        tmp = i
                    i += 1

                if tmp != -1:
                    q1 = """SELECT stock_amount FROM stock_data_""" + name + """
                                                            WHERE stock_name='""" + str(stock_name) + """';"""
                    res = (read_query(connection, q1))
                    old_amount = float(res[0][0])
                    x = ch.get()

                    if x == "add":
                        new_amount = old_amount + input_amount
                        string_update_amount = """UPDATE stock_data_""" + name + """
                                                                        SET
                                                                        stock_amount = """ + str(new_amount) + """
                                                                        WHERE stock_name='""" + str(stock_name) + """';
                                                                        """
                        execute_query(connection, string_update_amount)
                    elif x == "sub":
                        new_amount = old_amount - input_amount
                        if new_amount < 0:
                            new_amount = 0
                        string_update_amount = """UPDATE stock_data_""" + name + """
                                                                        SET
                                                                        stock_amount = """ + str(new_amount) + """
                                                                        WHERE stock_name='""" + str(stock_name) + """';
                                                                        """
                        execute_query(connection, string_update_amount)

                    elif x == "new":

                        string_update_amount = """UPDATE stock_data_""" + name + """
                                                SET
                                                stock_amount = """ + str(input_amount) + """
                                                WHERE stock_name='""" + str(stock_name) + """';
                                                """
                        execute_query(connection, string_update_amount)

                    messagebox("amount is updated!")
                    entry_stock_name.delete(0, "end")
                    entry_amount.delete(0, "end")



                else:  ##stock not in portfolio
                    session = requests.Session(impersonate="chrome")
                    tickerData = yf.Ticker(stock_name, session=session)
                    x = tickerData.history(period='1d')

                    if not x.empty:  ##stock is in yahoo finance
                        string_new_stock = """INSERT INTO stock_data_""" + str(name) + """ VALUES('""" + str(
                            today) + """' ,'""" + str(stock_name) + """',""" + str(input_amount) + """, 0, 0);"""
                        execute_query(connection, string_new_stock)
                        messagebox("amount is updated!")
                        entry_stock_name.delete(0, "end")
                        entry_amount.delete(0, "end")

                    if x.empty:  ##stock is not in yahoo finance
                        messagebox("stock ticker is not in yahoo finance!")
                        entry_stock_name.delete(0, "end")
                        entry_amount.delete(0, "end")

            elif input_amount < 0:
                messagebox("amount can't be negetive!")
                entry_stock_name.delete(0, "end")
                entry_amount.delete(0, "end")

            if input_amount == 0 or new_amount == 0:
                string_d2 = "SET SQL_SAFE_UPDATES = 0;"
                string_d3 = """DELETE FROM stock_data_""" + str(name) + """
                                                       WHERE stock_name='""" + str(stock_name) + """';"""
                string_d4 = "SET SQL_SAFE_UPDATES = 1;"
                execute_query(connection, string_d2)
                execute_query(connection, string_d3)
                execute_query(connection, string_d4)
                messagebox("amount is updated!")
                entry_stock_name.delete(0, "end")
                entry_amount.delete(0, "end")
    else:
        if entry_amount.get() == '':
            messagebox("enter valid input amount!")
        if entry_stock_name.get() == '':
            messagebox("enter valid stock name!")







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
             messagebox("you are already using the daily function!")
        if df["Portfolio"][id_global] == 0:
            messagebox("you need to create a stock portfolio first!")


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
        messagebox("you need to use the automated portfolio function to see the graph!")




##main function
def main_menu():


    string_name="hello "+name+"!"
    label_hello = tk.Label(root, text=string_name)
    label_hello.config(font=('Arial', 20))
    canvas1.create_window(400, 50, window=label_hello)

    button_ftr_st_clc = tk.Button(root, text='future stock calculator', command=ftr_st_clc, bg='lightsteelblue2',
                                font=('Arial', 11, 'bold'))
    canvas1.create_window(400, 150, window=button_ftr_st_clc)


    button_show_stk_prtlfo = tk.Button(root, text='show saved stock portfolio', command=show_stk_prtlfo, bg='lightsteelblue2',
                                font=('Arial', 11, 'bold'))
    canvas1.create_window(400, 200, window=button_show_stk_prtlfo)


    button_update_amount = tk.Button(root, text='update stock amount/add new stock', command=init_update, bg='lightsteelblue2',
                                font=('Arial', 11, 'bold'))
    canvas1.create_window(400, 250, window=button_update_amount)


    button_auto_func = tk.Button(root, text='start using daily automated portfolio function', command=auto_func, bg='lightsteelblue2',
                                font=('Arial', 11, 'bold'))
    canvas1.create_window(400, 300, window=button_auto_func)


    button_graph = tk.Button(root, text='show graph of total portfolio by date', command=graph, bg='lightsteelblue2',
                                font=('Arial', 11, 'bold'))
    canvas1.create_window(400, 350, window=button_graph)


    button_exit = tk.Button(root, text='exit program', command=exit, bg='lightsteelblue2',
                                font=('Arial', 11, 'bold'))
    canvas1.create_window(400, 400, window=button_exit)

   











def init(): ##logging in user name/creating a new user name
    q1 = """
            SELECT idUser_Names,Name FROM stock_db.user_names;   
            """
    i = 0
    tf = 0
    global name, id_global
    name = str(entry1.get())
    ##deleting the enter name page
    entry1.destroy()
    label1.destroy()
    button_continue.destroy()

    results = read_query(connection, q1)
    arr = []
    for result in results:
        result = result
        arr.append(result)
    columns = ["id", "Name"]
    df = pd.DataFrame(arr, columns=columns)
    i = 0
    while i < len(arr):
        if df["Name"][i]==str(name):
            tf=1
            id_global=i
        i += 1
    if tf==0:
        string_for_sql = """INSERT INTO `stock_db`.`user_names` (`idUser_Names`, `Name`, `automate`,`portfolio`) VALUES ('"""+str(i)+"""', '"""+name+"""', '0','0');"""
        execute_query(connection, string_for_sql)
        id_global=i
    main_menu()


def enter_name(): ##logging in user name/creating a new user name

    global entry1,label1,button_continue


    label1 = tk.Label(root, text='enter user name')
    label1.config(font=('Arial', 20))
    canvas1.create_window(400, 50, window=label1)

    entry1 = tk.Entry(root)
    canvas1.create_window(400, 100, window=entry1)

    button_continue = tk.Button(root, text='continue', command=init, bg='lightsteelblue2',
                                font=('Arial', 11, 'bold'))
    canvas1.create_window(400, 260, window=button_continue)




today=datetime.date.today()
root = tk.Tk()
connection = create_server_connection("127.0.0.1", "tony", "tonton12", "stock_db")
canvas1 = tk.Canvas(root, width=800, height=600)
canvas1.pack()
enter_name()
root.mainloop()




















##option for posting table or printing inside of tkinker
#global t1
#t1 = tk.Text(root)
# t1.pack()   ##this
#canvas1.create_window(400, 450, window=t1)  #or this
#sys.stdout = PrintToT1()
#print(df)






























