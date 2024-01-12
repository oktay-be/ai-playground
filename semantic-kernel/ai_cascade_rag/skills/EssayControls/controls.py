import random
from semantic_kernel.skill_definition import sk_function
from semantic_kernel import SKContext


class Citations:

    @sk_function(
        description="Determine the number of citations",
        name="CitationsNumber",
        input_description="The value to take the square root of",
    )
    def generate_random_integer(self, context: SKContext) -> str:
        return str(random.randint(context["min"], context["max"]))
