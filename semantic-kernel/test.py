from semantic_kernel.connectors.ai.open_ai import (
    AzureChatCompletion,
    AzureTextCompletion,
)
import semantic_kernel as sk
from utils.constants import OPENAI_DEPLOYMENT_NAME, OPENAI_ENDPOINT, OPENAI_API_KEY
# from semantic_kernel.orchestration.context_variables import ContextVariables
from skills.EssayControls.controls import Citations

def print_ai_services(kernel):
    print(f"Text completion services: {kernel.all_text_completion_services()}")
    print(f"Chat completion services: {kernel.all_chat_services()}")
    print(
        f"Text embedding generation services: {kernel.all_text_embedding_generation_services()}"
    )

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

kernel.add_chat_service("azure_chat_completion", azure_chat_service)

print_ai_services(kernel)

# Load Skills
writeAnEssay = kernel.import_semantic_skill_from_directory(
    "Skills", "WriteAnEssay"
)
essayControls = kernel.import_skill(Citations(7,12), skill_name="Citiations")

# Main input
sentence="Many employees demand to spend more of their working hours in home-office. Discuss chances and risks with respect to the required IT-infrastructure."

# Create Context Variables
context_variables = sk.ContextVariables()

ArgumentType = writeAnEssay['ArgumentType']
response = ArgumentType(sentence)

Baslik = writeAnEssay['Baslik']
baslik = Baslik(sentence)

AltBaslik = writeAnEssay['AltBaslik']
altbaslik = AltBaslik(sentence)

CitationsNumber = essayControls["CitationsNumber"]
nr = CitationsNumber()

context_variables['input'] = baslik.result
context_variables['subtitle'] = altbaslik.result

Chapters = writeAnEssay['Chapters']
chapters = Chapters(variables=context_variables)

print(chapters.result)


if response.error_occurred:
    print(response.last_error_description)
else:
    print(response.result)

print(response)

print("end")