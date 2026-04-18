import sys
import asyncio
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.prebuilt import create_react_agent
from mcp.client.session import ClientSession
from mcp.client.stdio import stdio_client, StdioServerParameters
from langchain_mcp_adapters.tools import load_mcp_tools

load_dotenv()

async def main():
    print("Loading LLM and connecting to MCP Database tools...")
    llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash")
    
    # Connect directly to our existing mcp_server.py
    server_params = StdioServerParameters(
        command=sys.executable,
        args=["assistant/mcp_server.py"]
    )
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # Initialize connection to FastMCP Server
            await session.initialize()
            
            # Map exposed FastMCP operations into LangChain compatible tool nodes
            tools = await load_mcp_tools(session)
            
            # Compile our LangGraph framework agent
            agent = create_react_agent(llm, tools)
            
            print("\n=============================================")
            print("   LangGraph MCP Agent CLI Ready!  ")
            print("=============================================")
            print("Type 'quit' or 'exit' to terminate the session.")
            
            while True:
                user_msg = input("\nYou: ")
                if user_msg.lower() in ("quit", "exit"):
                    break
                    
                input_msg = {"messages": [("user", user_msg)]}
                
                print("\n=============================================")
                # Stream the LangGraph execution steps iteratively
                async for event in agent.astream(input_msg, stream_mode="values"):
                    message = event["messages"][-1]
                    # Print the output from the Agent or Tool
                    message.pretty_print()
                print("=============================================\n")

if __name__ == "__main__":
    asyncio.run(main())
