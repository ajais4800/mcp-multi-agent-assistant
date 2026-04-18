import streamlit as st
import asyncio
import sys
import threading
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import HumanMessage, AIMessage
from mcp.client.session import ClientSession
from mcp.client.stdio import stdio_client, StdioServerParameters
from langchain_mcp_adapters.tools import load_mcp_tools

load_dotenv()

st.set_page_config(page_title="Multi-agent-assistant", page_icon="🤖")
st.title("🤖 Multi-agent-assistant")
st.markdown("I manage your tasks, schedule, and notes completely autonomously by securely connecting to the FastMCP toolkit.")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history — hide ToolMessages and raw metadata
for msg in st.session_state.messages:
    if isinstance(msg, HumanMessage):
        st.chat_message("user").write(msg.content)
    elif isinstance(msg, AIMessage) and msg.content:
        content_str = ""
        if isinstance(msg.content, list):
            texts = []
            for part in msg.content:
                if isinstance(part, str):
                    texts.append(part)
                elif isinstance(part, dict) and "text" in part:
                    texts.append(part["text"])
            content_str = "\n".join(texts)
        else:
            content_str = str(msg.content)

        if content_str.strip():
            st.chat_message("assistant").markdown(content_str)

async def run_agent(messages_history):
    server_params = StdioServerParameters(
        command=sys.executable,
        args=["assistant/mcp_server.py"]
    )
    llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash")

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            tools = await load_mcp_tools(session)
            agent = create_react_agent(llm, tools)
            response_state = await agent.ainvoke({"messages": messages_history})
            return response_state["messages"]

def run_in_thread(messages_history):
    """Run the async agent in a brand new isolated thread with its own event loop.
    This avoids anyio TaskGroup conflicts with Streamlit's existing event loop."""
    result = {}
    def thread_target():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            result["messages"] = loop.run_until_complete(run_agent(messages_history))
        except Exception as e:
            result["error"] = e
        finally:
            loop.close()

    t = threading.Thread(target=thread_target)
    t.start()
    t.join()

    if "error" in result:
        raise result["error"]
    return result["messages"]

# User Input
if prompt := st.chat_input("Ask me to manage your schedule or lookup a note..."):
    st.chat_message("user").write(prompt)
    user_msg = HumanMessage(content=prompt)
    st.session_state.messages.append(user_msg)

    with st.spinner("Thinking..."):
        try:
            updated_messages = run_in_thread(st.session_state.messages)
            st.session_state.messages = updated_messages
            st.rerun()
        except Exception as e:
            st.error(f"Error: {e}")
