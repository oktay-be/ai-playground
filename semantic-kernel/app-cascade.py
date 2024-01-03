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
    
    # kernel.register_memory_store(memory_store=sk.memory.VolatileMemoryStore())
    # kernel.import_skill(sk.core_skills.TextMemorySkill())

    # kernel.register_memory_store(memory_store=MilvusMemoryStore()) 
    
    generateContent = kernel.import_semantic_skill_from_directory(
        "ai/skills", "generateContent"
    )

    # Main input
    topic="Many employees demand to spend more of their working hours in home-office. Discuss chances and risks with respect to the required IT-infrastructure."

    # # Reference
    # url = "https://blog-idceurope.com/home-office-is-an-advantage-but-security-risks-remain/"

    # response = requests.get(url, verify=False, timeout=2)
    # if response.status_code == 200 and 'text/html' in response.headers['Content-Type']:
    #     soup = BeautifulSoup(response.text, 'html.parser')
    #     text = soup.get_text()

    # text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
    # splitted_text = text_splitter.split_text(text)

    # memory_collection_name = "resourceEssay"

    # print("Adding reference resource to a volatile Semantic Memory.")

    # i = 1
    # for chunk in splitted_text:
    #     await kernel.memory.save_information_async(
    #         collection=memory_collection_name,
    #         text=chunk,
    #         id=i,
    #     )
    #     i += 1

    # ask = "How does remote working effect competitiveness?"
    # memories = await kernel.memory.search_async(memory_collection_name, ask, limit=5, min_relevance_score=0.50)

################# APP #######################
    # Create Context Variables
    context_variables = sk.ContextVariables()
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
    # title = Title(topic)
    
    SubTitle = generateContent['SubTitle']
    sub_title = SubTitle(topic)

    context_variables['input'] = title
    context_variables['sub_title'] = sub_title

    TableOfContents = generateContent['TableOfContents']
    tableOfContents = TableOfContents(variables=context_variables)

    tableOfContents_deserialized = json.loads(tableOfContents)

    context_variables["relevance"] = 0.7
    context_variables["collection"] = "resourceEssay"

    context = kernel.create_new_context()
    context[sk.core_skills.TextMemorySkill.COLLECTION_PARAM] = "resourceEssay"
    context[sk.core_skills.TextMemorySkill.RELEVANCE_PARAM] = 0.7
   
    rendered_essay_list = ["title"]

    table_of_contents_deserialized = json.loads(tableOfContents)

    Chapter = generateContent["Chapter"]
    for chapter in table_of_contents_deserialized:
        # context_variables['chapter'] = chapter['chapter']
        searched = await kernel.memory.search_async("resourceEssay", chapter['chapter'], min_relevance_score=0.7)
        context_variables['searched'] = searched[0].text
        context_variables['chapter'] = chapter['chapter']
        context["searched"] = searched[0].text
        context["chapter"] = chapter['chapter']
        # gen_chapter = Validator.validate(Chapter(variables=context_variables))
        # gen_chapter = Validator.validate(Chapter(variables=context.variables))
        gen_chapter2 = await kernel.run_async(Chapter, input_vars=context_variables)
        rendered_essay_list.append(gen_chapter2.result)
        # rendered_essay_list.append(gen_chapter)

        # TODO: Debug if recall worked

    # Get the current date and time
    now = datetime.now()

    # Format the date and time as a string
    timestamp = now.strftime("%H%M%S")
    # Append the timestamp to the filename
    filename = f'essay_debug_{timestamp}.txt'

    rendered_essay = "\n".join(rendered_essay_list)

    with open(filename, 'w') as f:
        f.write(rendered_essay)

    print("end")

# Run the main function
asyncio.run(main())