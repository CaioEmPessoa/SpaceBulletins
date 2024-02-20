from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

import os
import requests
from datetime import datetime
from dotenv import load_dotenv
from bs4 import BeautifulSoup

load_dotenv()

EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")
USER_ID = os.getenv("USER_ID")
SPACEHEY_URL = "https://spacehey.com/"
BULLETINS_SITE = SPACEHEY_URL + "userbulletins?id=" + USER_ID

options = Options()

# don't open the broser
#options.add_argument("--headless")

# don't kills chrome when code ends
#options.add_experimental_option("detach", True) 


# Donwload driver (If needed) and starts it
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

driver.get(BULLETINS_SITE)
driver.implicitly_wait(3)

email_field = driver.find_element(By.ID, "email")
email_field.send_keys(EMAIL)

pswrd_field = driver.find_element(By.ID, "password")
pswrd_field.send_keys(PASSWORD)

# it has to be two times
pswrd_field.submit()
pswrd_field.submit()

driver.get(BULLETINS_SITE)

### now its in the logged in and on the right website ###

bulletins_soup = BeautifulSoup(driver.page_source, 'html.parser')
bulletin_table = bulletins_soup.find("table", {"class":"bulletin-table"})
bulletins = bulletin_table.findAll("tr")
for bulletin in bulletins[1:]:
    title = bulletin.find("td", {"class":"subject"})
    title = title.get_text().replace("\n", "")

    time = int(bulletin.find("time")["data-timestamp"])
    time = datetime.fromtimestamp(time)
    time = time.strftime("%d.%m.%y")

    comments_count = bulletin.findAll("td")[2].get_text().replace("\n", "")[0]

    BULLETIN_URL = bulletin.find("a", href=True)["href"]
    BULLETIN_LINK = SPACEHEY_URL + BULLETIN_URL
    BULLETIN_ID = BULLETIN_URL[BULLETIN_URL.find("id=")+3:]
    print(BULLETIN_ID) 

    driver.get(BULLETIN_LINK)

    bulletin_soup = BeautifulSoup(driver.page_source, 'html.parser')
    bulletin_soup.find("nav").decompose()
    bulletin_soup.find("footer").decompose()

    ''' 
    TODO:
    need to remove:
    report bulletin
    view profile (maybe)

    need to create:
    customstyle, main be centered
    edit "view bulletins" a tag to point to main page here, index
    '''
    
    # TODO: check if exists bulletin with same id AND content, without counting comments
    with open("./bulletins/"+BULLETIN_ID+".html", "w") as outfile:
        outfile.write(str(bulletin_soup))

    driver.get(BULLETINS_SITE)
