
# Automatic Email Alerts API

 Automatic price alerts that send you an email automatically.
 A price alert application that triggers an email when the user’s target price is achieved.
The application should send an email to the user when the price of BTC reaches 33,000$.

A rest API endpoint for the user’s to create an alert.

I used HTML and CSS to buld these webpages and will render them using flask render_template module.

I have used SQL lite to store data in our database. We are storing Emails and Target value of every user
and i used yahoo finance to get the real time price of BTC(Bit coin) and with the help of smtplib and email message library 
my API is sending Alert Emails to users if BTC price match with target price.


When the price of the coin reaches the price specified by the users, send an email to all
the users that set the alert at that price. (send mail using Gmail SMTP)




## API Reference
Input from user which will be stored in Data Base using SQL lite

### Data Base



| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `Email and Target` | `string and Number` | **Required**. |

#### Result

Send you an email automatically



  
## Deployment
Main Alert API.
To deploy this project run

```bash
# email and passwors from which we are sending mails
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

```

  