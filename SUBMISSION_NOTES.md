# Submission Notes

## HTML elements identified from the reference image
- A header bar containing a profile icon, my name, and the page heading "My Todo List"
- A list of todo items, each shown as a rounded card with a title, a description,
  and a circular checkbox: empty for incomplete, filled with a checkmark for completed
- A container (`#todo-list`) that JavaScript populates dynamically

## Frontend challenges
- Matching the reference image's hand-drawn card style: solved by loading the "Kalam"
  Google Font for the card text, and using a circular `div` with an inline SVG checkmark
  that's only shown (`display: block`) when the item has the `completed` class.
- Making the completed/incomplete difference readable at a glance rather than a small
  icon: added a green-filled checkbox plus strikethrough, greyed-out text for completed
  items, versus an amber-outlined empty circle and full-strength text for incomplete ones,
  so the distinction doesn't rely on noticing one small detail.
- Keeping the layout usable at narrow widths: added a media query that stacks the header
  (profile above title instead of side by side) and shrinks card padding/font size below
  480px.

## Backend challenges
- SQLite stores booleans as 0/1, not `True`/`False`, so the `completed` value has to be
  cast with `bool()` when building the Pydantic `Todo` objects, otherwise the API would
  return `0`/`1` instead of proper JSON booleans.
- CORS: the browser blocked `fetch()` calls to the backend from the frontend's own origin
  until `CORSMiddleware` was added to `main.py`.
- Port 8000 was already in use on my machine, so I ran the server on 8001 instead
  (`--port 8001`), and matched `API_BASE` in `script.js` to the same port.
- **Stale database schema**: after adding a `category` field to the `Todo` model and the
  `CREATE TABLE` statement, `GET /todos` started returning a 500 Internal Server Error.
  The cause was that `CREATE TABLE IF NOT EXISTS` doesn't retroactively add a new column
  to a `todos.db` file that already existed from an earlier run — the old file still had
  the original 4-column structure, so `row["category"]` failed. Fixed by deleting the
  stale `todos.db` so it got rebuilt fresh with the current schema on the next startup.

## Environment / tooling challenges (Windows-specific)
- `uv run fastapi dev main.py` and `uv run uvicorn main:app --reload` both failed with
  `Failed to spawn: Access is denied (os error 5)`. Testing showed the problem wasn't
  fastapi or uvicorn specifically — every generated `.exe` wrapper in `.venv\Scripts`
  was being blocked from running, most likely by endpoint security software on a
  managed machine. `python.exe` itself ran fine, so the fix was to bypass the wrapper
  entirely and run uvicorn as a Python module instead:
  `uv run python -m uvicorn main:app --reload --port 8001`
- Had an activated manual `venv` folder at the same time uv was managing its own
  `.venv` for the project, which produced a `VIRTUAL_ENV does not match` warning and
  meant commands could pick up the wrong (empty) environment. Resolved by running
  `deactivate` and letting uv manage its own `.venv` exclusively.
- `uvicorn`/`fastapi` commands must be run from the exact folder containing `main.py`
  (`Assessment/backend`) — running them from a different working directory produced
  `Error loading ASGI app. Could not import module "main"`.

## How I investigated/fixed them
- Used the FastAPI docs page at `/docs` to test `GET /todos` directly and read the full
  error response (which showed `Internal Server Error` for the schema bug) before
  touching the frontend at all.
- Isolated the Windows spawn error by testing `fastapi`, then `uvicorn`, then running
  `python.exe` directly — narrowing it down from "some project problem" to "every exe
  wrapper in this venv is blocked" by process of elimination.
- Checked the terminal's live request log (`GET /todos ... 500`) to confirm exactly
  which request was failing and when, rather than guessing.

## How data moves from SQLite to FastAPI to the browser
1. `initialize_database()` creates the `todos` table (if it doesn't exist) and seeds
   sample rows on first run.
2. `GET /todos` opens a connection, runs `SELECT * FROM todos`, and gets back
   `sqlite3.Row` objects.
3. Each row is converted into a `Todo` Pydantic model, which FastAPI automatically
   serializes into a JSON array in the response.
4. `script.js` calls `fetch("http://127.0.0.1:8001/todos")`, parses the JSON with
   `.json()`, and loops through it, building a `<div class="todo-item">` per todo with
   `createElement`/`textContent`, then appending each one into `#todo-list`.

## Bonus questions
- **When a POST request is sent, is the item automatically stored in the database?**
  No — a POST endpoint has to explicitly run an `INSERT` SQL statement and commit it;
  sending the request alone does nothing without backend code to handle it.
- **What must the backend do before the new todo becomes permanent?** Execute a
  parameterized `INSERT` and call `connection.commit()` (SQLite only writes to disk on
  commit).
- **After creating a todo, how would you make it appear on the page?** Either re-fetch
  the full list from `GET /todos` and re-render, or take the created todo returned by
  the POST response and append just that one element to `#todo-list`.
- **How would you avoid displaying thousands of todo items at once?** Add pagination or
  a `LIMIT`/`OFFSET` to the SQL query, and only fetch the next page as the user scrolls
  or clicks "load more".
- **What should the frontend send when a todo is marked complete?** The todo's `id` and
  the new `completed` value, sent to a `PUT`/`PATCH` endpoint that runs an
  `UPDATE ... WHERE id = ?` query.
- **Why use parameters instead of placing values directly in the query string?** To
  prevent SQL injection — untrusted input placed directly into a query string can be
  crafted to alter the query's meaning; parameters are always treated as data, never as
  SQL code.
