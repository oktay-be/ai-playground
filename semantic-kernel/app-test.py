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
    kernel.register_memory_store(memory_store=sk.memory.VolatileMemoryStore())
    kernel.import_skill(sk.core_skills.TextMemorySkill())
    kernel.import_semantic_skill_from_directory(
        "ai/skills", "WriteAnEssay"
    )

    # Main input
    sentence="Many employees demand to spend more of their working hours in home-office. Discuss chances and risks with respect to the required IT-infrastructure."

    # Reference
    url = "https://blog-idceurope.com/home-office-is-an-advantage-but-security-risks-remain/"

    scraper = Scraper()
    chunker = Chunker()
    embedder = Embedder()

    text = await scraper.scrape_async(url)
    chunked_text = await chunker.chunk(text, "local")
    await embedder.embed(chunked_text, kernel)

    # Create Context Variables
    context_variables = sk.ContextVariables()

    # Open the file
    with open('chapters_example.json', 'r') as f:
        # Load the JSON data from the file
        tableOfContents_deserialized = json.load(f)

    context_variables["relevance"] = 0.7
    context_variables["collection"] = "resourceEssay"

    context = kernel.create_new_context()
    context[sk.core_skills.TextMemorySkill.COLLECTION_PARAM] = "resourceEssay"
    context[sk.core_skills.TextMemorySkill.RELEVANCE_PARAM] = 0.7

    rendered_essay_list = ["title"]

    Chapter = writeAnEssay["Chapter"]
    for chapter in tableOfContents_deserialized:
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