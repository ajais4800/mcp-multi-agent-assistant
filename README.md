# Multi-agent-assistant: LangGraph & MCP Powered AI Orchestrator

## Overview
**Multi-agent-assistant** is a production-ready, autonomous AI system that leverages **LangGraph** to coordinate specialized tool-calling workflows. By integrating with the **Model Context Protocol (MCP)**, the agent securely interacts with local data sources and tools, such as a task manager, calendar, and notebook, to solve multi-step user requests with extreme reliability.

Instead of simple one-off responses, this assistant uses a **ReAct (Reason + Act)** loop to autonomously decide which tools to use, how to sequence them, and how to verify the results before responding to the user.

## Key Features
*   **Autonomous Orchestration:** Powered by **LangGraph**, enabling complex cyclic workflows and robust state management.
*   **A2A Tooling:** Implements the **Model Context Protocol (MCP)** via **FastMCP** for standardized, secure agent-to-app communication.
*   **Unified Memory:** Seamlessly manages tasks, events, and notes in a local **SQLite** database.
*   **Premium Web UI:** A clean, responsive chat interface built with **Streamlit** that hides technical complexity and provides a sleek user experience.

## Technologies Used
*   **Core Logic:** [LangGraph](https://github.com/langchain-ai/langgraph) (Orchestration & State Management)
*   **LLM Brain:** [Gemini 2.0 Flash](https://ai.google.dev/gemini-api) (Advanced logical reasoning)
*   **Interface:** [Streamlit](https://streamlit.io/) (Premium Web Chat UI)
*   **Protocol:** [Model Context Protocol (MCP)](https://modelcontextprotocol.io/) (Standardized tool-calling)
*   **Database:** SQLite (Relational storage for notes, tasks, and events)
*   **Async Bridge:** `nest_asyncio` & `asyncio` for high-performance concurrent task execution.

## How to Run Locally

### 1. Environment Setup
Create a `.env` file in the root directory:
```env
GEMINI_API_KEY=your_gemini_api_key_here
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Launch the Web UI
The main interface is powered by Streamlit:
```bash
python -m streamlit run assistant/web_ui.py
```
Automatically opens at `http://localhost:8501`.

### 4. Terminal CLI (Alternative)
For raw terminal interaction:
```bash
python assistant/main_cli.py
```

## Deployment
This application is container-ready. To deploy it to **Google Cloud Run**:
1.  Build a Docker image containing the code and dependencies.
2.  Deploy to Cloud Run with the `GEMINI_API_KEY` mapped as a secret.
3.  Use a persistence layer like **Google Cloud SQL (PostgreSQL)** if you wish to migrate from local SQLite to cloud storage.
