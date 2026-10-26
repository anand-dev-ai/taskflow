# TaskFlow V2 — Full-Stack Task Management Platform

TaskFlow V2 is an upgraded version of my original capstone project, developed to demonstrate backend engineering, relational database design, authentication, algorithm implementation, automated testing, and deployment.

Built with Python, FastAPI, SQLAlchemy, SQLite, HTML, CSS, and JavaScript, the application provides authenticated task and project management through a web dashboard and REST API.

The project extends the original CRUD, data structures and algorithms (DSA), Quick Add, and statistics features with JWT-based authentication, user-scoped resources, automated tests, and deployment.

## Live Application

- **Live Demo:** https://taskflow-6rmp.onrender.com
- **API Documentation (Swagger UI):** https://taskflow-6rmp.onrender.com/docs

## Key Features

- **Authentication:** JWT-based authentication, password hashing, and authenticated API access.
- **User-specific resources:** Access controls for users' own projects and tasks.
- **Task management:** Create, retrieve, update, and delete tasks.
- **Project management:** Organize tasks into projects.
- **Task organization:** Manage priorities, statuses, descriptions, and due dates.
- **Search and filtering:** Find and organize tasks using supported search, filtering, and sorting operations.
- **Project statistics:** Retrieve task counts and project-level statistics.
- **Quick Add:** Parse natural-language task descriptions into structured task data using a deterministic parser.
- **Custom algorithms:** Implement insertion sort, binary search, and linear search.
- **Algorithm benchmarking:** Compare algorithm comparison counts across different dataset sizes.
- **Input validation:** Validate request data using Pydantic models.
- **Automated testing:** Test application workflows using pytest.
- **Continuous integration:** Run automated tests through GitHub Actions.
- **Web interface:** Responsive HTML, CSS, and JavaScript frontend.
- **Deployment:** Serve the frontend and backend through FastAPI in the deployed application.

## Technology Stack

| Area | Technologies |
|---|---|
| Programming language | Python |
| Backend framework | FastAPI |
| API documentation | OpenAPI, Swagger UI |
| Database | SQLite |
| ORM | SQLAlchemy |
| Data validation | Pydantic |
| Authentication | JWT, password hashing |
| Frontend | HTML5, CSS3, JavaScript |
| HTTP communication | Fetch API |
| Testing | pytest |
| CI | GitHub Actions |
| Version control | Git, GitHub |
| Hosting | Render |

## Project Architecture

The application separates its backend responsibilities into modules for application routes and logic, database configuration, ORM models, request and response schemas, algorithm implementations, and Quick Add parsing.

The frontend contains the HTML page, CSS styles, and JavaScript used to communicate with the backend.

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
├── tests/
│   └── test_v2.py
├── check_algorithms.py
├── benchmark.py
├── requirements.txt
└── README.md
```

The exact files and test paths should match the current repository.

### Architecture responsibilities

- **`main.py`:** FastAPI application, routes, middleware, and application integration.
- **`database.py`:** Database configuration, SQLAlchemy setup, and database-session dependency.
- **`models.py`:** Relational database models and relationships.
- **`schemas.py`:** Pydantic schemas and request validation.
- **`algorithms.py`:** Custom sorting and searching implementations.
- **`ai_parser.py`:** Deterministic natural-language task parsing.
- **`frontend/`:** Browser interface and API communication.
- **`tests/`:** Automated tests for application behavior.

## Database Design

TaskFlow V2 uses SQLAlchemy with SQLite to persist application data.

The primary entities are:

### User

Represents an application user and stores account information. Authentication-related fields support secure login.

### Project

Represents a project owned by a user. The owner relationship connects projects to their users.

### Task

Represents a task associated with a project. Task fields support titles, descriptions, priorities, status, and due dates.

### Relationships

The relational model connects users, projects, and tasks through foreign keys and SQLAlchemy relationships.

These relationships support structured queries and help maintain consistency between related records.

TaskFlow V2 also uses user-scoped queries and ownership checks to ensure that authenticated users can access only resources they are authorized to manage.

## Authentication and Authorization

TaskFlow V2 uses JWT-based authentication and password hashing.

The authentication workflow includes:

1. Registering a user.
2. Storing a password hash rather than a plaintext password.
3. Authenticating login credentials.
4. Issuing a JWT after successful authentication.
5. Sending the token with protected API requests.
6. Verifying the authenticated user's identity and resource ownership.

User-scoped access controls are an important part of the application because authentication alone does not establish permission to access every resource.

## REST API Development

FastAPI provides the application's REST API and generates OpenAPI documentation for supported endpoints.

The API supports task and project management, authentication, and other features implemented in the application.

### API documentation

Open the deployed Swagger UI:

https://taskflow-6rmp.onrender.com/docs

Swagger UI allows developers to inspect available endpoints, examine request and response schemas, and try supported API operations.

### Request validation

Pydantic schemas validate incoming request data. Depending on the endpoint, validation can enforce required fields, permitted priority values, and non-empty task titles.

Invalid request data should produce appropriate HTTP error responses rather than creating invalid records.

### Error handling

The application uses HTTP status codes to communicate request outcomes. Examples include:

- `200 OK` for successful retrieval or updates where configured.
- `201 Created` for successful resource creation where configured.
- `401 Unauthorized` for missing or invalid authentication where applicable.
- `403 Forbidden` when a request is authenticated but not permitted, where implemented.
- `404 Not Found` when a requested resource does not exist or is intentionally treated as unavailable.
- `422 Unprocessable Entity` for request validation failures.

Actual status codes depend on the endpoint implementation and should be verified against the running API.

## Task Management

TaskFlow V2 supports task creation, retrieval, updates, and deletion.

Tasks can include fields such as:

- Title
- Description
- Priority
- Status
- Due date
- Project association
- Timestamps, where implemented

The application also provides supported filtering, sorting, search, and statistics operations.

## Project Statistics

TaskFlow provides project-level task statistics through its API.

Where implemented, SQLAlchemy queries use database aggregation, such as `COUNT` and `GROUP BY`, to calculate task counts.

Database-side aggregation can avoid retrieving every task into Python solely to calculate totals.

## Custom Data Structures and Algorithms

TaskFlow includes hand-written implementations of three algorithms.

### Insertion Sort

Insertion sort orders records according to a specified key by shifting larger elements and inserting each item into its appropriate position.

- Best-case time complexity: `O(n)` for already sorted input.
- Average-case time complexity: `O(n²)`.
- Worst-case time complexity: `O(n²)`.
- Auxiliary space complexity: `O(1)` for an in-place implementation.

### Binary Search

Binary search repeatedly halves a sorted search space to locate a target.

- Best-case time complexity: `O(1)`.
- Average-case time complexity: `O(log n)`.
- Worst-case time complexity: `O(log n)`.
- Auxiliary space complexity: `O(1)` for an iterative implementation.

**Requirement:** Binary search operates on data sorted according to the same key used for searching.

### Linear Search

Linear search examines records sequentially until it finds a target or reaches the end.

- Best-case time complexity: `O(1)`.
- Average-case time complexity: `O(n)`.
- Worst-case time complexity: `O(n)`.
- Auxiliary space complexity: `O(1)` for a simple iterative implementation.

### Algorithm Comparison

The project includes a benchmark script that records comparison counts for different input sizes.

Previously recorded results include:

| Dataset size | Insertion sort comparisons | Binary search comparisons | Linear search comparisons |
|---:|---:|---:|---:|
| 10 | 45 | 5 | 10 |
| 500 | 94,034 | 15 | 500 |
| 3,000 | 2,681,712 | 21 | 3,000 |

These are recorded comparison counts, not execution-time measurements. They should be retained only if they match the current benchmark implementation and can be reproduced.

The benchmark illustrates why repeated searching in sorted data can benefit from binary search, while the initial sorting cost must also be considered.

## Quick Add: Natural-Language Task Parsing

TaskFlow's Quick Add feature converts supported natural-language descriptions into structured task data.

For example, a description such as:

```text
Fix the scanner ASAP next Monday
```

may be parsed into:

```json
{
  "title": "Fix the scanner",
  "priority": "high",
  "due_date_hint": "next monday"
}
```

The exact output depends on the parser's implemented rules.

### Parsing behavior

The deterministic parser recognizes supported priority keywords and date phrases, removes recognized phrases from the task title, and produces structured fields.

For example, supported priority rules may recognize:

- `urgent` or `asap` as high priority.
- `whenever` or `low priority` as low priority.
- No recognized priority keyword as medium priority.

When a high-priority keyword and a low-priority keyword are both present, the current documented rule gives high priority precedence.

Supported date phrases include terms such as `today`, `tomorrow`, `next week`, and weekday names.

### Important implementation distinction

The current parser is deterministic and does not itself require an external LLM API call.

The feature demonstrates natural-language-style task parsing, prompt-structure concepts, and structured data validation. It should not be described as a trained machine-learning model or a live LLM integration unless that functionality is separately implemented.

Recognized due-date phrases are hints. If stored as text, they are not necessarily normalized into actual calendar dates.

## Frontend Integration

The browser frontend communicates with FastAPI using the Fetch API.

The interface supports task-related interactions implemented in the current frontend, including form submission and task-list updates.

### Frontend validation

Client-side validation can prevent empty or whitespace-only titles from being submitted.

Backend validation remains necessary because client-side checks can be bypassed.

### Safe DOM rendering

Where implemented, the frontend uses DOM methods such as `document.createElement`, `appendChild`, and `textContent` to display task information.

Using `textContent` for user-provided text helps avoid interpreting that text as HTML.

### Local storage

If enabled, browser `localStorage` can cache previously retrieved task data for faster initial display.

Cached data is not the authoritative database. The backend remains the source of truth, and cached content should be reconciled with the server response.

### Responsive layout

The frontend uses CSS to adapt the interface to different screen sizes.

The supported breakpoints and specific responsive behavior should match the current stylesheet.

## Automated Testing

TaskFlow V2 includes automated tests for important application workflows.

The verified test result previously recorded for the project was:

- Five pytest tests passing.
- A successful GitHub Actions Python Tests workflow.

These results should be rechecked against the latest code before being treated as current.

Run the test suite from the repository root:

```bash
python -m pytest -v
```

If the project has a separate algorithm-check script, run it with:

```bash
python check_algorithms.py
```

The algorithm-check script and pytest suite serve different purposes and should be described separately.

## Continuous Integration

The GitHub Actions Python Tests workflow runs automated tests to help detect regressions when code changes are pushed or when the workflow is otherwise triggered.

The workflow provides repeatable test execution and a visible record of success or failure.

Its actual triggers, Python version, dependency installation steps, and test commands are defined in the repository's workflow configuration.

View the repository's Actions tab to inspect the workflow runs.

## Local Installation and Setup

### Prerequisites

- Python installed on your system.
- Git, if cloning the repository.
- The project dependencies listed in `requirements.txt`.

### 1. Clone the repository

```bash
git clone https://github.com/anand-dev-ai/taskflow.git
cd taskflow
```

Switch to the appropriate branch if the current V2 code is maintained on a separate branch.

### 2. Create a virtual environment

On Windows PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Start the application

Run the following from the project root:

```bash
uvicorn backend.main:app --reload
```

Open the local API documentation:

http://127.0.0.1:8000/docs

If the frontend is served directly through FastAPI in the current version, open the application at the root URL:

http://127.0.0.1:8000/

If the local development setup instead requires a separate frontend server, follow the instructions for that specific version of the application.

## Configuration and Security Notes

- Never commit real passwords, secret keys, or access tokens.
- Use appropriate secret management for JWT signing keys.
- Store password hashes rather than plaintext passwords.
- Validate input on the server, even when the frontend performs validation.
- Verify resource ownership for authenticated requests.
- Restrict CORS origins to the intended frontend origins.
- Treat cached browser data as untrusted and potentially stale.
- Keep dependencies and configuration consistent between development and deployment.

## Git and Version Control

The project is maintained in Git and hosted on GitHub.

Review recorded changes with:

```bash
git log --oneline
```

Inspect branches with:

```bash
git branch --all
```

A feature-branch workflow can help isolate changes and make development history easier to review. Claims about merges, pull-request reviews, or team collaboration should reflect the actual repository history.

## Future Improvements

Potential areas for further development include:

- Database schema migrations.
- Containerized development and deployment.
- Expanded automated tests and API integration tests.
- More comprehensive error handling and logging.
- Improved algorithm benchmark methodology.
- Stronger API performance measurement.
- Additional documentation for configuration and deployment.

These are possible future improvements, not claims that the features are already implemented.

## Conclusion

TaskFlow V2 combines authenticated task management, relational database modeling, REST API development, custom algorithms, deterministic natural-language parsing, automated testing, and deployment in one project.

It demonstrates practical software engineering work across backend implementation, data validation, authorization, testing, version control, and application delivery.

The project is intended as a learning and portfolio application. Its features, test results, benchmark measurements, and deployment behavior should be evaluated against the current source code and reproducible evidence.
