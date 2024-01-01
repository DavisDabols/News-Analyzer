from datetime import datetime
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import chromedriver_autoinstaller

def TvnetScraper(query, starttime, endtime):
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
        URL = f"https://www.tvnet.lv/search?sections=4133%2C4221%2C6177%2C4232%2C5912%2C4228%2C4238%2C4281%2C4214%2C4235%2C5178&query={query}&start={starttime.year}-{starttime.month}-{starttime.day}T01%3A00%3A00%2B03%3A00&end={endtime.year}-{endtime.month}-{endtime.day}T23%3A59%3A59%2B02%3A00&fields=body%2Cauthors%2Cheadline&page={pagenumber}"
        browser.get(URL)
        try:
            WebDriverWait(browser, 10).until(EC.visibility_of_element_located((By.TAG_NAME, "article")))
        except:
            browser.close()
            return articles
        soup = bs(browser.page_source, "html.parser")
        #Atrod lapas saturu
        main = soup.find(class_="structured-content")
        #Atrod rakstu elementus
        elements = []
        for e in main.find_all("article", class_="list-article"):
            if e.find(class_='list-article--commercial'):
                continue
            else:
                elements.append(e)

        #Ja lapā nav raksti, viss tiek atgriezts
        if elements == []:
            browser.close()
            return articles

        for element in elements:
            elementText = element.find("h2", class_="list-article__headline")
            elementHref = element.find("a", class_="list-article__url")
            elementDate = element.find("meta", itemprop="datePublished")
            date = datetime.strptime(elementDate["content"].split('T', 1)[0], '%Y-%m-%d').date()
            if date >= starttime:
                if date <= endtime:
                    articles[elementHref["href"]] = elementText.text.strip()
            else: 
                browser.close()
                return articles
        pagenumber = pagenumber + 1