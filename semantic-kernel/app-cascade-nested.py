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
        "ai/skills", "generateContent"
    )

    # Main input
    topic="Many employees demand to spend more of their working hours in home-office. Discuss chances and risks with respect to the required IT-infrastructure."
    


################# APP #######################
    # Create Context Variables
    context_variables = sk.ContextVariables()
    context_variables['topic'] = topic

    context = kernel.create_new_context()
    
    TopicType = kernel.skills.data["generatecontent"]["topictype"]
    TopicType = kernel.skills.get_function("generatecontent", "topictype")
    TopicType = generateContent['TopicType']

    TopicType = generateContent['TopicType']
    topic_type = TopicType(topic)
    
    context_variables['topic_type'] = topic_type.result
    context_variables['input'] = topic

    context["topic_type"] = topic_type.result
    context["input"] = topic

    Title = generateContent['Title']
    title = Title(variables=context_variables)
    title = Title(context=context)
    context_variables['title'] = title.result
    # title = Title(topic)
    
    SubTitle = generateContent['Subtitle']
    sub_title = SubTitle(topic)

    context_variables['sub_title'] = sub_title.result

    TableOfContents = generateContent['TableOfContents']
    tableOfContents = TableOfContents(variables=context_variables)


    rendered_article_list = [context_variables['title']]

    table_of_contents_deserialized = json.loads(tableOfContents.result)

    Chapter = generateContent["Chapter"]
    for chapter in table_of_contents_deserialized:
        context_variables['chapter'] = chapter['chapter']
        context_variables["sub_topics"] = "\n".join(f"- {element}" for element in chapter["topics"])
        generated_chapter = Chapter(variables=context_variables)
        rendered_article_list.append(generated_chapter.result)


    # Get the current date and time
    now = datetime.now()

    # Format the date and time as a string
    timestamp = now.strftime("%H%M%S")
    # Append the timestamp to the filename
    filename = f'essay_debug_{timestamp}.txt'

    rendered_essay = "\n".join(rendered_article_list)

    with open(filename, 'w') as f:
        f.write(rendered_essay)

    print("end")

# Run the main function
asyncio.run(main())