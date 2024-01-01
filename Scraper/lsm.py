from datetime import datetime
import re
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import chromedriver_autoinstaller

def LSMScraper(query, starttime, endtime):
    #Instalē chromedriver, ja tas vēl nav izdarīts
    chromedriver_autoinstaller.install()

    articles = {}
    pagenumber = 1
    errorcount = 0
    #iestatījumi chromedriver
    options = Options()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--allow-running-insecure-content')
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    options.add_argument('--incognito')
    options.add_argument('--headless')
    browser = webdriver.Chrome(options=options)
    while True:
        URL = f"https://www.lsm.lv/meklet/?search_q={query}#gsc.tab=0&gsc.q={query}&gsc.sort=date&gsc.page={pagenumber}&gsc.ref=more%3Alsm.lv"
        browser.get(URL)
        try:
            WebDriverWait(browser, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, "gsc-resultsbox-visible")))
        except:
            browser.close()
            return articles
        soup = bs(browser.page_source, "html.parser")
        #Atrod lapas saturu
        main = soup.find(class_="gsc-resultsbox-visible")
        #Atrod rakstu elementus
        elements = main.find_all("div", class_="gs-webResult gs-result")

        #Ja lapā nav raksti, viss tiek atgriezts
        if elements == []:
            browser.close()
            return articles

        for element in elements:
            elementText = element.find("a", class_="gs-title")
            elementDate = re.search("[0-9]{2}\.[0-9]{2}\.[0-9]{4}", elementText["data-ctorig"])
            #LSM pievieno arī tēmas un sākuma lapu meklēšanā, tādējādi šis arī izfiltrē tās lapas
            if elementDate != None:
                dateObj = datetime.strptime(elementDate.group(), "%d.%m.%Y").date()
                if dateObj >= starttime:
                    errorcount = 0
                    if dateObj <= endtime:
                        articles[elementText["href"]] = elementText.text.strip()
                else:
                    #Pārbauda vai ir 3 raksti pēc kārtas pirms sākuma datuma (LSM mēdz iebāzt vecus rakstus starp jauniem)
                    errorcount = errorcount + 1
                    if errorcount >= 3:
                        browser.close()
                        return articles
        pagenumber = pagenumber + 1