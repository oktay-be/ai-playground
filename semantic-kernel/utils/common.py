from langchain.text_splitter import RecursiveCharacterTextSplitter
from semantic_kernel import ContextVariables, Kernel
from typing import List
from typing import Tuple
import requests
from bs4 import BeautifulSoup   

class Chunker:

    async def chunk(self, text, mode):
        if mode == "local":
            text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
            splitted_text = text_splitter.split_text(text)
            return splitted_text
        elif mode == "azure":
            # TODO: Support Azure here
            return
        
class Embedder:

    async def embed(self, splitted_text: List[str], kernel: Kernel):

        # TODO: Check if memory skill lodaded, exit if not
        memory_collection_name = "resourceEssay"
        print("Adding reference resource to a volatile Semantic Memory.")

        i = 1
        for chunk in splitted_text:
            await kernel.memory.save_information_async(
                collection=memory_collection_name,
                text=chunk,
                id=i,
            )
            i += 1


class Scraper:

    async def scrape_async(self, url):
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
        
    