from urllib.request import urlopen
from urllib.error import HTTPError
from urllib.error import URLError
from bs4 import BeautifulSoup
import smtplib

try:
    url = urlopen(input('Digite a URL do produto: \n'))
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
print(productTitle)
    
def sendMail():
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    
    fromEmail = 'email.marcos.oliveira@gmail.com'
    toEmail = 'email.marcos.oliveira@gmail.com'
    myPass = 'ctnedwsuwrdnpaoj'
    
    server.login(fromEmail, myPass)
    
    subject = 'Hello! The price of the product you are waiting for has dropped'
    body = f'Your product named {productTitle} has a discount. Check it on:'
    msg = f"Subject: {subject}\n\n{body}"
    server.sendmail(
        fromEmail,
        toEmail,
        msg
    )
    print('Hello! An descount e-mail has been sent.')
    server.quit()
   
def getPrice():
    price = soup.find(id='priceblock_ourprice')
    price = price.get_text()
    price = price.replace(",", ".")
    converted_price = float(price[2:])
    print(converted_price)

    # Checking Price
    saving_price = 1700
    if converted_price < saving_price:
        sendMail()
                      
getPrice()
