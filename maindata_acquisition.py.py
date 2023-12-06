# data_acquisition.py

import requests
from bs4 import BeautifulSoup
import pandas as pd

def acquire_data():
    api_url = "https://api.baseballstats.com"
    response = requests.get(api_url)
    api_data = response.json()

    web_url = "https://baseballstats.com"
    html_content = requests.get(web_url).content
    soup = BeautifulSoup(html_content, 'html.parser')

    web_data = pd.read_html(html_content)
    processed_data = pd.concat(web_data)

    return processed_data
