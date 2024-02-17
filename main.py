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
WEBSITE = "https://spacehey.com/userbulletins?id="+USER_ID

options = Options()

# don't open the broser
options.add_argument("--headless")

# don't kills chrome when code ends
#options.add_experimental_option("detach", True) 


# Donwload driver (If needed) and starts it
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

driver.get(WEBSITE)
driver.implicitly_wait(2)

email_field = driver.find_element(By.ID, "email")
email_field.send_keys(EMAIL)

pswrd_field = driver.find_element(By.ID, "password")
pswrd_field.send_keys(PASSWORD)

# it has to be two times
pswrd_field.submit()
pswrd_field.submit()

driver.get(WEBSITE)

### now its in the logged in and on the right website ###

bulletin_info = {}
''' How it'll look like
"Title": {
    "bulletin-text":"text",
    "comments-count":1,
    "comments":{
        "user-one":"comment",
        "user-two":"comment"
    },
    "bulletin-date":"dd/mm/yy"
}
'''

soup = BeautifulSoup(driver.page_source, 'html.parser')
bulletin_table = soup.find("table", {"class":"bulletin-table"})
bulletins = bulletin_table.findAll("tr")
for bulletin in bulletins[1:]:
    title = bulletin.find("td", {"class":"subject"})
    title = title.get_text().replace("\n", "")

    time = int(bulletin.find("time")["data-timestamp"])
    time = str(datetime.fromtimestamp(time))

    comments_count = bulletin.findAll("td")[2].get_text().replace("\n", "")

    bulletin_info[title] = {
        "comments-coun":comments_count,
        "bulletin-date":time
        }
    bulletin_link = bulletin.find("a", href=True)["href"]

print(bulletin_info)