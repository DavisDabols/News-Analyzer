from datetime import datetime
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import chromedriver_autoinstaller

def APnewsScraper(query, starttime, endtime):
    #Instalē chromedriver, ja tas vēl nav izdarīts
    chromedriver_autoinstaller.install()

    articles = {}
    pagenumber = 1
    #iestatījumi chromedriver
    options = Options()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--allow-running-insecure-content')
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    options.add_argument('--incognito')
#    options.add_argument('--headless')
    browser = webdriver.Chrome(options=options)
    while True:
        URL = f"https://apnews.com/search?q={query}&s=1&p={pagenumber}"
        browser.get(URL)
        try:
            WebDriverWait(browser, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, "PageList-items-item")))
        except:
            browser.close()
            return articles
        soup = bs(browser.page_source, "html.parser")
        #Atrod lapas saturu
        main = soup.find(class_="SearchResultsModule-results")
        #Atrod rakstu elementus
        elements = []
        for e in main.find_all("div", class_="PageList-items-item"):
            if e.find(class_='SovrnAd Advertisement sovrn-hub-feed'):
                continue
            else:
                elements.append(e)

        #Ja lapā nav raksti, viss tiek atgriezts
        if elements == []:
            browser.close()
            return articles

        for element in elements:
            elementText = element.find("span", class_="PagePromoContentIcons-text")
            elementHref = element.find("a", class_="Link")
            elementDate = element.find("bsp-timestamp")
            timestamp = int(elementDate["data-timestamp"]) / 1000
            date = datetime.fromtimestamp(timestamp).date()
            if date >= starttime:
                if date <= endtime:
                    articles[elementHref["href"]] = {'Title': elementText.text.strip(),
                                                     'Date': date}
            else: 
                browser.close()
                return articles
        pagenumber = pagenumber + 1