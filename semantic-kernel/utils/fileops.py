# CONSTANTS
from utils.constants import (
    OPENAI_DEPLOYMENT_NAME,
    OPENAI_ENDPOINT,
    OPENAI_API_KEY,
    DOCUMENT_MAP,
    DIR_PATH,
)

# TOOLING
import asyncio
from typing import Tuple
import requests
from bs4 import BeautifulSoup   
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document
import os
from datetime import datetime

# FILE OPS
class FileOps:
    def __init__(self, dir_path):
        self.dir_path = dir_path

    def load(self) -> Tuple[Document]:
        raise NotImplementedError
    
    def create_directory(self):
        if not os.path.exists(self.dir_path):
            os.makedirs(self.dir_path)

    async def write_text(self, text) -> str:
        # Create a timestamp
        timestamp = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')

        # Create a file path with the timestamp
        file_path = os.path.join(self.dir_path, f'{timestamp}.txt')

        # Write the text to the file
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(text)

        return file_path

    # Relevant when files are loaded
    def load_single_document(self, file_path: str) -> Document:
        # Loads a single document from a file path
        file_extension = os.path.splitext(file_path)[1]
        loader_class = DOCUMENT_MAP.get(file_extension)
        if loader_class:
            loader = loader_class(file_path)
        else:
            raise ValueError("Document type is undefined")
        return loader.load()[0]