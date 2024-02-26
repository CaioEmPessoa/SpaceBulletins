from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

import os
import json
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

with open("./bulletins/bulletinsInfo.json", "r") as read_json:
    data = json.load(read_json)

options = Options()

# don't open the broser
options.add_argument("--headless")

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
    time = time.strftime("%d/%m/%y")

    comments_count = bulletin.findAll("td")[2].get_text().replace("\n", "")[0]

    BULLETIN_URL = bulletin.find("a", href=True)["href"]
    BULLETIN_LINK = SPACEHEY_URL + BULLETIN_URL
    BULLETIN_ID = BULLETIN_URL[BULLETIN_URL.find("id=")+3:]

    data[BULLETIN_ID] = {
        "id":BULLETIN_ID,
        "title":title,
        "time":time,
        "comment_count":comments_count
    }

    driver.get(BULLETIN_LINK)

    bulletin_soup = BeautifulSoup(driver.page_source, 'html.parser')
    bulletin_soup.find("nav").decompose()
    bulletin_soup.find("footer").decompose()

    bulletin_soup.find("p", {"class":"publish-date"}).clear()
    
    links_p = bulletin_soup.find("p", {"class":"links"})
    links_a = links_p.findAll("a")
    links_a[0]["href"] = "../index.html"
    links_a[1].decompose()
    links_a[2].decompose()

    if int(comments_count)>0:
        bulletin_soup.find("p", {"class":"report"}).decompose()

    for meta in bulletin_soup.findAll("meta"):
        meta.decompose() 
    
    for link in bulletin_soup.findAll("link"):
        link.decompose()

    with open("./bulletins/"+BULLETIN_ID+".html", "w", encoding="utf-8") as file:
        file.write(f"<link rel=\"stylesheet\" href=../styles/main.css>")
        file.write(f"<link rel=\"stylesheet\" href=../styles/custom.css>")
        file.write(str(bulletin_soup))

    driver.get(BULLETINS_SITE)

with open("./bulletins/bulletinsInfo.json", "w") as write_json:
    json.dump(data, write_json, indent=4)

## I'm gonna use bs to edit the index page and add the stored bulletins
## i know this isn't supposed to be used
## I wanted to use js but it can't read local json so i'm doing this

saved_bulletins = os.listdir("./bulletins")
saved_bulletins.remove("bulletinsInfo.json")

with open("./index.html", "r", encoding="utf-8") as read_index:
    index_soup = BeautifulSoup(read_index.read(), "html.parser")
    table = index_soup.find("tbody", {"id":"bulletins-table"})
    
    #clear all previous bullletins
    for t in table.findAll("tr"):
        t.decompose()

    for bulletin in saved_bulletins:
        tr = index_soup.new_tag("tr")
        table.insert(1, tr)
        
        for i in range(4):
            th = index_soup.new_tag("th")
            tr.insert(0, th)

        th_list = tr.findAll("th")
        
        with open("./bulletins/bulletinsInfo.json", "r") as read_json:
            data = json.load(read_json)[bulletin[:-5]]
            
            #time
            th_list[0].insert(0, data["time"])

            #subject
            subject = index_soup.new_tag("a", href=f"./bulletins/{data['id']}.html")
            th_list[1].insert(0, subject)
            th_list[1].find("a").insert(0, data["title"])

            #comments
            th_list[2].insert(0, data["comment_count"]+" comments")

            #id
            th_list[3].insert(0, data["id"])

with open("./index.html", "w", encoding="utf-8") as write_index:
    write_index.write(str(index_soup))