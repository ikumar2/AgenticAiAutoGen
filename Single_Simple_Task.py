import asyncio
import os

from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.ui import Console
from autogen_ext.models.ollama import OllamaChatCompletionClient
from dotenv import load_dotenv

load_dotenv()

async def main():

    ollama_model_client = OllamaChatCompletionClient(model="llama3.2")
    assistance = AssistantAgent(name="assistant",model_client=ollama_model_client)
    await Console(assistance.run_stream(task="Why agentic ai is important for testing"))
    await ollama_model_client.close()

asyncio.run(main())