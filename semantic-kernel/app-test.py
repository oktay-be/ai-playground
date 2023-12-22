import semantic_kernel as sk
import asyncio
from ai.kernel_config import KernelConfig
from utils.validator import Validator
from utils.common import Chunker, Embedder, Scraper
import json
from datetime import datetime
    
async def main():

    kernel_config = KernelConfig()

    # Equip kernel with skills 
    kernel_config.equip_with_builtin_skills()
    kernel_config.equip_with_memory()
    writeAnEssay = kernel_config.equip_with_semantic_skills()
    essayControls = kernel_config.equip_with_native_skills(7, 11)
    kernel = kernel_config.kernel


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