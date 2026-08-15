# TaskFlow — Full-Stack AI-Assisted Task Management Platform

TaskFlow is a full-stack task and project management platform built with FastAPI, SQLAlchemy, SQLite, HTML, CSS, and JavaScript.

It provides:

- User and project management
- Full task CRUD
- Project task statistics
- Insertion-sort based task sorting
- Binary and linear task search
- Algorithm comparison benchmarks
- AI-assisted natural-language Quick-Add
- Browser localStorage caching
- Responsive frontend dashboard
- Request logging middleware
- CORS configuration

---

## 1. Technology Stack

### Backend

- Python
- FastAPI
- SQLAlchemy
- Pydantic
- SQLite
- Uvicorn

### Frontend

- HTML5
- CSS3
- JavaScript
- Fetch API
- localStorage

---

## 2. Project Structure

```text
taskflow/
├── backend/
│   ├── __init__.py
│   ├── main.py
│   ├── models.py
│   ├── schemas.py
│   ├── database.py
│   ├── algorithms.py
│   └── ai_parser.py
├── frontend/
│   ├── index.html
│   ├── styles.css
│   └── script.js
├── check_algorithms.py
├── benchmark.py
├── requirements.txt
└── README.md

3. Environment Setup
Create a Python virtual environment.

Windows PowerShell
python -m venv .venv
Activate it:

.venv\Scripts\Activate.ps1
Install the required packages:

pip install -r requirements.txt
4. Running the Application
TaskFlow uses a two-process setup.

Terminal 1 — Backend
From the project root:

uvicorn backend.main:app --reload --host 127.0.0.1 --port 8000
The backend runs at:

http://127.0.0.1:8000
Swagger API documentation is available at:

http://127.0.0.1:8000/docs
Terminal 2 — Frontend
From the project root:

cd frontend
python -m http.server 5500
Open the dashboard in the browser:

http://127.0.0.1:5500
The frontend communicates with:

http://127.0.0.1:8000
The backend CORS configuration explicitly allows:

http://localhost:5500
http://127.0.0.1:5500
5. Database Schema
TaskFlow uses three related SQLAlchemy tables:

users

projects

tasks

Users
Column	Type	Constraint
id	Integer	Primary key
name	String	NOT NULL
email	String	NOT NULL, UNIQUE
Projects
Column	Type	Constraint
id	Integer	Primary key
name	String	NOT NULL
owner_id	Integer	Foreign key → users.id
Tasks
Column	Type	Constraint
id	Integer	Primary key
title	String	NOT NULL
priority	String	low / medium / high
due_date	String	Nullable
project_id	Integer	Foreign key → projects.id
The SQLAlchemy models use relationship() and back_populates() for:

User ↔ Project
Project ↔ Task
Therefore:

user.projects
project.owner
project.tasks
task.project
resolve through SQLAlchemy relationships.

6. API Endpoints
Users
POST /users
Creates a user.

Example request:

{
  "name": "Rahul",
  "email": "rahul@example.com"
}
Example response:

{
  "id": 1,
  "name": "Rahul",
  "email": "rahul@example.com"
}
Successful creation returns:

201 Created
GET /users
Lists all users.

Example response:

[
  {
    "id": 1,
    "name": "Rahul",
    "email": "rahul@example.com"
  }
]
Successful response:

200 OK
7. Project Endpoints
POST /projects
Creates a project.

Example request:

{
  "name": "Scanner Maintenance",
  "owner_id": 1
}
Example response:

{
  "id": 1,
  "name": "Scanner Maintenance",
  "owner_id": 1
}
Successful creation returns:

201 Created
If the owner does not exist:

404 Not Found
GET /projects
Lists all projects.

Example response:

[
  {
    "id": 1,
    "name": "Scanner Maintenance",
    "owner_id": 1
  }
]
8. Task CRUD Endpoints
POST /tasks
Creates a task.

Example request:

{
  "title": "Repair scanner",
  "priority": "high",
  "due_date": "tomorrow",
  "project_id": 1
}
Example response:

{
  "id": 1,
  "title": "Repair scanner",
  "priority": "high",
  "due_date": "tomorrow",
  "project_id": 1
}
Successful creation:

201 Created
If the project does not exist:

404 Not Found
GET /tasks
Lists all tasks.

Example response:

[
  {
    "id": 1,
    "title": "Repair scanner",
    "priority": "high",
    "due_date": "tomorrow",
    "project_id": 1
  }
]
GET /tasks/{task_id}
Gets one task by ID.

Example:

GET /tasks/1
Example response:

{
  "id": 1,
  "title": "Repair scanner",
  "priority": "high",
  "due_date": "tomorrow",
  "project_id": 1
}
If the task does not exist:

404 Not Found
PUT /tasks/{task_id}
Updates a task.

Example request:

{
  "title": "Repair scanner urgently",
  "priority": "high",
  "due_date": "today",
  "project_id": 1
}
Example response:

{
  "id": 1,
  "title": "Repair scanner urgently",
  "priority": "high",
  "due_date": "today",
  "project_id": 1
}
If the task does not exist:

404 Not Found
DELETE /tasks/{task_id}
Deletes a task.

Example:

DELETE /tasks/1
Example response:

{
  "message": "Task deleted successfully"
}
If the task does not exist:

404 Not Found
9. Validation
Task requests use Pydantic models.

The task priority must be one of:

low
medium
high
For example:

{
  "title": "Test task",
  "priority": "urgent",
  "project_id": 1
}
is rejected because urgent is not a valid priority.

The title also has a custom validator.

Whitespace-only titles are rejected.

Example:

"     "
produces HTTP:

422 Unprocessable Entity
10. Project Statistics
GET /projects/statistics
Returns task statistics for every project.

The aggregation is performed by SQLAlchemy using SQL COUNT and GROUP BY.

Example response:

[
  {
    "project_id": 1,
    "project_name": "Scanner Maintenance",
    "task_count": 3
  },
  {
    "project_id": 2,
    "project_name": "Network",
    "task_count": 5
  }
]
The task counts are calculated by the database rather than fetching every task and counting them in Python.

11. Sorting Endpoint
GET /tasks?sort=priority
Returns tasks sorted by priority.

Priority ranking:

low = 1
medium = 2
high = 3
Example:

GET /tasks?sort=priority
Example response:

[
  {
    "id": 2,
    "title": "Clean scanner",
    "priority": "low",
    "due_date": "Friday",
    "project_id": 1
  },
  {
    "id": 1,
    "title": "Repair scanner",
    "priority": "high",
    "due_date": "today",
    "project_id": 1
  }
]
The endpoint fetches real tasks from the database and calls the custom:

insertion_sort(records, "priority_rank")
It does not use Python's:

sorted()
or:

list.sort()
12. Search Endpoints
GET /tasks/search?title={title}&algo=binary
Searches for an exact task title using binary search.

Example:

GET /tasks/search?title=Repair%20scanner&algo=binary
Example response:

{
  "id": 1,
  "title": "Repair scanner",
  "priority": "high",
  "due_date": "today",
  "project_id": 1
}
The search index is sorted using the custom insertion sort before binary search.

If the task does not exist:

404 Not Found
GET /tasks/search?title={title}&algo=linear
Searches for an exact task title using linear search.

Example:

GET /tasks/search?title=Repair%20scanner&algo=linear
Example response:

{
  "id": 1,
  "title": "Repair scanner",
  "priority": "high",
  "due_date": "today",
  "project_id": 1
}
If the task does not exist:

404 Not Found
An unsupported algorithm value returns:

422 Unprocessable Entity
13. AI Quick-Add
POST /tasks/quick-add
Quick-Add accepts a natural-language description and creates a real task in the same database.

Example request:

{
  "description": "Fix the scanner ASAP next Monday",
  "project_id": 1
}
Example response:

{
  "id": 5,
  "title": "Fix the scanner",
  "priority": "high",
  "due_date": "next monday",
  "project_id": 1
}
Successful creation:

201 Created
The implementation:

Validates the request.

Checks that the project exists.

Builds a role-based prompt.

Runs the deterministic mock parser.

Validates the parsed task with the Pydantic Task model.

Creates the real database row.

Returns the created task.

The required mock parser uses:

zero API keys
zero network calls
zero paid services
14. AI Parser Rules
The parser first creates a lower-case copy of the description for keyword matching.

The original description casing is preserved for the title.

Priority
Priority is determined in this order:

High
If the description contains:

urgent
or:

asap
priority becomes:

high
Low
If high priority keywords are absent and the description contains:

whenever
or:

low priority
priority becomes:

low
Medium
If neither group matches:

medium
If both high and low keywords are present, high wins.

All occurrences of all priority keywords are removed from the title.

15. AI Due-Date Rules
Due-date phrases are checked in this order:

today

tomorrow

next week

next monday

next tuesday

next wednesday

next thursday

next friday

next saturday

next sunday

monday

tuesday

wednesday

thursday

friday

saturday

sunday

The first matching phrase is used.

The returned phrase is lowercase.

For example:

Finish the report next Friday
produces:

{
  "due_date_hint": "next friday"
}
The due-date value is stored as raw text in the database.

16. AI Title Rules
The parser removes every matching priority keyword from the original description.

It also removes the matched due-date phrase.

The remaining text is trimmed using .strip().

If nothing remains, the title becomes:

Untitled task
The title can never be empty.

17. Prompt Structure
The Quick-Add feature constructs a role-based prompt with:

system → parsing instructions
user → free-text task description
This structure allows the same interface to be used later with a real LLM while the required implementation remains a deterministic mock.

18. Prompting Technique
The implementation is modeled primarily on zero-shot prompting.

The system message directly describes the expected parsing behavior instead of requiring many example conversations.

This reduces token usage compared with few-shot prompting because multiple examples do not have to be included in every request.

The explicit instructions also improve response reliability because the parser behavior is clearly defined.

Chain-of-thought prompting is unnecessary because the required output is a structured task record rather than an explanation of reasoning.

The current implementation is deterministic and therefore does not depend on probabilistic LLM behavior.

19. Five AI Worked Examples
Example 1
Input:

This is urgent, mark it ASAP please
Output:

{
  "title": "This is , mark it please",
  "priority": "high",
  "due_date_hint": null
}
Example 2
Input:

 
Output:

{
  "title": "Untitled task",
  "priority": "medium",
  "due_date_hint": null
}
Example 3
Input:

Finish the report next Friday, it's urgent
Output:

{
  "title": "Finish the report , it's",
  "priority": "high",
  "due_date_hint": "next friday"
}
Example 4
Input:

tomorrow review tomorrow
Output:

{
  "title": "review",
  "priority": "medium",
  "due_date_hint": "tomorrow"
}
Example 5
Input:

Fix the scanner ASAP next Monday
Output:

{
  "title": "Fix the scanner",
  "priority": "high",
  "due_date_hint": "next monday"
}
20. Algorithms
TaskFlow implements three hand-written algorithms.

insertion_sort(records, key)
Insertion sort modifies the input list directly.

It starts at the second element, compares the current element with previous elements, shifts larger elements to the right, and inserts the current element into its correct position.

It does not use Python's built-in sorting functions.

binary_search(sorted_records, target_value, key)
Binary search operates on records that are already sorted by the specified key.

It uses:

low
high
mid
pointers.

It returns the index of the matching record.

If the target is not found, it returns:

-1
linear_search(records, target_value, key)
Linear search scans the records from beginning to end.

It returns the index of the first matching record.

If no record matches, it returns:

-1
21. Algorithm Complexity
Algorithm	Best Case	Worst Case
Insertion Sort	O(n)	O(n²)
Binary Search	O(1)	O(log n)
Linear Search	O(1)	O(n)
Insertion sort has O(n) best-case time when the list is already ordered.

Its worst-case time is O(n²) because many elements may need to be shifted.

Binary search has O(1) best-case time when the middle element is the target.

Its worst-case time is O(log n) because it halves the search space at each step.

Linear search has O(1) best-case time when the first item matches and O(n) worst-case time when it must inspect the entire list.

22. Comparison-Counting Benchmark
The benchmark uses the counting versions of the algorithms.

The benchmark was run at three data sizes.

Data size: 10
Insertion sort comparisons: 45
Binary search: index=0, comparisons=5
Linear search: index=9, comparisons=10
Data size: 500
Insertion sort comparisons: 94034
Binary search: index=0, comparisons=15
Linear search: index=499, comparisons=500
Data size: 3000
Insertion sort comparisons: 2681712
Binary search: index=0, comparisons=21
Linear search: index=2999, comparisons=3000
Run the benchmark with:

python benchmark.py
23. Benchmark Analysis
The benchmark shows that insertion sort becomes expensive as the number of records increases.

At 10 records it required only 45 comparisons, but at 3,000 records it required 2,681,712 comparisons.

In comparison, binary search required only 21 comparisons for the 3,000-record search, while linear search required 3,000 comparisons.

For TaskFlow, users may repeatedly view and search their tasks throughout the day while adding or renaming tasks less frequently.

Therefore, paying the sorting cost can be worthwhile when sorted data is reused for repeated searches.

For a single search, however, linear search can be preferable because it does not require an initial sorting operation.

24. Automated Algorithm Checks
The project includes:

check_algorithms.py
Run it with:

python check_algorithms.py
The script checks:

Empty insertion sort

Single-element insertion sort

Binary search first index

Binary search last index

Binary search middle index

Binary search not-found case

Insertion sort comparison counting

Binary search comparison counting

Linear search comparison counting

Expected output:

PASS: insertion_sort empty list
PASS: insertion_sort single element
PASS: binary_search first index
PASS: binary_search last index
PASS: binary_search middle
PASS: binary_search not found
PASS: insertion_sort_count sorting and count
PASS: binary_search_count
PASS: linear_search_count absent value
The script uses normal if/else conditional statements and does not require pytest or unittest.

25. Frontend Dashboard
The frontend is located in:

frontend/
It contains:

index.html
styles.css
script.js
The dashboard includes:

Page heading

Add-task form

Task title input

Due-date input

Priority input

Task list

Edit controls

Delete controls

The frontend communicates with the real FastAPI backend through the Fetch API.

There is no disconnected mock task data layer.

26. Frontend Validation
The add-task form uses:

event.preventDefault()
before submitting data.

If the title is empty or contains only whitespace, a validation message is displayed.

The request is not sent to the backend until the title is valid.

Once the title becomes valid, the validation error is removed.

27. Safe DOM Rendering
Task items are created using:

document.createElement()
and:

appendChild()
User-provided task titles are inserted using:

textContent
rather than unsafe HTML string concatenation.

Interactive controls use:

addEventListener()
and no inline onclick attributes are used.

28. localStorage Cache
The frontend stores the current real backend task list in localStorage.

The task list is converted to JSON using:

JSON.stringify()
When the page loads, the cached JSON is read using:

JSON.parse()
The cached tasks are rendered immediately while the live backend request is in progress.

After the backend responds, the current backend data replaces the cached data.

localStorage is only a cache and is not a replacement for the backend database.

29. Responsive Design
The frontend uses CSS media queries.

A breakpoint is provided for screens up to:

768px
Another breakpoint is provided for screens up to:

480px
The layout changes at these breakpoints, including the task form layout.

The page also uses the CSS box model with:

margin

border

padding

for task-list and task-item elements.

A persistent UI element uses sticky positioning.

30. Request Logging Middleware
TaskFlow includes custom HTTP middleware.

For every request it records:

HTTP method

URL path

processing time in milliseconds

Example console output:

GET /tasks - 4.32 ms
POST /tasks - 5.21 ms
POST /tasks/quick-add - 7.18 ms
This middleware executes for every HTTP request.

31. FastAPI Dependency
The application defines a shared database dependency:

get_db
It is used with:

Depends(get_db)
across multiple endpoints.

This avoids duplicating database-session creation and cleanup logic.

The same dependency is used by the CRUD, statistics, sorting, search, and Quick-Add endpoints.

32. CORS
CORS middleware is configured explicitly.

Allowed origins:

http://localhost:5500
http://127.0.0.1:5500
Allowed methods:

GET
POST
PUT
DELETE
OPTIONS
Allowed headers include:

Content-Type
Authorization
A wildcard origin is not used.

33. Error Handling
Common errors include:

404
Returned when a requested task, project, or user-related resource does not exist.

Example:

{
  "detail": "Task not found"
}
422
Returned when Pydantic validation fails.

Examples include:

Missing required fields

Invalid priority

Blank title

Blank Quick-Add description

Invalid request data

The Quick-Add endpoint also returns 422 when the specified project does not exist.

No task row is created when validation fails.

34. Testing the Application
Start the backend:

uvicorn backend.main:app --reload --host 127.0.0.1 --port 8000
Start the frontend in another terminal:

cd frontend
python -m http.server 5500
Open:

http://127.0.0.1:5500
API documentation:

http://127.0.0.1:8000/docs
The application can be tested through the dashboard or through Swagger.

The following functionality is supported:

User creation

User listing

Project creation

Project listing

Task creation

Task listing

Task retrieval

Task update

Task deletion

Task sorting

Binary search

Linear search

Project statistics

AI Quick-Add

Frontend validation

localStorage caching

Responsive dashboard

35. Example End-to-End Workflow
First create a user:

{
  "name": "Rahul",
  "email": "rahul@example.com"
}
Suppose the returned user ID is:

1
Create a project:

{
  "name": "Dark Store Engineering",
  "owner_id": 1
}
Suppose the returned project ID is:

1
Create a normal task:

{
  "title": "Check scanner",
  "priority": "medium",
  "due_date": "tomorrow",
  "project_id": 1
}
Or use Quick-Add:

{
  "description": "Fix scanner ASAP next Monday",
  "project_id": 1
}
The Quick-Add parser creates:

{
  "title": "Fix scanner",
  "priority": "high",
  "due_date": "next monday",
  "project_id": 1
}
The new task is stored in the same tasks table and can immediately be retrieved using:

GET /tasks
or:

GET /tasks/{id}
It is also included in:

GET /projects/statistics
36. Repository and Git Workflow
The complete TaskFlow application is contained in one repository.

The repository contains all three graded sections:

Section 1 → Core App
Section 2 → Algorithms Engine
Section 3 → AI Quick-Add
The Git workflow uses a feature branch.

At least one feature branch was created, committed to multiple times, and merged back into the main branch.

The complete history can be inspected with:

git log --graph --oneline --all
37. Final Project Checklist
The project contains:

 FastAPI backend

 SQLAlchemy ORM

 SQLite database

 Users table

 Projects table

 Tasks table

 Foreign-key relationships

 Pydantic validation

 Task CRUD

 User create/list

 Project create/list

 Project statistics

 FastAPI dependency

 Request logging middleware

 CORS

 Frontend dashboard

 Fetch API

 localStorage caching

 Client-side validation

 Responsive CSS

 Custom insertion sort

 Custom binary search

 Custom linear search

 Sorting endpoint

 Search endpoint

 Counting benchmarks

 Algorithm check script

 AI Quick-Add

 Deterministic mock parser

 Role-based prompt structure

 Five AI worked examples

 No API key required

 One repository containing the entire application

38. Conclusion
TaskFlow combines a relational backend, interactive frontend, custom algorithms, and deterministic AI-assisted task creation into one working full-stack application.

The sorting and searching algorithms operate on real database task data.

The Quick-Add parser creates real task records in the same database used by the normal CRUD endpoints.

The frontend communicates directly with the backend and uses localStorage only as a temporary cache.

The application can therefore be run locally without any paid external service or API key.


### Now do only these 3 things

**1.** In VS Code, open `README.md`.

**2.** Press:

```text
Ctrl + A
then paste the complete README above.

3. Press:

Ctrl + S