import semantic_kernel as sk
import asyncio
from ai.kernel_config import KernelConfig
from utils.validator import Validate

    
async def main():

    kernel = KernelConfig()

    # Equip kernel with skills 
    kernel.equip_with_builtin_skills()
    writeAnEssay = kernel.equip_with_semantic_skills()
    essayControls = kernel.equip_with_native_skills(7, 11)

    # Main input
    sentence="Many employees demand to spend more of their working hours in home-office. Discuss chances and risks with respect to the required IT-infrastructure."

    # Create Context Variables
    context_variables = sk.ContextVariables()

    ArgumentType = writeAnEssay['ArgumentType']
    response = Validate(ArgumentType(sentence))


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


    print("end")

# Run the main function
asyncio.run(main())