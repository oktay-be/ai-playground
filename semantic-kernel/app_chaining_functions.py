import semantic_kernel as sk
import asyncio
from utils.validator import Validator
from ai.skills.WriteAnEssay.Orchestrator import Orchestrator
from ai.kernel_config import KernelConfig
import json
from datetime import datetime
import time

start_time = time.time()
    
async def main():

    kernel_config = KernelConfig()

    # Equip kernel with skills 
    kernel_config.equip_with_builtin_skills()
    kernel_config.equip_with_memory()
    writeAnEssay = kernel_config.equip_with_semantic_skills()
    essayControls = kernel_config.equip_with_native_skills()
    kernel = kernel_config.kernel

    # Main input
    sentence="Many employees demand to spend more of their working hours in home-office. Discuss chances and risks with respect to the required IT-infrastructure."

    # References
    # Todo: Support list
    url = "https://blog-idceurope.com/home-office-is-an-advantage-but-security-risks-remain/"

    # Create Context Variables
    context_variables = sk.ContextVariables()
    context_variables["original_input"] = sentence
    context_variables["input"] = sentence
    context_variables["relevance"] = 0.7
    context_variables["collection"] = "resourceEssay"
    context_variables["generated_content_type"] = "article"

    orchestrator = Orchestrator(kernel)

    await orchestrator.add_to_memory(url, "resourceEssay")

    generated_content = (
        await kernel.run_async(
            kernel.skills.data["writeanessay"]["orchestrate_flow"],
            input_vars=context_variables,
        )
    )

    end_time = time.time()
    execution_time = end_time - start_time
    print(f"The script executed in {execution_time} seconds.")

    print(generated_content["calibrated_content"])

# Run the main function
asyncio.run(main())