from autogen_agentchat.agents import AssistantAgent

from framework.mcp_config import McpConfig


class AgentFactory:

    def __init__(self,model_client):
        self.model_client= model_client
        self.mcp_config = McpConfig()


    def File_handler_agent(self,system_message):
        file_handler_agent = AssistantAgent(name="FileHandlerAgent", model_client=self.model_client,
                                workbench=self.mcp_config.file_handler_agent(),
                                system_message=system_message)
        return file_handler_agent

    def Automation_agent(self,system_message):
        automation_agent = AssistantAgent(name="AutomationAgent", model_client=self.model_client,
                                workbench=self.mcp_config.get_automation_agent(),
                                system_message=system_message)
        return automation_agent

    def Build_Automation_Test(self,system_message):
        automation_test_agent = AssistantAgent(name="AutomationTestAgent", model_client=self.model_client,
                                system_message=system_message)
        return automation_test_agent