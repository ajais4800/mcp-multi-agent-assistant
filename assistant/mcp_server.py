from mcp.server.fastmcp import FastMCP
import database

# Initialize the db to ensure tables exist
database.init_db()

mcp = FastMCP("PersonalAssistantDataMcpServer")

@mcp.tool()
def add_task(title: str, description: str, due_date: str) -> str:
    """Add a new task to the task manager. Provide a concise title, a brief description, and a due date (e.g. YYYY-MM-DD or tomorrow)."""
    return database.add_task(title, description, due_date)

@mcp.tool()
def list_tasks() -> str:
    """List all tasks in the task manager."""
    return database.list_tasks()

@mcp.tool()
def schedule_event(title: str, event_datetime: str, location: str = "") -> str:
    """Schedule an event in the calendar. Provide an event title, the date and time, and optional location."""
    return database.schedule_event(title, event_datetime, location)

@mcp.tool()
def list_events() -> str:
    """List all scheduled calendar events."""
    return database.list_events()

@mcp.tool()
def save_note(content: str) -> str:
    """Save a piece of information or note for later retrieval."""
    return database.save_note(content)

@mcp.tool()
def list_notes() -> str:
    """List all saved notes."""
    return database.list_notes()

if __name__ == "__main__":
    print("Starting MCP Server...")
    mcp.run()
