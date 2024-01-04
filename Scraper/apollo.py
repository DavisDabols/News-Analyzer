from datetime import datetime
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import chromedriver_autoinstaller

def ApolloScraper(query, starttime, endtime):
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
        URL = f"https://www.apollo.lv/search?start={starttime.year}-{starttime.month}-{starttime.day}T00%3A00%3A00%2B02%3A00&end={endtime.year}-{endtime.month}-{endtime.day}T23%3A59%3A59%2B02%3A00&query={query}&sections=4132%2C4435%2C4506%2C4428%2C4448%2C4425%2C4440%2C4433%2C4213&fields=body%2Cauthors%2Cheadline&page={pagenumber}"
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
                    articles[elementHref["href"]] = {'Title': elementText.text.strip(),
                                                     'Date': date}
            else: 
                browser.close()
                return articles
        pagenumber = pagenumber + 1