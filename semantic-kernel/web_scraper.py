# CONSTANTS
from utils.constants import (
    OPENAI_DEPLOYMENT_NAME,
    OPENAI_ENDPOINT,
    OPENAI_API_KEY,
    DOCUMENT_MAP,
    DIR_PATH,
)
from utils.fileops import Scraper

# TOOLING
import asyncio 
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document

from datetime import datetime

async def main():


    url = "https://blog-idceurope.com/home-office-is-an-advantage-but-security-risks-remain/"

    text = Scraper(url)

    
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
    splitted_text = text_splitter.split_text(text)
    
    memory_collection_name = "resourceEssay"
    print("Adding reference resource to a volatile Semantic Memory.");

    i = 0
    for chunk in splitted_text:
        await kernel.memory.save_reference_async(
            collection=memory_collection_name,
            # description=value,
            text=chunk,
            external_id=i,
            external_source_name="Web"
        )
        i += 1

    # memories = await kernel.memory.search_async(memory_collection_name, ask, limit=5, min_relevance_score=0.77)


    # print("Populating memory...")
    # await populate_memory(kernel)

    print("Asking questions... (manually)")
    await search_memory_examples(kernel)

    print("Setting up a chat (with memory!)")
    chat_func, context = await setup_chat_with_memory(kernel)

    print("Begin chatting (type 'exit' to exit):\n")
    chatting = True
    while chatting:
        chatting = await chat(kernel, chat_func, context)

# Run the main function
asyncio.run(main())