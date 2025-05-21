from fastmcp import Client
from fastmcp.exceptions import ToolError
from fastmcp.utilities.mcp_config import MCPConfig
from mcp.types import TextContent


class MCPClient:
    def __init__(self, config: MCPConfig):
        self.config = config
        self.client = Client(config)

    async def list_tools(self) -> str:
        """
        List all tools available in the MCP server.
        """
        tools = await self.client.list_tools()
        descriptions = "Available tools:\n"
        for tool in tools:
            descriptions += f"## {tool.name}\n### {tool.description}\n\n"

        return descriptions

    async def call_tool(
        self,
        tool_name: str,
        inputs: dict[str, str],
    ) -> str:
        """
        Call a specific tool with the given inputs.
        """
        try:
            resp = await self.client.call_tool(tool_name, inputs)
        except ToolError as e:
            return f"Error: calling tool {tool_name} with the following arguments:\n{inputs}\n\nError:\n{str(e)}"

        if isinstance(resp, TextContent):
            return resp.text
        else:
            return "The tool did not return a text response. But Conflux can only handle text responses. Please check the tool's response type."
