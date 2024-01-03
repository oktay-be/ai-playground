# TOOLING
import asyncio
from typing import Tuple
import requests
from bs4 import BeautifulSoup   

class Scraper:

    async def scrap_async(self, url):
        response = requests.get(url, verify=False)
        if response.status_code == 200 and 'text/html' in response.headers['Content-Type']:
            soup = BeautifulSoup(response.text, 'html.parser')
            text = soup.get_text()
            if 'You need to enable JavaScript to run this app.' in text:
                print(f"Unable to parse page {url} due to JavaScript being required")
                return ''
            return text
        else:
            return ''