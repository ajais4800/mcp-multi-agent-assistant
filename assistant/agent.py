import os
import sys
from google.adk.agents import Agent
from google.adk.tools.mcp_tool import MCPToolset, StdioConnectionParams
from mcp.client.stdio import StdioServerParameters

server_script = os.path.join(os.path.dirname(__file__), "mcp_server.py")
server_params = StdioServerParameters(command=sys.executable, args=[server_script])

mcp_toolset = MCPToolset(
    connection_params=StdioConnectionParams(server_params=server_params)
)

root_agent = Agent(
    model='gemini-2.5-flash',
    name='PrimaryAssistantAgent',
    instruction="""
    You are a highly capable multi-agent orchestrator. 
    You have tools to manage tasks, calendar events, and notes.
    If the user asks for multi-step tasks (e.g. "read my notes and schedule an event for tomorrow based on them"),
    you should strategically break down the steps and call the tools sequentially.
    """,
    tools=[mcp_toolset]
)

if __name__ == "__main__":
    print("Agent is ready.")
