import asyncio

from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.ui import Console
from autogen_core.models import ModelCapabilities, ModelInfo
from autogen_ext.agents.web_surfer import MultimodalWebSurfer
from autogen_ext.models.ollama import OllamaChatCompletionClient
from playwright.async_api import BrowserContext, Download, Page, Playwright, async_playwright


async def main():
    custom_model_capabilities = ModelInfo(
        is_chat_model=True,
        is_tool_model=True,  # Set to True if it supports function calling
        is_image_model=True,  # Set to True if it supports processing images
        is_video_model=False,  # Set to True if it supports processing videos
        is_audio_model=False,
        json_output= True,  # Set to True if it supports processing audio
        function_calling= True,
        vision= True
    )

    ollama_model_client = OllamaChatCompletionClient(model="llama3.2", model_capabilities=custom_model_capabilities)

    web_suffer_agent = MultimodalWebSurfer(
        name= "webSurfer",
        model_client=ollama_model_client,
        headless=False,
        animate_actions=True
    )

    agent_team = RoundRobinGroupChat(participants=[web_suffer_agent], max_turns=10)

    await Console(agent_team.run_stream(task="Navigate to iskcon boston website"
                                             "click on Contribute link and navigate on contribute page"
                                             "Observe how many ways to donate"))

    await web_suffer_agent.close()
    await ollama_model_client.close()

asyncio.run(main())