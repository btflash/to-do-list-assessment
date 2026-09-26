const API_BASE = "http://127.0.0.1:8001";

const todoListElement = document.getElementById("todo-list");

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

function loadTodos() {
    fetch(`${API_BASE}/todos`)
        .then((response) => response.json())
        .then((todos) => {
            renderTodos(todos);
        })
        .catch((error) => {
            console.error("Failed to load todos:", error);
            todoListElement.textContent = "Could not load todos. Is the backend running?";
        });
}

loadTodos();