import random
from semantic_kernel.skill_definition import sk_function
from semantic_kernel import SKContext


class Handlers:

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


# class Style:
#     self.essay_style = "Academic"
#     @sk_function(
#         description="Style of the essay",
#         name="styler",
#         input_description="The value to take the square root of",
#     )
#     def square_root(self) -> str:
#         return self.essay_style