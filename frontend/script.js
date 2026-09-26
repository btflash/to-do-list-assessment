const todoListElement = document.getElementById("todo-list");

const todos = [{
        id: 1,
        title: "Review maintenance tasks and priorities for the day",
        description: "Check today's work orders and rank them",
        completed: true,
    },
    {
        id: 2,
        title: "Follow up on pending maintenance requests",
        description: "Check status of open work orders",
        completed: false,
    },
    {
        id: 3,
        title: "Update maintenance records and documentation",
        description: "Keep logs current for the day's work",
        completed: true,
    },
    {
        id: 4,
        title: "Complete 30-60 minutes of professional learning",
        description: "PMP (Mon/Wed/Fri), French (Tue/Thu), Web dev (Sat), Career/LinkedIn (Sun)",
        completed: false,
    },
    {
        id: 5,
        title: "Plan priorities for the next day",
        description: "Set tomorrow's top three tasks",
        completed: true,
    },
];

const CHECK_ICON = `
  <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
    <path d="M4 12.5L9.5 18L20 6" stroke="#2B2B28" stroke-width="2.5"
          stroke-linecap="round" stroke-linejoin="round"/>
  </svg>
`;

function createTodoElement(todo, index) {
    const item = document.createElement("div");
    item.className = "todo-item";
    if (todo.completed) item.classList.add("completed");
    if (index % 2 === 1) item.classList.add("alt");

    const text = document.createElement("div");
    text.className = "todo-text";

    const title = document.createElement("h3");
    title.className = "todo-title";
    title.textContent = todo.title;

    const description = document.createElement("p");
    description.className = "todo-description";
    description.textContent = todo.description;

    text.appendChild(title);
    text.appendChild(description);

    const checkbox = document.createElement("div");
    checkbox.className = "todo-checkbox";
    checkbox.innerHTML = CHECK_ICON;

    item.appendChild(text);
    item.appendChild(checkbox);

    return item;
}

function renderTodos(todoArray) {
    todoListElement.innerHTML = "";
    todoArray.forEach((todo, index) => {
        todoListElement.appendChild(createTodoElement(todo, index));
    });
}

renderTodos(todos);

// --- Backend version (for the FastAPI/SQLite assignment submission) ---
// Once the backend is running (uv run fastapi dev main.py), swap the
// line above for the fetch below to load todos from /todos instead
// of this hardcoded array:
//
// const API_BASE = "http://127.0.0.1:8000";
// fetch(`${API_BASE}/todos`)
//   .then((response) => response.json())
//   .then((data) => renderTodos(data))
//   .catch((error) => {
//     console.error("Failed to load todos:", error);
//     todoListElement.textContent = "Could not load todos. Is the backend running?";
//   });