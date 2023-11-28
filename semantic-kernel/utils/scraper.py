# TOOLING
import asyncio
from typing import Tuple
import requests
from bs4 import BeautifulSoup   

class Scraper:
    def __init__(self, url):
        self.url = url
        self.scrap_async(self.url)

    async def scrap_async(self):
        response = requests.get(self.url)
        if response.status_code == 200 and 'text/html' in response.headers['Content-Type']:
            soup = BeautifulSoup(response.text, 'html.parser')
            text = soup.get_text()
            if 'You need to enable JavaScript to run this app.' in text:
                print(f"Unable to parse page {self.url} due to JavaScript being required")
                return ''
            return text
        else:
            return ''