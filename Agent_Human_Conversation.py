import asyncio

from autogen_agentchat.agents import AssistantAgent, UserProxyAgent
from autogen_agentchat.conditions import TextMentionTermination
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.ui import Console
from autogen_ext.models.ollama import OllamaChatCompletionClient


async def main():
    ollama_model_client = OllamaChatCompletionClient(model="llama3.2")
    assistant = AssistantAgent(name="MathTutor", model_client= ollama_model_client,
                   system_message="you are helpful math tutor. Help the user to solve math problems step by step."
                                  "When user says 'Thanks Done' or 'Bye' or similar, acknowledge and say 'LESSON COMPLETED'")
    user_proxy= UserProxyAgent(name="student")
    team = RoundRobinGroupChat(participants=[user_proxy,assistant],
                        termination_condition=TextMentionTermination("LESSON COMPLETED"))
    await Console(team.run_stream(task='I need help with algebra problem can you help me solve 2*4*6'))
    await ollama_model_client.close()
asyncio.run(main())