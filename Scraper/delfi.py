from datetime import datetime
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import chromedriver_autoinstaller

def DelfiScraper(query, starttime, endtime):
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
    options.add_argument('--headless')
    browser = webdriver.Chrome(options=options)
    while True:
        #Delfi mājaslapas kļūmes dēļ nevar iegūt laika periodus no mājaslapas (vienmēr automātiski atjaunojas uz 1.1.24)
        URL = f"https://www.delfi.lv/archive?search={query}&from=1/1/2024,+12:00:00+AM&to={endtime.day}/{endtime.month}/{endtime.year},+11:59:59+PM&page={pagenumber}&order=PUBLISH_AT&domain=www.delfi.lv"
        browser.get(URL)
        try:
            WebDriverWait(browser, 10).until(EC.visibility_of_element_located((By.TAG_NAME, "article")))
        except:
            browser.close()
            return articles
        soup = bs(browser.page_source, "html.parser")
        #Atrod lapas saturu
        main = soup.find(id="portal-main-content")
        #Atrod rakstu elementus
        elements = main.find_all("article", class_="d-flex align-items-center text-size-4 headline headline--text-aside headline--archive")

        #Ja lapā nav raksti, viss tiek atgriezts
        if elements == []:
            browser.close()
            return articles

        for element in elements:
            elementText = element.find("a", class_="")
            elementDate = element.find("time", class_="text-size-7")
            date = datetime.strptime(elementDate["datetime"].split('T', 1)[0], '%Y-%m-%d').date()
            if date >= starttime:
                if date <= endtime:
                    articles[f"https://www.delfi.lv{elementText['href']}"] = {'Title': elementText.text.strip(),
                                                                              'Date': date}
            else: 
                browser.close()
                return articles
        pagenumber = pagenumber + 1