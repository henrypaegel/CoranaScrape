# scraping Inzidenz from hamburg.de/corona-zahlen
import requests
import csv
from bs4 import BeautifulSoup
import re
import time
from datetime import datetime

URL = 'https://hamburg.de/corona-zahlen'
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}


def scrapeInzidenz(soup):
    # extract textbox from site
    results = soup.find(id='pushedContainer')
    textbox = results.find_all('p', class_='teaser-text c_chartheadline')
    m = re.findall('>[0-9]*,*[0-9]<|\(..\...\.....\)', str(textbox)) # grab from textbox
    # edit to clean numbers
    inzidenz = m[0][1:len(m[0])-1]
    date = m[1][1:len(m[1])-1]
    return inzidenz, date

def downloadSite(URL):
    page = requests.get(URL, headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser')
    return soup

def waitMidnight():  # sleep until next day
    now = datetime.now()
    secondsFromMidnight = (
        now - now.replace(hour=0, minute=0, second=0, microsecond=0)).total_seconds()
    secondsToMidnight = 86400 - secondsFromMidnight
    time.sleep(secondsToMidnight)

while True:
    # download and parse the homepage
    results = downloadSite(URL).find(id='pushedContainer')
    textbox = results.find_all('p', class_='teaser-text c_chartheadline')
    today = datetime.today()
    currentDate = today.strftime("%d.%m.%Y")
    if str(textbox).find(str(currentDate)) == -1:
        # wait 60 seconds until next request
        time.sleep(60)
        continue

    else:
        data = scrapeInzidenz(downloadSite(URL))
        with open('output.csv', mode='w') as pasteFile:
            pasteWriter = csv.writer(pasteFile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)   
            pasteWriter.writerow(data)         
        text = "Inzidenz: " + data[0] + " --- Abgerufen: " + str(datetime.now())
        print(datetime.now(), "- scraped", data)
        print(datetime.now(), "- waiting until tomorrow")
        waitMidnight()
        print(datetime.now(), "- checking for new data")
        continue
