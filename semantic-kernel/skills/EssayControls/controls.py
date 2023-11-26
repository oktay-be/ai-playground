import random
from semantic_kernel.skill_definition import sk_function


class Citations:
    def __init__(self, min, max):
        self.min = min
        self.max = max

    @sk_function(
        description="Determine the number of citations",
        name="CitationsNumber",
        input_description="The value to take the square root of",
    )
    def generate_random_integer(self) -> str:
        return str(random.randint(self.min, self.max))

# class Style:
#     self.essay_style = "Academic"
#     @sk_function(
#         description="Style of the essay",
#         name="styler",
#         input_description="The value to take the square root of",
#     )
#     def square_root(self) -> str:
#         return self.essay_style