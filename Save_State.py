import asyncio
import json

from autogen_agentchat.agents import AssistantAgent, UserProxyAgent
from autogen_agentchat.ui import Console
from autogen_ext.models.ollama import OllamaChatCompletionClient



async def main():
    ollama_model_client = OllamaChatCompletionClient(model="llama3.2")

    agent1 = AssistantAgent(name="Helper", model_client= ollama_model_client)

    agent2 = AssistantAgent(name="Backup_Helper", model_client= ollama_model_client)

    await Console(agent1.run_stream(task="My favorite time early morning in day time"))
    state = await agent1.save_state()
    with open("memory.json", "w") as f :
        json.dump(state, f, default=str)

    with open("memory.json", "r") as f :
        save_state = json.load(f)

    await agent2.load_state(save_state)
    await Console(agent2.run_stream(task="what is my favorite time in day"))

    await ollama_model_client.close()

asyncio.run(main())