# ORCHESTRATION
from semantic_kernel.connectors.ai.open_ai import (
    AzureChatCompletion,
    AzureTextCompletion,
    AzureTextEmbedding,
)
import semantic_kernel as sk

# Native Function
from ai.skills.EssayControls.controls import Citations

from typing import Tuple
import os
from utils.constants import (
    OPENAI_DEPLOYMENT_NAME,
    OPENAI_ENDPOINT,
    OPENAI_API_KEY,
    OPENAI_EMBEDDING_MODEL_NAME,
)

class KernelConfig:
    def __init__(self):
        self.kernel = sk.Kernel()
        self.add_chat_service()
        self.add_embedding_service()
        self.print_ai_services()


    def add_chat_service(self):
        azure_chat_service = AzureChatCompletion(
            deployment_name=OPENAI_DEPLOYMENT_NAME,
            endpoint=OPENAI_ENDPOINT,
            api_key=OPENAI_API_KEY,
        )
        self.kernel.add_chat_service("azure_chat_completion", azure_chat_service)

    def add_embedding_service(self):
        azure_embedding_service = AzureTextEmbedding(
            deployment_name=OPENAI_EMBEDDING_MODEL_NAME,
            endpoint=OPENAI_ENDPOINT,
            api_key=OPENAI_API_KEY,
        )
        self.kernel.add_text_embedding_generation_service("ada", azure_embedding_service)

    def equip_with_memory(self):
        # Todo: Add Azure AI Service and Chromadb support
        # Todo: Add OpenAI support
        # Work with volatile memory
        self.kernel.register_memory_store(memory_store=sk.memory.VolatileMemoryStore())

    def equip_with_builtin_skills(self):
        # Builtin native plugin: To store and retrieve text in memory
        self.kernel.import_skill(sk.core_skills.TextMemorySkill())
        # Load Skills

    def equip_with_semantic_skills(self) -> sk.SKFunctionBase:
        return self.kernel.import_semantic_skill_from_directory(
            "ai/skills", "WriteAnEssay"
        )

    def equip_with_native_skills(self) -> sk.SKFunctionBase:
        return self.kernel.import_skill(Citations(), skill_name="Citiations")

    def print_ai_services(self):
        print(f"Text completion services: {self.kernel.all_text_completion_services()}")
        print(f"Chat completion services: {self.kernel.all_chat_services()}")
        print(f"Text embedding generation services: {self.kernel.all_text_embedding_generation_services()}"
        )

   