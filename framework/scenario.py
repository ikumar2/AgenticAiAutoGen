import asyncio

from autogen_agentchat.conditions import TextMentionTermination
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.ui import Console
from autogen_core.models import ModelInfo
from autogen_ext.models.ollama import OllamaChatCompletionClient

from framework.agentFactory import AgentFactory


async def main():
    custom_model_capabilities = ModelInfo(
        json_output=True,  # Set to True if it supports processing audio
        function_calling=True,
        vision=True
    )
    model_client = OllamaChatCompletionClient(model="llama3.2", model_capabilities=custom_model_capabilities)
    factory = AgentFactory(model_client)

    automation_test_agent = factory.Build_Automation_Test(system_message="""
                                                         Act as System Analyst and read the scenario and build Test cases with detailed steps with the help of file_handler_agent as per provided scenario in /framework/Data/Scenarios_for_build file.  .
                                                         
                                                         Your Task:
                                                         "Read the file Scenarios_for_build using the tool 'file_handler_agent'. Call the tool and read the file"
                                                         "Build the detailed Test cases with steps for Smoke Testing as per each scenarios "
                                                         "Write the scenario in Data directory file 'Final_Scenarios using tools file_handler_agent. Call the tool and read write the file"
                                                         "Once done with writing detailed Test cases in framwork -> Data -> Final_Scenario then provide the detailed steps to 'AutomationAgent' for automating those steps "
                                                                       "When detailed steps are ready - automation_agent should proceed next """)

    file_handler_agent = factory.File_handler_agent(system_message="Act as expert in file system to read and write file from Data folder as exist in framework.")

    automation_agent = factory.Automation_agent(system_message="Act as automation expert and perform the all action as per step by step"
                                                               "Take the all stepped scenarios from 'automation_test_agent'."
                                                "Navigate to website. "
                                                "Look for all available links. "
                                                "Search and click if requested "
                                                "Utilize the wait to wait for page load or all element visible and changing the color or state of button or link. "
                                                "If needed further any information go back to 'scenario_build_agent' and get the detail. " )

    agent_team = RoundRobinGroupChat(participants=[automation_test_agent, file_handler_agent, automation_agent],
                                     termination_condition=TextMentionTermination('TASK COMPLETED'))

    task_result = await Console(agent_team.run_stream(task="Connected to automation_test_agent and build the detailed steps to test as per scenario provided in Scenarios_for_build and write down in Final_Scenarios file. "
                                                           "Provide to automation_agent to automate detail step" ))

    await model_client.close()

asyncio.run(main())