# MCP Multi-Agent Assistant

## Overview
This project is an advanced, multi-agent AI system designed to coordinate smaller sub-agents and execute complex workflows. By integrating directly with the Model Context Protocol (MCP), the agent acts as an autonomous personal assistant, securely navigating and managing tools such as a Task Manager, Calendar, and Notebook. 

When given a multi-step prompt (e.g., *"Read my notes and schedule a meeting based on what you find"*), the primary agent applies logical chain-of-thought to coordinate tasks, call the respective backend tools sequentially, and store the output.

## Technologies Used
* **Google Agent Development Kit (ADK):** The core multi-agent framework managing orchestration, memory, and state.
* **Gemini 2.5 Flash (`google-genai`):** The LLM brain fueling the logical decision-making process.
* **Model Context Protocol (MCP) / FastMCP:** Standardized A2A (Agent-to-App) tool-calling server. 
* **SQLite:** A lightweight RDBMS simulating AlloyDB structures for secure native storage.
* **FastAPI:** Operates under the hood to deploy the seamless Interactive Web UI and agent execution endpoints.

## How It Works
1. **The Tool Server:** Our local `mcp_server.py` operates as an isolated execution environment, exposing native python CRUD database functions as standardized API tools to the core agent.
2. **The Graph:** When the user poses a question, the primary ADK agent queries the MCP server's schemas to determine which tools are required to fulfill the request.
3. **Execution:** The agent dynamically bridges intent with the database, orchestrating multiple interactions sequentially in the background to return a completed outcome to the user.

## How to Run It

### 1. Requirements Setup
Make sure to create a `.env` file at the root of the directory with your API key:
```env
GEMINI_API_KEY=your_key_here
```
Install the necessary dependencies utilizing Python:
```bash
pip install -r requirements.txt
```

### 2. Launch the Application
Start the ADK framework server via the command-line:

**To deploy the interactive Web UI (Recommended):**
```bash
adk web .
```
Navigate to `http://127.0.0.1:8000` to interact with your Agent directly!

**To use the terminal-based interactive CLI:**
```bash
adk run .
```
