from datetime import datetime
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import chromedriver_autoinstaller

#Funkcija mājaslapas cnn.com skrāpēšanai
def CNNScraper(query, starttime, endtime):
    #Instalē chromedriver, ja tas vēl nav izdarīts
    chromedriver_autoinstaller.install()

    articles = {}
    pagenumber = 1
    articlecounter = 0
    #iestatījumi chromedriver
    options = Options()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--allow-running-insecure-content')
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    options.add_argument('--incognito')
    options.add_argument('--headless')
    browser = webdriver.Chrome(options=options)
    while True:
        #Iegūst lapu
        URL = f"https://edition.cnn.com/search?q={query}&from={articlecounter}&size=10&page={pagenumber}&sort=newest&types=all&section="
        browser.get(URL)
        try:
            WebDriverWait(browser, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, "container__field-links")))
        except:
            browser.close()
            return articles
        soup = bs(browser.page_source, "html.parser")
        #Atrod lapas saturu
        main = soup.find(class_="container__field-links")
        #Atrod rakstu elementus
        elements = main.find_all("div", class_="container__item")

        #Ja lapā nav raksti, viss tiek atgriezts
        if elements == []:
            browser.close()
            return articles

        #Pievieno elementus rezultātu vārdnīcai
        for element in elements:
            elementText = element.find("span", class_="container__headline-text")
            elementHref = element["data-open-link"]
            elementDate = element.find("div", class_="container__date").text.strip()
            date = datetime.strptime(elementDate, '%b %d, %Y').date()
            if date >= starttime:
                if date <= endtime:
                    articles[elementHref] = {'Title': elementText.text.strip(),
                                                     'Date': date}
            else: 
                browser.close()
                return articles
            
        pagenumber = pagenumber + 1
        #CNN meklēšanas funkcijas URL ir skaitītājs, no kuras iegūst no kura rezultāta sākt rādīt kopā ar lapas numuru
        articlecounter = articlecounter + 10