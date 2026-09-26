import sqlite3

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

DB_PATH = "todos.db"


class Todo(BaseModel):
    id: int
    title: str
    description: str
    completed: bool
    category: str


def get_connection():
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def initialize_database():
    connection = get_connection()

    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS todos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT NOT NULL,
            completed INTEGER NOT NULL DEFAULT 0,
            category TEXT NOT NULL DEFAULT 'General'
        )
        """
    )

    # Only seed sample data the first time the table is created.
    existing = connection.execute("SELECT COUNT(*) FROM todos").fetchone()[0]
    if existing == 0:
        sample_todos = [
            # Morning
            ("Review maintenance tasks and priorities for the day", "Check today's work orders and rank them", 1, "Morning"),
            ("Check and respond to important emails", "Clear anything urgent before the day gets busy", 1, "Morning"),
            ("Spend 15 minutes learning French vocabulary", "Short daily vocab session", 1, "Morning"),
            ("Read one industry article", "Maintenance, safety, or project management topic", 1, "Morning"),

            # During Work
            ("Follow up on pending maintenance requests", "Check status of open work orders", 1, "During Work"),
            ("Update maintenance records and documentation", "Keep logs current for the day's work", 1, "During Work"),
            ("Identify one process improvement opportunity", "Something that could run more efficiently", 1, "During Work"),
            ("Network with at least one colleague or stakeholder", "A short conversation counts", 1, "During Work"),

            # Evening
            ("Complete 30-60 minutes of professional learning", "PMP (Mon/Wed/Fri), French (Tue/Thu), Web dev (Sat), Career/LinkedIn (Sun)", 1, "Evening"),
            ("Exercise or take a 30-minute walk", "Movement before winding down", 1, "Evening"),
            ("Plan priorities for the next day", "Set tomorrow's top three tasks", 1, "Evening"),

            # Weekly - Monday
            ("Review weekly goals and work schedule", "Set the tone for the week ahead", 0, "Monday"),
            ("Prioritize maintenance projects", "Rank projects for the week", 0, "Monday"),

            # Weekly - Tuesday
            ("Study PMP project management concepts", "Continue PMP prep material", 0, "Tuesday"),
            ("Update CV or LinkedIn if needed", "Keep profile current", 0, "Tuesday"),

            # Weekly - Wednesday
            ("Learn a new maintenance or reliability engineering concept", "One new concept this week", 0, "Wednesday"),
            ("Follow up on ongoing projects", "Check progress on active projects", 0, "Wednesday"),

            # Weekly - Thursday
            ("French speaking and listening practice", "Focused practice session", 0, "Thursday"),
            ("Read safety management material", "Safety-focused reading", 0, "Thursday"),

            # Weekly - Friday
            ("Review achievements for the week", "Note what got done", 0, "Friday"),
            ("Prepare next week's work plan", "Draft the plan for next week", 0, "Friday"),

            # Weekly - Saturday
            ("Continue HTML, CSS, and JavaScript learning with Databloom", "Databloom Future Code coursework", 0, "Saturday"),
            ("Build a small practice project", "Apply what was learned this week", 0, "Saturday"),

            # Weekly - Sunday
            ("Family and personal time", "Unplug from work", 0, "Sunday"),
            ("Review finances and investments", "Check accounts and investments", 0, "Sunday"),
            ("Plan the upcoming week", "Set the week ahead", 0, "Sunday"),
        ]
        connection.executemany(
            "INSERT INTO todos (title, description, completed, category) VALUES (?, ?, ?, ?)",
            sample_todos,
        )

    connection.commit()
    connection.close()


app = FastAPI()

# Allows the frontend (served from a different origin/port) to call this API.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

initialize_database()


@app.get("/")
def home():
    return {"message": "Todo API is running"}


@app.get("/todos")
def get_todos():
    connection = get_connection()
    cursor = connection.execute("SELECT * FROM todos")
    rows = cursor.fetchall()
    connection.close()

    todos = [Todo(id=row["id"], title=row["title"], description=row["description"],
                  completed=bool(row["completed"]), category=row["category"]) for row in rows]
    return todos
