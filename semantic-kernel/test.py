from semantic_kernel.connectors.ai.open_ai import (
    AzureChatCompletion,
    AzureTextEmbedding,
)
import semantic_kernel as sk
from utils.constants import (
    OPENAI_DEPLOYMENT_NAME, OPENAI_ENDPOINT, OPENAI_API_KEY
)
import asyncio
from ai.dtt_semantic_kernel import dttKernel

    
async def main():

    kernel = dttKernel()

    # Main input
    sentence="Many employees demand to spend more of their working hours in home-office. Discuss chances and risks with respect to the required IT-infrastructure."

    # # Create Context Variables
    # context_variables = sk.ContextVariables()

    # ArgumentType = writeAnEssay['ArgumentType']
    # response = ArgumentType(sentence)

    # Baslik = writeAnEssay['Baslik']
    # baslik = Baslik(sentence)

    # AltBaslik = writeAnEssay['AltBaslik']
    # altbaslik = AltBaslik(sentence)

    # CitationsNumber = essayControls["CitationsNumber"]
    # nr = CitationsNumber()

    # context_variables['input'] = baslik.result
    # context_variables['subtitle'] = altbaslik.result

    # Chapters = writeAnEssay['Chapters']
    # chapters = Chapters(variables=context_variables)

    

    # print(chapters.result)


    # if response.error_occurred:
    #     print(response.last_error_description)
    # else:
    #     print(response.result)

    # print(response)

    print("end")

# Run the main function
asyncio.run(main())