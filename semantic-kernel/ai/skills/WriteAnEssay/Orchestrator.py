import random
import json
from datetime import datetime
from semantic_kernel.skill_definition import sk_function
from semantic_kernel import SKContext, Kernel
from utils.validator import Validator
from utils.common import Chunker, Embedder, Scraper


class Orchestrator:
    def __init__(self, kernel: Kernel):
        self._kernel = kernel

    @sk_function(
        description="Routes the request to the appropriate function",
        name="orchestrate_flow",
    )
    async def orchestrate(self, context: SKContext) -> str:
        # Loading functions like this. So that we have the flexibility of loading different functions with the same name depending on a condition
        GenerateArgumentType = self._kernel.skills.get_function("WriteAnEssay", "GenerateArgumentType")
        GenerateBaslik = self._kernel.skills.get_function("writeanessay","GenerateBaslik")
        GenerateAltBaslik = self._kernel.skills.get_function("writeanessay","GenerateAltBaslik")
        GenerateTableOfContents = self._kernel.skills.get_function("writeanessay","GenerateTableOfContents")
        # self._kernel.skills.data["writeanessay"]["citationsNumber"]
        GenerateChapters = self._kernel.skills.get_function("writeanessay","GenerateChapters")
        CalibrateGeneratedContent = self._kernel.skills.get_function("writeanessay","CalibrateGeneratedContent")

        result = await self._kernel.run_async(
            GenerateArgumentType,
            GenerateBaslik,
            GenerateAltBaslik,
            # CitationsNumber,
            GenerateTableOfContents,
            GenerateChapters,
            CalibrateGeneratedContent,
            input_vars=context.variables
            )

        return result
    
    async def add_to_memory(self, url: str) -> None:

        scraper = Scraper()
        chunker = Chunker()
        embedder = Embedder()

        text = await scraper.scrape_async(url)
        chunked_text = await chunker.chunk(text, "local")
        await embedder.embed(chunked_text, self._kernel)

    @sk_function(
        description="Determine the number of citations",
        name="CitationsNumber",
        input_description="The value to take the square root of",
    )
    def generate_random_integer(self, context: SKContext) -> str:
        return str(random.randint(context["min"], context["max"]))

################### GENERATE ARGUMENT TYPE #######################
    
    @sk_function(
        description="Generates argument type",
        name="GenerateArgumentType",
        input_description="Context variables",
    )
    def generate_argument_type(self, context: SKContext) -> str:
        ArgumentType = self._kernel.skills.get_function("writeanessay","argumentType")
        argument_type = Validator.validate(ArgumentType(context["input"]))
        context["argument_type"] = argument_type
        # This is goingt to be assigned to context["input"] for the next SF
        return "bas"
        
################### GENERATE BASLIK #######################
    
    @sk_function(
        description="Generates baslik",
        name="GenerateBaslik",
        input_description="Context variables",
    )
    def generate_baslik(self, context: SKContext) -> str:
        Baslik = self._kernel.skills.get_function("writeanessay","Baslik")
        baslik = Validator.validate(Baslik(variables=context.variables))
        context["baslik"] = baslik
        return "bas"
    
################### GENERATE ALT BASLIK #######################
    
    @sk_function(
        description="Generates alt baslik",
        name="GenerateAltBaslik",
        input_description="Context variables",
    )
    def generate_alt_baslik(self, context: SKContext) -> str:
        AltBaslik = self._kernel.skills.get_function("writeanessay","AltBaslik")
        alt_baslik = Validator.validate(AltBaslik(variables=context.variables))
        context["alt_baslik"] = alt_baslik
        return "bas"
    
################### GENERATE TABLE OF CONTENTS #######################
    
    @sk_function(
        description="Generates generate table of contents",
        name="GenerateTableOfContents",
        input_description="Context variables",
    )
    def generate_table_of_contents(self, context: SKContext) -> str:
        TableOfContents = self._kernel.skills.get_function("writeanessay","TableOfContents")
        tableOfContents = Validator.validate(TableOfContents(variables=context.variables))
        context["table_of_contents"] = tableOfContents
        return "some_input"

################### GENERATE CHAPTERS #######################

    @sk_function(
        description="Generates chapters",
        name="GenerateChapters",
        input_description="Context variables",
    )
    async def generate_chapters(self, context: SKContext) -> str:
        
        # Get the current date and time
        now = datetime.now()

        # Format it as a string in the 'YY-MM-DD-HH-MM' format
        timestamp = now.strftime('%Y-%m-%d-%H-%M')

        # Add the timestamp to the filename
        filename = f'essay_{timestamp}.txt'

        rendered_essay_list = [context["baslik"]]

        # TODO: Validate json here
        # TODO: Record json in cloud for later use
        Chapter = self._kernel.skills.get_function("writeanessay","chapter")
        tableOfContents_deserialized = json.loads(context["table_of_contents"])
        for chapter in tableOfContents_deserialized:
            context["subtopics"] = "\n".join(f"- {element}" for element in chapter["topics"])
            context["chapter"] = chapter["chapter"]
            gen_chapter2 = Validator.validate(await self._kernel.run_async(Chapter, input_vars=context.variables))
            rendered_essay_list.append(gen_chapter2)
        context["original_article"] = "\n".join(rendered_essay_list)

        # Open the file in write mode
        with open(filename, 'w') as file:
            # Write the essay to the file
            file.write(context["original_article"])
        return "bas"

################### CALIBRATE #######################

    @sk_function(
        description="Calibrate Article",
        name="CalibrateGeneratedContent",
        input_description="Calibrate Generated Content",
    )
    async def calibrate_generated_content(self, context: SKContext) -> str:
        # Get the current date and time
        now = datetime.now()

        # Format it as a string in the 'YY-MM-DD-HH-MM' format
        timestamp = now.strftime('%Y-%m-%d-%H-%M')

        # Add the timestamp to the filename
        filename_calibrated = f'essay_calibrated_{timestamp}.txt'

        CalibrateContent = self._kernel.skills.get_function("writeanessay","calibrate")
        calibratedContent = Validator.validate(CalibrateContent(variables=context.variables))
        context["calibrated_article"] = '\n'.join([context["baslik"], calibratedContent])
        
        # Open the file in write mode
        with open(filename_calibrated, 'w') as file:
            # Write the essay to the file
            file.write(context["calibrated_article"])
        return "bas"
