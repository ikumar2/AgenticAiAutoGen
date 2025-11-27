import asyncio

from autogen_agentchat.agents import AssistantAgent, UserProxyAgent
from autogen_agentchat.conditions import TextMentionTermination
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.ui import Console
from autogen_core.models import ModelInfo
from autogen_ext.models.ollama import OllamaChatCompletionClient
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_ext.tools.mcp import StdioServerParams, McpWorkbench
from openai import videos
from utils.FileHelper import get_project_path



async def main():
    file_store_path = str(get_project_path('Data')) # As tool by default read and write on root level so to making under Data need to touch code of fileserver.
    filesystem_server_params = StdioServerParams(command="npx",
                                                 args=["-y",
                                                       "@modelcontextprotocol/server-filesystem",
                                                        file_store_path],
                                                        read_timeout_seconds=60)

    fs_workbench = McpWorkbench(filesystem_server_params)

    async with fs_workbench as fs_wb:

        custom_model_capabilities = ModelInfo(
            json_output=True,  # Set to True if it supports processing audio
            function_calling=True,
            vision=True
            )
        ollama_model_client = OllamaChatCompletionClient(model="llama3.2", model_capabilities=custom_model_capabilities)

        math_tutor = AssistantAgent(name="MathTutor", model_client=ollama_model_client, workbench=fs_wb,
                                   system_message="you are helpful math tutor. Help the user to solve math problems step by step. "
                                                  "you have to access file system to create file and store. "
                                                  "write the file under Data director."
                                                  "When user says 'Thanks Done' or 'Bye' or similar, acknowledge and say 'LESSON COMPLETED'")

        user_proxy = UserProxyAgent(name="student")
        team = RoundRobinGroupChat(participants=[user_proxy, math_tutor],
                                   termination_condition=TextMentionTermination("LESSON COMPLETED"))

        await Console(team.run_stream(task='I need help with algebra problem. '
                                           'Tutor, feel free to create files to help with student learning'))
        await ollama_model_client.close()

asyncio.run(main())