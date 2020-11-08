from urllib.request import urlopen
from urllib.error import HTTPError
from urllib.error import URLError
from bs4 import BeautifulSoup
from googletrans import Translator

try:
    url = urlopen(input('Enter the article URL: \n'))
    # Valid to any article at https://www.forbes.com/sites/startswithabang/ from July 2020
except HTTPError as e:
    print(e)
except URLError:
    print('Page not found or incorrect domain.')
else:
    soup = BeautifulSoup(url.read(), 'html.parser')

# Getting title's article
title = soup.title.get_text()  

# Checking if title has ':' or '?' to use as file name 
for charMistake in title:
    if charMistake == ':' or charMistake == '?':
        title = title.replace(':',' -')
        title = title.replace('?',' (Question Mark)')
                
def getOriginalText():
    paragraphs = soup.select('div > p, div > p ~ blockquote, div > p ~ ul, div > p ~ ol') # Where ',' means 'or'
    with open('{} - Original.txt'.format(title), 'w', encoding="utf8") as arq:
        arq.write('Extracting the article "{}" \n \n'.format(title))
        arq.write('*** Initializing paragraphs *** \n \n')
        for paragraph in paragraphs:
            paragraph = paragraph.get_text()
            arq.write(str(paragraph) + "\n \n")
                
def getOriginalCaptions():                
    captions = soup.select('p.color-body')
    with open('{} - Captions.txt'.format(title), 'w', encoding="utf8") as arq:
        arq.write('*** Initializing captions *** \n \n')
        for caption in captions:
            caption = caption.get_text()
            arq.write(caption + '\n \n')
                
def getTranslation():
    getOriginalText() 
    getOriginalCaptions()
    translator = Translator()
    
    # Reading source files 
    with open(title + ' - Original.txt', 'r', encoding="utf8") as textArq:
        textToTranslate = textArq.readlines()
    article = translator.translate(textToTranslate, dest='pt')
    
    with open(title + ' - Captions.txt', 'r', encoding="utf8") as captionArq:
        captionsToTranslate = captionArq.readlines()
    captions = translator.translate(captionsToTranslate, dest='pt') 
    
    # Creating new translated files
    with open('{} - Legendas.txt'.format(title), 'w', encoding="utf8") as translatedCaption:
        for caption in captions:
            translatedCaption.write(caption.text + '\n')
        
    with open('{} - Traduzido.txt'.format(title), 'w', encoding="utf8") as translatedText:
        for text in article:
            translatedText.write(text.text + '\n')
        

getTranslation() # Run program