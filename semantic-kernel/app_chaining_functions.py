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
    essayControls = kernel_config.equip_with_native_skills()
    kernel = kernel_config.kernel

    ArgumentType = writeAnEssay['ArgumentType']
    Baslik = writeAnEssay['Baslik']
    AltBaslik = writeAnEssay['AltBaslik']
    CitationsNumber = essayControls["CitationsNumber"]
    GenerateTableOfContents = essayControls['GenerateTableOfContents']
    GenerateChapters = essayControls['GenerateChapters']

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
    context_variables["original_request"] = sentence
    context_variables["input"] = sentence
    context_variables["relevance"] = 0.7
    context_variables["collection"] = "resourceEssay"

    await kernel.run_async(
        ArgumentType,
        Baslik,
        AltBaslik,
        CitationsNumber,
        GenerateTableOfContents,
        GenerateChapters,
        input_vars=context_variables
        )
    
    print("end")

# Run the main function
asyncio.run(main())