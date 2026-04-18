import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "app.db")

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    # Tasks table
    c.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            due_date TEXT,
            status TEXT DEFAULT 'pending'
        )
    ''')
    # Events table
    c.execute('''
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            event_datetime TEXT NOT NULL,
            location TEXT
        )
    ''')
    # Notes table
    c.execute('''
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def add_task(title: str, description: str, due_date: str) -> str:
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO tasks (title, description, due_date) VALUES (?, ?, ?)", 
              (title, description, due_date))
    task_id = c.lastrowid
    conn.commit()
    conn.close()
    return f"Task '{title}' added with ID {task_id}."

def list_tasks() -> str:
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT id, title, description, due_date, status FROM tasks")
    rows = c.fetchall()
    conn.close()
    if not rows:
        return "No tasks found."
    return "\n".join([f"[{r[0]}] {r[1]} (Due: {r[3]}) - {r[4]}: {r[2]}" for r in rows])

def schedule_event(title: str, event_datetime: str, location: str = "") -> str:
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO events (title, event_datetime, location) VALUES (?, ?, ?)", 
              (title, event_datetime, location))
    event_id = c.lastrowid
    conn.commit()
    conn.close()
    return f"Event '{title}' scheduled at {event_datetime} with ID {event_id}."

def list_events() -> str:
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT id, title, event_datetime, location FROM events ORDER BY event_datetime ASC")
    rows = c.fetchall()
    conn.close()
    if not rows:
        return "No events scheduled."
    return "\n".join([f"[{r[0]}] {r[1]} at {r[2]} (Location: {r[3]})" for r in rows])

def save_note(content: str) -> str:
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO notes (content) VALUES (?)", (content,))
    note_id = c.lastrowid
    conn.commit()
    conn.close()
    return f"Note saved with ID {note_id}."

def list_notes() -> str:
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT id, content, timestamp FROM notes ORDER BY timestamp DESC")
    rows = c.fetchall()
    conn.close()
    if not rows:
        return "No notes found."
    return "\n".join([f"[{r[0]}] {r[2]}: {r[1]}" for r in rows])

if __name__ == "__main__":
    init_db()
    print("Database initialized.")
