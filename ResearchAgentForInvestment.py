import asyncio

from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.conditions import MaxMessageTermination, TextMentionTermination
from autogen_agentchat.teams import SelectorGroupChat
from autogen_agentchat.ui import Console
from autogen_ext.models.ollama import OllamaChatCompletionClient


async  def main():
    ollama_model_client = OllamaChatCompletionClient(model="llama3.2-vision")
    researcher = AssistantAgent (
        "ResearcherAgent",
        model_client=ollama_model_client,
        system_message="You are a researcher. Your role is to gather information and provide research finding. " 
                         "Do not write articles or create content -> Just provide research data and facts."
    )

    writer = AssistantAgent(
        "WriterAgent",
        model_client=ollama_model_client,
        system_message= "You are a writer. Your role is to take research information and "
                        "create well-written articles. Wait for research to provide, then write the content."
    )
    critic = AssistantAgent(
        "CriticAgent",
        model_client=ollama_model_client,
        system_message="You are a critic. Review written content and provide feedback. "
                       "Say 'TERMINATE' when satisfied with final result"

    )
    text_termination = TextMentionTermination("TERMINATE")
    max_message_termination= MaxMessageTermination(max_messages=15)

    termination = text_termination | max_message_termination

    team = SelectorGroupChat(participants=[critic,writer,researcher],
                      model_client= ollama_model_client, termination_condition=termination ,
                      allow_repeated_speaker=True)

    await Console(team.run_stream(task = "Research renewable energy tends future impact and write a brief summary which renewable company should i invest and why? what would be return in 3 month and 6 month"))
    await ollama_model_client.close()
asyncio.run(main())