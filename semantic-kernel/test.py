# CONSTANTS
from utils.constants import (
    OPENAI_DEPLOYMENT_NAME,
    OPENAI_ENDPOINT,
    OPENAI_API_KEY,
    DOCUMENT_MAP,
    DIR_PATH,
)
from utils.common import Scraper
from ai.kernel_config import KernelConfig
import semantic_kernel as sk
# TOOLING
import asyncio 
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document
from typing import Tuple

from datetime import datetime

# Will be saved in embeddings
async def populate_memory(kernel: sk.Kernel) -> None:
    # Todo: SaveReferenceAsync check
    # Add some documents to the semantic memory
    await kernel.memory.save_information_async(
        "aboutMe", id="info1", text="My name is Andrea"
    )
    await kernel.memory.save_information_async(
        "aboutMe", id="info2", text="I currently work as a tour guide"
    )
    await kernel.memory.save_information_async(
        "aboutMe", id="info3", text="I've been living in Seattle since 2005"
    )
    await kernel.memory.save_information_async(
        "aboutMe", id="info4", text="I visited France and Italy five times since 2015"
    )
    await kernel.memory.save_information_async(
        "aboutMe", id="info5", text="I received my postgraduate degree in 2010"
    )
    await kernel.memory.save_information_async(
        "aboutMe", id="info6", text="I have 3 kids"
    )


async def search_memory_examples(kernel: sk.Kernel) -> None:
    questions = [
        "what's my name",
        "where do I live?",
        "where's my family from?",
        "where have I traveled?",
        "what do I do for work",
    ]


    for question in questions:
        print(f"Question: {question}")
        result = await kernel.memory.search_async("aboutMe", question)
        print(f"Answer: {result[0].text}\n")
        
async def setup_chat_with_memory(
    kernel: sk.Kernel,
) -> Tuple[sk.SKFunctionBase, sk.SKContext]:
    sk_prompt = """
    ChatBot can have a conversation with you about any topic.
    It can give explicit instructions or say 'I don't know' if
    it does not have an answer.

    Information about me, from previous conversations:
    +++++
    - {{$fact1}} {{recall $fact1}}
    - {{$fact2}} {{recall $fact2}}
    - {{recall $fact3}}
    - {{recall $fact4}}
    +++++

    Chat:
    *****
    {{$chat_history}}
    *****
    User: {{$user_input}}
    ChatBot: """.strip()


    chat_func = kernel.create_semantic_function(sk_prompt, max_tokens=200, temperature=0.8)

    context = kernel.create_new_context()
    context["fact1"] = "what is my name?"
    context["fact2"] = "where do I live?"
    context["fact3"] = "How many poeple are there in my family?"
    context["fact4"] = "When did I graduate from college?"


    context[sk.core_skills.TextMemorySkill.COLLECTION_PARAM] = "aboutMe"
    context[sk.core_skills.TextMemorySkill.RELEVANCE_PARAM] = 0.8

    context["chat_history"] = ""

    return chat_func, context

async def chat(
    kernel: sk.Kernel, chat_func: sk.SKFunctionBase, context: sk.SKContext
) -> bool:
    try:
        user_input = input("User:> ")
        context["user_input"] = user_input
        print(f"User:> {user_input}")
    except KeyboardInterrupt:
        print("\n\nExiting chat...")
        return False
    except EOFError:
        print("\n\nExiting chat...")
        return False

    if user_input == "exit":
        print("\n\nExiting chat...")
        return False

    answer = await kernel.run_async(chat_func, input_vars=context.variables)
    context["chat_history"] += f"\nUser:> {user_input}\nChatBot:> {answer}\n"

    print(f"ChatBot:> {answer}")
    return True

# TODO: autodetect envoding
# doc = load_single_document(file_path)
# create_directory(DIR_PATH)
# file_path = await write_text(text)


async def main():

    kernel_wrapper = KernelConfig()
    kernel_wrapper.equip_with_builtin_skills()
    kernel_wrapper.equip_with_memory()

    print("Populating memory...")
    await populate_memory(kernel_wrapper.kernel)

    print("Asking questions... (manually)")
    await search_memory_examples(kernel_wrapper.kernel)

    print("Setting up a chat (with memory!)")
    chat_func, context = await setup_chat_with_memory(kernel_wrapper.kernel)

    # print("Begin chatting (type 'exit' to exit):\n")
    # chatting = True
    # while chatting:
    #     chatting = await chat(kernel_wrapper.kernel, chat_func, context)



    ###########################################

    scraper = Scraper()

    url = "https://blog-idceurope.com/home-office-is-an-advantage-but-security-risks-remain/"

    text = await scraper.scrape_async(url)

    
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
    splitted_text = text_splitter.split_text(text)
    
    memory_collection_name = "resourceEssay"
    print("Adding reference resource to a volatile Semantic Memory.")

    i = 1
    for chunk in splitted_text:
        await kernel_wrapper.kernel.memory.save_information_async(
            collection=memory_collection_name,
            text=chunk,
            id=i,
        )
        i += 1

    ask = "How does remote working effect competitiveness?"
    memories = await kernel_wrapper.kernel.memory.search_async(memory_collection_name, ask, limit=5, min_relevance_score=0.50)

    print("asa")



# Run the main function
asyncio.run(main())