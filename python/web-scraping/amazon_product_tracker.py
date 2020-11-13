from urllib.request import urlopen
from urllib.error import HTTPError
from urllib.error import URLError
from bs4 import BeautifulSoup
import smtplib

try:
    url = urlopen(input('Enter the product URL: \n'))
except HTTPError as e:
    print(e)
except URLError:
    print('Page not found or domain incorrect.')
else:
    soup = BeautifulSoup(url.read(), 'html.parser')

# Getting product name

productTitle = soup.find(id='productTitle')
productTitle = productTitle.get_text()
productTitle = productTitle.strip()
    
def sendMail():
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    
    fromEmail = 'From To E-mail Here' # example@gmail.com
    toEmail = 'To E-mail Here' # anotherexample@gmail.com
    myPass = 'Enter Your E-mail Password Here' # https://passwords.google.com
    
    server.login(fromEmail, myPass)
    
    subject = 'Hello! The price of the product you are waiting for has dropped'
    body = f'Your product named {productTitle} has a discount. Check it on:'
    msg = f'Subject: {subject}\n\n{body}'
    server.sendmail(
        fromEmail,
        toEmail,
        msg
    )
    print('An discount has been found. Check your e-mail for additional details.')
    server.quit()
   
def getPrice():
    price = soup.find(id='priceblock_ourprice')
    price = price.get_text()
    price = price.replace(",", ".")  
    converted_price = float(price[2:]) # Removing the 'R$' symbol and transforming the string to float
    print(converted_price)

    # Checking Price
    saving_price = 1000
    if converted_price < saving_price:
        sendMail()
                      
getPrice()
