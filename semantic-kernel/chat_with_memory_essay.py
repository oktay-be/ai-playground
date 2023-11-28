from semantic_kernel.connectors.ai.open_ai import (
    AzureChatCompletion,
    AzureTextEmbedding,
)
import semantic_kernel as sk
from utils.constants import (
    OPENAI_DEPLOYMENT_NAME, OPENAI_ENDPOINT, OPENAI_API_KEY
)
import asyncio
from typing import Tuple

def print_ai_services(kernel):
    print(f"Text completion services: {kernel.all_text_completion_services()}")
    print(f"Chat completion services: {kernel.all_chat_services()}")
    print(
        f"Text embedding generation services: {kernel.all_text_embedding_generation_services()}"
    )

# Will be saved in embeddings
async def populate_memory(kernel: sk.Kernel) -> None:
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
    - {{$fact6}} {{recall $fact6}}
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
    context["fact5"] = "How many poeple are there in my family?"
    context["fact6"] = """
        4. Assessing IT Infrastructure for Remote Work
    - Reliable internet connection and bandwidth requirements
    - Secure and efficient VPN setup
    - Access to necessary software and tools
    - Backup and data protection measures
    """


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

async def main():

    kernel = sk.Kernel()

    # Not availble for gtp-35-turbo-16k:  More info: https://learn.microsoft.com/en-us/azure/ai-services/openai/concepts/models#gpt-35-models
    # kernel.add_text_completion_service(
    #     service_id="azure_gpt35_text_completion",
    #     service=AzureTextCompletion(
    #         OPENAI_DEPLOYMENT_NAME, OPENAI_ENDPOINT, OPENAI_API_KEY
    #     ),
    # )

    azure_chat_service = AzureChatCompletion(
        deployment_name=OPENAI_DEPLOYMENT_NAME,
        endpoint=OPENAI_ENDPOINT,
        api_key=OPENAI_API_KEY,
    )

    # Equip kernel
    kernel.add_chat_service("azure_chat_completion", azure_chat_service)
    kernel.add_text_embedding_generation_service("ada", AzureTextEmbedding("text-embedding-ada-002", OPENAI_ENDPOINT, OPENAI_API_KEY))

    # Work with volatile memory
    kernel.register_memory_store(memory_store=sk.memory.VolatileMemoryStore())

    # Builtin native plugin: To store and retrieve text in memory
    kernel.import_skill(sk.core_skills.TextMemorySkill())

    # End of Equip Kernel

    github_files ={}
    github_files["https://github.com/microsoft/semantic-kernel/blob/main/README.md"] = \
        "README: Installation, getting started, and how to contribute"
    github_files["https://github.com/microsoft/semantic-kernel/blob/main/dotnet/notebooks/02-running-prompts-from-file.ipynb"] = \
        "Jupyter notebook describing how to pass prompts from a file to a semantic skill or function"
    github_files["https://github.com/microsoft/semantic-kernel/blob/main/dotnet/notebooks/00-getting-started.ipynb"] = \
        "Jupyter notebook describing how to get started with the Semantic Kernel"
    github_files["https://github.com/microsoft/semantic-kernel/tree/main/samples/skills/ChatSkill/ChatGPT"] = \
        "Sample demonstrating how to create a chat skill interfacing with ChatGPT"
    github_files["https://github.com/microsoft/semantic-kernel/blob/main/dotnet/src/SemanticKernel/Memory/Volatile/VolatileMemoryStore.cs"] = \
        "C# class that defines a volatile embedding store"


    memory_collection_name = "SKGitHub"
    print("Adding some GitHub file URLs and their descriptions to a volatile Semantic Memory.");
    i = 0
    for entry, value in github_files.items():
        await kernel.memory.save_reference_async(
            collection=memory_collection_name,
            description=value,
            text=value,
            external_id=entry,
            external_source_name="GitHub"
        )
        i += 1
        print("  URL {} saved".format(i))

    ask = "I love Jupyter notebooks, how should I get started?"
    print("===========================\n" + "Query: " + ask + "\n")

    memories = await kernel.memory.search_async(memory_collection_name, ask, limit=5, min_relevance_score=0.77)

    i = 0
    for memory in memories:
        i += 1
        print(f"Result {i}:")
        print("  URL:     : " + memory.id)
        print("  Title    : " + memory.description)
        print("  Relevance: " + str(memory.relevance))
        print()

    # from semantic_kernel.connectors.memory.azure_cognitive_search import AzureCognitiveSearchMemoryStore

    # azure_ai_search_api_key, azure_ai_search_url = sk.azure_aisearch_settings_from_dot_env()

    # #text-embedding-ada-002 uses a 1536-dimensional embedding vector
    # kernel.register_memory_store(
    #     memory_store=AzureCognitiveSearchMemoryStore(
    #         vector_size=1536,
    #         search_endpoint=azure_ai_search_url,
    #         admin_key=azure_ai_search_api_key
    #     )
    # )

    print_ai_services(kernel)

    print("Populating memory...")
    await populate_memory(kernel)

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