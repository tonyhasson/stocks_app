
import matplotlib.pyplot as plt
import yfinance as yf
import shelve
from selenium import webdriver
from bs4 import BeautifulSoup
import requests as rq
import pandas as pd



##classes:

class stock(object):
    def __init__(self, name, price,amount):
        self.name = name
        self.price = price
        self.amount=amount
        self.percent=0















##functions:


def st_port_chk():
    i=0
    sum_price=0
    a=[]
    amount_of_stocks=int(input("enter amount of stocks you want to enter: "))

    while i<amount_of_stocks:
       stock_name=input("enter a stock exact ticker(if the stock is international,if not enter 0): ")
       if stock_name!='0':
            tickerData = yf.Ticker(stock_name)
            x = tickerData.history(period='1s')
            stock_price = x['Close'][1]
       else:
           stock_name = input("enter israeli stock name: ")
           stock_price = float(input("enter a stock price: "))

       stock_amount = float(input("enter amount of stocks owned: "))
       d = shelve.open('stock_data.txt')  # here you will save the score variable
       d[name+'_stock_name_'+str(i)] = stock_name  # thats all, now it is saved on disk.
       d[name+'_stock_amount_'+str(i)] = stock_amount
       d[name+'_stock_price_'+str(i)] = stock_price
       d.close()
       sum_price+=stock_price*stock_amount
       new_stock=stock(stock_name,stock_price,stock_amount)
       a.append(new_stock)
       i+=1
       print("new stock ")
    print(str(sum_price))
    d = shelve.open('stock_data.txt')
    d[name+'_total_price'] = sum_price
    d[name+'_amount_of_stocks']=amount_of_stocks
    d.close()
    i=0
    while i<amount_of_stocks:
        a[i].percent=float((a[i].price*a[i].amount*100)/sum_price)
        d = shelve.open('stock_data.txt')
        d[name+'_stock_percent_'+str(i)] =a[i].percent
        d.close()

        print("name:"+str(a[i].name)+"   price: " +str(a[i].price)+"   amount: " +str(a[i].amount)+"  percent: "+ str(a[i].percent) +"%")
        i+=1

def ftr_st_clc():
    amount_rn=float(input("            enter current balance: "))

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



def sav_stk_prtlfo():
    percents = []
    names = []
    d = shelve.open('stock_data.txt')  
    i=0
    total_price=0
    amount_of_stocks=d[name+'_amount_of_stocks']
    while i<amount_of_stocks:
        stock_name=d[name+'_stock_name_'+str(i)]
        stock_amount=d[name+'_stock_amount_'+str(i)]
        if stock_amount>0:
            tickerData = yf.Ticker(stock_name)
            x = tickerData.history(period='1s')
            if not x.empty:
                 stock_price = x['Close'][1]
            if x.empty:
                print("do you want to use the same price as before or a new price for "+stock_name+"?")
                option=int(input("same price: 1 new price: 2"))
                if option==1:
                     stock_price=d[name+'_stock_price_'+str(i)]
                if option==2:
                     stock_price=float(input("enter the current price of "+stock_name+" stock: "))
            d[name+'_stock_price_'+str(i)]=stock_price
            total_price+=stock_price*stock_amount

        i+=1
    i=0
    print("total price: " + str(total_price))
    d[name+'_total_price']=total_price
    while i<amount_of_stocks:
        if d[name + '_stock_amount_' + str(i)]>0:
            stock_percent=(d[name+'_stock_price_'+str(i)]*d[name+'_stock_amount_'+str(i)]*100)/total_price
            percents.append(stock_percent)
            names.append(d[name+'_stock_name_'+str(i)])
            d[name+'_stock_percent_'+str(i)]=stock_percent
            print("name :" + str(d[name+'_stock_name_'+str(i)]) + "  amount: " + str(d[name+'_stock_amount_'+str(i)]) + "  price: " + str(
            d[name+'_stock_price_'+str(i)]) + " percent: " + str(d[name+'_stock_percent_'+str(i)]))
        i += 1

    ##showing pie chart
    fig1, ax1 = plt.subplots()
    text="total dollars invested: "+str(total_price)+""
    plt.title(text, fontdict=None, loc='center', pad=None)
    ax1.pie(percents, labels=names, autopct='%1.1f%%',
             shadow=True, startangle=90)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    plt.show()

    d.close()


def update_amount():
    stock_name=""
    tmp=-1
    while stock_name!= "stop":
        stock_name=input("enter existing stock in your portfolio or a new stock you wish to add or stop to quit the function: ")
        if stock_name != "stop":
            i=0
            tmp = -1
            d = shelve.open('stock_data.txt')
            amount_of_stocks=d[name+'_amount_of_stocks']
            while i<d[name+'_amount_of_stocks']:
                if d[name+'_stock_name_'+str(i)]==stock_name:
                    tmp=i
                i+=1

            if tmp!=-1:
                d[name + '_stock_amount_' + str(tmp)]=float(input("enter new amount: "))
                print("amount is updated!")

            else:
                tickerData = yf.Ticker(stock_name)
                x = tickerData.history(period='1s')
                if not x.empty:
                    d[name + '_amount_of_stocks']+=1
                    d[name + '_stock_name_' + str(amount_of_stocks)]=stock_name
                    d[name + '_stock_amount_' + str(amount_of_stocks)] = float(input("enter amount of stock: "))
                    print("amount is updated!")

                if x.empty:
                    stock_name = input("enter israeli stock name: ")
                    stock_price = float(input("enter a stock price: "))
                    d[name + '_amount_of_stocks'] += 1
                    d[name + '_stock_name_' + str(amount_of_stocks)]=stock_name
                    d[name+'_stock_price_'+str(amount_of_stocks)]=stock_price
                    d[name + '_stock_amount_' + str(amount_of_stocks)] = float(input("enter amount of stock: "))
                    print("amount is updated!")

            d.close()

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
        print("to quit program:-1")
        option=int(input(""))
        if option==1:
            st_port_chk()
        if option==2:
            ftr_st_clc()
        if option==3:
            sav_stk_prtlfo()
        if option==4:
            update_amount()
    print("good bye " + name + "!")

def init(): ##logging in user name/creating a new user name
    i=0
    tf=0
    global name
    name=input("enter your name: ")
    d = shelve.open('stock_data.txt')
    amount_name=d['amount_name']
    while i<amount_name:
         if d['name_'+str(i)]==name:
               tf=1
         i+=1
    if tf==0:
        d['name_'+str(amount_name)]=name
        amount_name+=1
        d['amount_name']=amount_name

    d.close()
init()
main_menu()



##def take_price_from_url():##need to check if how to use url without opening the website,maybe use requests.
    ##can get a price out of tase website
  ##  driver = webdriver.Chrome(r"C:\Users\tonyh\OneDrive\Desktop\New folder\chromedriver.exe")
    ##driver.get("https://www.tase.co.il/en/market_data/security/01148964/historical_data?pType=0&oId=01148964")
    ##content = driver.page_source
    ##soup = BeautifulSoup(content,features="lxml")
    ##price=soup.find("table", {"class": "table table_page_main_table"}).find("tbody").find("tr")
    ##print(price.findAll("td")[1].text)












