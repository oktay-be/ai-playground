import semantic_kernel as sk
import asyncio
import json
from datetime import datetime
from semantic_kernel.connectors.ai.open_ai import (
    AzureChatCompletion,
    AzureTextCompletion,
    AzureTextEmbedding,
)
import os
import semantic_kernel as sk
import requests
from bs4 import BeautifulSoup  
from langchain.text_splitter import RecursiveCharacterTextSplitter
import time


# from semantic_kernel.connectors.memory.milvus import MilvusMemoryStore

async def main():
    kernel = sk.Kernel()

    azure_chat_service = AzureChatCompletion(
        deployment_name="gpt-35-turbo-16k",
        endpoint=os.getenv("OPENAI_ENDPOINT"),
        api_key=os.getenv("OPENAI_API_KEY"),
    )

    azure_embedding_service = AzureTextEmbedding(
        deployment_name="text-embedding-ada-002",
        endpoint=os.getenv("OPENAI_ENDPOINT"),
        api_key=os.getenv("OPENAI_API_KEY"),
    )

    kernel.add_chat_service("azure_chat_completion", azure_chat_service)
    kernel.add_text_embedding_generation_service("ada", azure_embedding_service)
    
    generateContent = kernel.import_semantic_skill_from_directory(
        "ai_nested/skills", "generateContent"
    )

    # Main input
    topic="Many employees demand to spend more of their working hours in home-office. Discuss chances and risks with respect to the required IT-infrastructure."
    


################# APP #######################
    # Create Context Variables
    
    # SubTitle = generateContent['Subtitle']
    # sub_title = SubTitle(topic)
    start_time = time.time()


    TableOfContents = generateContent['TableOfContents']
    tableOfContents = TableOfContents(topic)

    end_time = time.time()
    execution_time = end_time - start_time
    print(f"The script executed in {execution_time} seconds.")

    print("end")

# Run the main function
asyncio.run(main())