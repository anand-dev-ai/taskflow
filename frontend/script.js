const API_BASE_URL = "http://127.0.0.1:8000";

const taskForm = document.getElementById("task-form");
const titleInput = document.getElementById("title");
const priorityInput = document.getElementById("priority");
const dueDateInput = document.getElementById("due-date");
const projectIdInput = document.getElementById("project-id");

const titleError = document.getElementById("title-error");
const taskList = document.getElementById("task-list");
const taskCount = document.getElementById("task-count");
const loadingMessage = document.getElementById("loading-message");
const submitButton = document.getElementById("submit-button");

const CACHE_KEY = "taskflow_tasks";

let tasks = [];
let editingTaskId = null;


// ------------------------------------
// Local storage
// ------------------------------------

function saveTasksToCache() {
    localStorage.setItem(CACHE_KEY, JSON.stringify(tasks));
}

function loadTasksFromCache() {
    const cachedTasks = localStorage.getItem(CACHE_KEY);

    if (!cachedTasks) {
        return [];
    }

    try {
        return JSON.parse(cachedTasks);
    } catch (error) {
        console.error("Could not parse cached tasks:", error);
        return [];
    }
}


// ------------------------------------
// Render tasks
// ------------------------------------

function renderTasks() {
    taskList.replaceChildren();

    taskCount.textContent =
        `${tasks.length} task${tasks.length === 1 ? "" : "s"}`;

    if (tasks.length === 0) {
        const emptyMessage = document.createElement("p");
        emptyMessage.className = "empty-message";
        emptyMessage.textContent = "No tasks found.";
        taskList.appendChild(emptyMessage);
        return;
    }

    tasks.forEach((task) => {
        const taskItem = document.createElement("article");
        taskItem.className = "task-item";

        const title = document.createElement("h3");
        title.textContent = task.title;

        const details = document.createElement("div");
        details.className = "task-details";

        const priorityBadge = document.createElement("span");
        priorityBadge.className =
            `task-badge priority-${task.priority}`;
        priorityBadge.textContent =
            `Priority: ${task.priority}`;

        const dueDateBadge = document.createElement("span");
        dueDateBadge.className = "task-badge";
        dueDateBadge.textContent =
            `Due: ${task.due_date || "Not specified"}`;

        const projectBadge = document.createElement("span");
        projectBadge.className = "task-badge";
        projectBadge.textContent =
            `Project: ${task.project_id}`;

        details.appendChild(priorityBadge);
        details.appendChild(dueDateBadge);
        details.appendChild(projectBadge);

        const actions = document.createElement("div");
        actions.className = "task-actions";

        const editButton = document.createElement("button");
        editButton.type = "button";
        editButton.className = "edit-button";
        editButton.textContent = "Edit";

        editButton.addEventListener("click", () => {
            startEditingTask(task);
        });

        const deleteButton = document.createElement("button");
        deleteButton.type = "button";
        deleteButton.className = "delete-button";
        deleteButton.textContent = "Delete";

        deleteButton.addEventListener("click", () => {
            deleteTask(task.id);
        });

        actions.appendChild(editButton);
        actions.appendChild(deleteButton);

        taskItem.appendChild(title);
        taskItem.appendChild(details);
        taskItem.appendChild(actions);

        taskList.appendChild(taskItem);
    });
}


// ------------------------------------
// Validation
// ------------------------------------

function validateTitle() {
    const trimmedTitle = titleInput.value.trim();

    if (!trimmedTitle) {
        titleError.textContent = "Title cannot be blank.";
        return false;
    }

    titleError.textContent = "";
    return true;
}

titleInput.addEventListener("input", () => {
    if (titleInput.value.trim()) {
        titleError.textContent = "";
    }
});


// ------------------------------------
// Load tasks from backend
// ------------------------------------

async function loadTasksFromBackend() {
    loadingMessage.textContent = "Loading tasks from server...";

    try {
        const response = await fetch(`${API_BASE_URL}/tasks`);

        if (!response.ok) {
            throw new Error(`HTTP error: ${response.status}`);
        }

        tasks = await response.json();

        saveTasksToCache();
        renderTasks();

        loadingMessage.textContent = "";
    } catch (error) {
        console.error("Failed to load tasks:", error);

        loadingMessage.textContent =
            "Could not connect to the backend. Showing cached tasks.";
    }
}


// ------------------------------------
// Add task
// ------------------------------------

async function addTask() {
    const response = await fetch(`${API_BASE_URL}/tasks`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            title: titleInput.value.trim(),
            priority: priorityInput.value,
            due_date: dueDateInput.value.trim() || null,
            project_id: Number(projectIdInput.value)
        })
    });

    if (!response.ok) {
        const errorData = await response.json();
        throw new Error(
            errorData.detail
                ? JSON.stringify(errorData.detail)
                : `HTTP error: ${response.status}`
        );
    }

    const createdTask = await response.json();

    tasks.push(createdTask);

    saveTasksToCache();
    renderTasks();
}


// ------------------------------------
// Update task
// ------------------------------------

async function updateTask(taskId) {
    const response = await fetch(
        `${API_BASE_URL}/tasks/${taskId}`,
        {
            method: "PUT",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                title: titleInput.value.trim(),
                priority: priorityInput.value,
                due_date: dueDateInput.value.trim() || null,
                project_id: Number(projectIdInput.value)
            })
        }
    );

    if (!response.ok) {
        const errorData = await response.json();

        throw new Error(
            errorData.detail
                ? JSON.stringify(errorData.detail)
                : `HTTP error: ${response.status}`
        );
    }

    const updatedTask = await response.json();

    tasks = tasks.map((task) => {
        if (task.id === taskId) {
            return updatedTask;
        }

        return task;
    });

    saveTasksToCache();
    renderTasks();
}


// ------------------------------------
// Delete task
// ------------------------------------

async function deleteTask(taskId) {
    const confirmed = window.confirm(
        "Are you sure you want to delete this task?"
    );

    if (!confirmed) {
        return;
    }

    try {
        const response = await fetch(
            `${API_BASE_URL}/tasks/${taskId}`,
            {
                method: "DELETE"
            }
        );

        if (!response.ok) {
            const errorData = await response.json();

            throw new Error(
                errorData.detail
                    ? JSON.stringify(errorData.detail)
                    : `HTTP error: ${response.status}`
            );
        }

        tasks = tasks.filter((task) => task.id !== taskId);

        saveTasksToCache();
        renderTasks();
    } catch (error) {
        console.error("Failed to delete task:", error);
        window.alert("Could not delete the task.");
    }
}


// ------------------------------------
// Start editing
// ------------------------------------

function startEditingTask(task) {
    editingTaskId = task.id;

    titleInput.value = task.title;
    priorityInput.value = task.priority;
    dueDateInput.value = task.due_date || "";
    projectIdInput.value = task.project_id;

    submitButton.textContent = "Update Task";

    titleInput.focus();
}


// ------------------------------------
// Form submission
// ------------------------------------

taskForm.addEventListener("submit", async (event) => {
    event.preventDefault();

    if (!validateTitle()) {
        return;
    }

    try {
        submitButton.disabled = true;

        if (editingTaskId === null) {
            await addTask();
        } else {
            await updateTask(editingTaskId);
        }

        taskForm.reset();

        priorityInput.value = "medium";
        projectIdInput.value = "1";

        editingTaskId = null;
        submitButton.textContent = "Add Task";
        titleError.textContent = "";
    } catch (error) {
        console.error("Task operation failed:", error);
        window.alert(
            `Task operation failed: ${error.message}`
        );
    } finally {
        submitButton.disabled = false;
    }
});


// ------------------------------------
// Initial page load
// ------------------------------------

function initializeApp() {
    tasks = loadTasksFromCache();

    renderTasks();

    loadTasksFromBackend();
}

initializeApp();