from flask.json import jsonify
from flask import Flask
from flask import render_template,request
import sqlite3
import os

import os
import smtplib
import imghdr
from email.message import EmailMessage

import yfinance as yf
import datetime as dt
import pandas as pd
from pandas_datareader import data as pdr

currentdirectory=os.path.dirname(os.path.abspath(__file__))


app=Flask(__name__)

# @app.route('/')
# def hello_world():
#     return 'Hellow ,World'

@app.route('/')
def main():
    return render_template('index.html')

@app.route('/',methods=['POST'])
def storeRecords():
    email =request.form["email"]
    Target=request.form["target"]
    connection=sqlite3.connect(currentdirectory + "\records.db")
    cursor=connection.cursor()
    query1="INSERT INTO records VALUES ('{email}',{target})".format(email=email,target=Target)
    cursor.execute(query1)
    connection.commit()
def AlertUser():

    # email and passwors of an gmail account from which we are sending mails
    # to alert users
    EMAIL_ADDRESS = "XYZ@gmail.com"
    EMAIL_PASSWORD = "XYZ123"

    msg = EmailMessage()

    yf.pdr_override()
    start = dt.datetime(2021, 9, 9)
    now = dt.datetime.now()

    stock = "BTC-USD"
    TargetPrice = 33000

    msg["Subject"] = "Alert on" + stock
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = "User1@gmail.com"

    alerted = False

    while 1:
        df = pdr.get_data_yahoo(stock, start, now)
        currentClose = df["Adj Close"][-1]
        print(currentClose)

        condition = currentClose > TargetPrice

        if (condition and alerted == False):
            alerted = True
            message = stock + "Has activated the alert price of " + str(TargetPrice) + \
                      "\nCurrent Price: " + str(currentClose)

            msg.set_content(message)

            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
                smtp.send_message(msg)

                print("Completed")
        else:
            print(" no new Alerts")


@app.route('/showrecords',methods=['GET'])
def showrecords():
    try:
        if request.method=='GET':
            email=request.args.get("email")
            connection = sqlite3.connect(currentdirectory + "\records.db")
            cursor = connection.cursor()
            query1="SELECT Target from records WHERE email={email}".format(email=email)
            result=cursor.execute(query1)
            result=result.fetchall()[0][0]
            return render_template("showrecords.html",Target=result)
    except:
        return render_template("showrecords.html",Target="")





if __name__=="__main__":
    app.run(debug=True)