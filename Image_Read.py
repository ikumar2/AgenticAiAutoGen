import asyncio
import os
from utils.FileHelper import get_project_path

from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.messages import MultiModalMessage
from autogen_agentchat.ui import Console
from autogen_core import Image
from autogen_ext.models.ollama import OllamaChatCompletionClient
from dotenv import load_dotenv

load_dotenv()


async def main():
    data_file = get_project_path('data', 'Speech-learning-Assistant_V1.0.png')
    ollama_model_client = OllamaChatCompletionClient(model="llama3.2-vision")
    assistant = AssistantAgent(name="MultiModelAssistant", model_client=ollama_model_client)
    image = Image.from_file(data_file)
    multimodal_message= MultiModalMessage(
        content=["What do you see the this image", image ], source= "user"
    )
    await Console(assistant.run_stream(task=multimodal_message))
    await ollama_model_client.close()

asyncio.run(main())