from autogen_ext.tools.mcp import StdioServerParams, McpWorkbench

from utils.FileHelper import get_project_path


class McpConfig:

    def __init__(self):
        pass

    def get_automation_agent(self):
        playwright_server_params=StdioServerParams(command="npx",
                                                     args=["@playwright/mcp@latest"
                                                           ])
        return McpWorkbench(server_params=playwright_server_params)

    def file_handler_agent(self):
        file_store_path = str(get_project_path('Data'))  # As tool by default read and write on root level so to making under Data need to touch code of fileserver.
        filesystem_server_params = StdioServerParams(command="npx",
                                                     args=["-y",
                                                           "@modelcontextprotocol/server-filesystem",
                                                           file_store_path],
                                                     read_timeout_seconds=60)
        return McpWorkbench(filesystem_server_params)

