import asyncio

from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.conditions import TextMentionTermination
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.ui import Console
from autogen_core.models import ModelInfo
from autogen_ext.code_executors import docker
from autogen_ext.models.ollama import OllamaChatCompletionClient

from utils.FileHelper import get_project_path
from autogen_ext.tools.mcp import StdioServerParams, McpWorkbench


async def main():
    credential_path = str(get_project_path('.env'))
    Jira_server_params = StdioServerParams(command="docker",
                      args=[
                          "run", "--rm", "-i",
                          "--env-file",
                            credential_path,
                          "ghcr.io/sooperset/mcp-atlassian:latest"
                      ])
    jira_workbench = McpWorkbench(Jira_server_params)

    playwright_server_params = StdioServerParams(command="npx",
                                                 args=["@playwright/mcp@latest"
                                                       ])
    playwright_workbench = McpWorkbench(playwright_server_params)


    async with jira_workbench as jira_wb, playwright_workbench as playwright_wb:
        custom_model_capabilities = ModelInfo(
            json_output=True,  # Set to True if it supports processing audio
            function_calling=True,
            vision=True
        )
        ollama_model_client = OllamaChatCompletionClient(model="llama3.2", model_capabilities=custom_model_capabilities)

        Jira_Analyst = AssistantAgent(name="Jira_Agent", model_client=ollama_model_client, workbench=jira_wb,
                            system_message=())

        playwright_automation_analyst =AssistantAgent(name="AutomationAgent",model_client=ollama_model_client, workbench=playwright_wb,
                                            system_message=() )

        agent_team = RoundRobinGroupChat(participants=[Jira_Analyst, playwright_automation_analyst],
                            termination_condition=TextMentionTermination('TESTING COMPLETED'))

        await Console(agent_team.run_stream(task=""))

        await ollama_model_client.close()

asyncio.run(main())
