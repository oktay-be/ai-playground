import semantic_kernel as sk
import asyncio
from ai.kernel_config import KernelConfig
from utils.validator import Validator

    
async def main():

    kernel = KernelConfig()

    # Equip kernel with skills 
    kernel.equip_with_builtin_skills()
    generateContent = kernel.equip_with_semantic_skills()
    essayControls = kernel.equip_with_native_skills(7, 11)

    # Main input
    sentence="Many employees demand to spend more of their working hours in home-office. Discuss chances and risks with respect to the required IT-infrastructure."

    # Create Context Variables
    # context_variables = sk.ContextVariables()

    # TopicType = generateContent['TopicType']
    # TopicType = Validator.validate(TopicType(sentence))

    # Baslik = generateContent['Baslik']
    # title = Validator.validate(Baslik(sentence))

    # AltBaslik = generateContent['AltBaslik']
    # subtitle = Validator.validate(AltBaslik(sentence))

    # CitationsNumber = essayControls["CitationsNumber"]
    # citationsNumber = CitationsNumber()

    # context_variables['input'] = title
    # context_variables['subtitle'] = subtitle

    # Chapters = generateContent['Chapters']
    # chapters = Validator.validate(Chapters(variables=context_variables))

    # print(chapters)

    context_variables = sk.ContextVariables()
    # Main input
    sentence="Many employees demand to spend more of their working hours in home-office. Discuss chances and risks with respect to the required IT-infrastructure."
    context_variables['input'] = sentence

    kernel.kernel.run_async()

    print("end")

# Run the main function
asyncio.run(main())