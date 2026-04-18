from langgraph.graph import StateGraph
from typing import TypedDict
from llm import route_with_gemini
from tools import create_task, schedule_event, save_note, query_data

# --- State ---
class State(TypedDict):
    input: str
    decision: str
    output: str

# --- Router ---
def router(state):
    decision = route_with_gemini(state["input"])
    return {"decision": decision}

# --- Nodes ---
def task_node(state):
    return {"output": create_task("Task", "tomorrow")}

def calendar_node(state):
    return {"output": schedule_event("Meeting", "10AM")}

def notes_node(state):
    return {"output": save_note(state["input"])}

def data_node(state):
    return {"output": query_data("SELECT * FROM table")}

# --- Build Graph ---
builder = StateGraph(State)

builder.add_node("router", router)
builder.add_node("task", task_node)
builder.add_node("calendar", calendar_node)
builder.add_node("notes", notes_node)
builder.add_node("data", data_node)

builder.set_entry_point("router")

builder.add_conditional_edges(
    "router",
    lambda x: x["decision"],
    {
        "task": "task",
        "calendar": "calendar",
        "notes": "notes",
        "data": "data",
    }
)

# ✅ THIS is what main.py is trying to import
graph = builder.compile()