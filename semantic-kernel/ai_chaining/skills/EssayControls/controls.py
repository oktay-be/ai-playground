import random
import json
from semantic_kernel.skill_definition import sk_function
from semantic_kernel import SKContext
from utils.validator import Validator


class Handlers:

    @sk_function(
        description="Determine the number of citations",
        name="CitationsNumber",
        input_description="The value to take the square root of",
    )
    def generate_random_integer(self, context: SKContext) -> str:
        return str(random.randint(context["min"], context["max"]))

    @sk_function(
        description="Generates generate table of contents",
        name="GenerateTableOfContents",
        input_description="Context variables",
    )
    def generate_table_of_contents(self, context: SKContext) -> str:
        print("inside generate_table_of_contents")

    @sk_function(
        description="Generates chapters",
        name="GenerateChapters",
        input_description="Context variables",
    )
    def generate_chapters(self, context: SKContext) -> str:
        print("inside generate_chapters")

        # Validate json here
        # Record json in cloud for later use
        tableOfContents_deserialized = json.loads(context["input"])
        for chapter in tableOfContents_deserialized:
            # gen_chapter2 = Validator.validate(await kernel.run_async(Chapter, input_vars=context_variables))
            # rendered_essay_list.append(gen_chapter2)
            print(chapter['chapter'])

# class Style:
#     self.essay_style = "Academic"
#     @sk_function(
#         description="Style of the essay",
#         name="styler",
#         input_description="The value to take the square root of",
#     )
#     def square_root(self) -> str:
#         return self.essay_style
# class Style:
#     self.essay_style = "Academic"
#     @sk_function(
#         description="Style of the essay",
#         name="styler",
#         input_description="The value to take the square root of",
#     )
#     def square_root(self) -> str:
#         return self.essay_style