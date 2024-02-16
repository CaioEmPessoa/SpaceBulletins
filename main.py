import os
from dotenv import load_dotenv
from bs4 import BeautifulSoup
import requests

load_dotenv()

EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")
ID = os.getenv("ID")

html_text = requests.get("https://spacehey.com/userbulletins?id="+ID).text
soup = BeautifulSoup(html_text, 'lxml')