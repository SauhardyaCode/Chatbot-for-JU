from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import json
import os

# Setup Chrome options for headless run (no browser window)
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
driver = webdriver.Chrome(options=chrome_options)

def read_json(fileJSON):
    if os.path.exists(fileJSON):
        with open(fileJSON,"r",encoding="utf-8") as f:
            try:return json.load(f)
            except:pass
    return []