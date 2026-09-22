# TaskFlow V2

TaskFlow V2 evolves the original capstone into an authenticated task-management application while preserving the original CRUD, DSA, Quick Add, and statistics ideas.

## Highlights
- JWT authentication and password hashing
- User-scoped projects and tasks
- Task status, priority, description, due dates, timestamps
- Search, filtering and sorting
- Quick Add natural-language parser with date normalization
- Project statistics
- Algorithm implementations and benchmarking
- FastAPI + SQLAlchemy + SQLite

## Run
1. Create/activate `.venv`
2. `pip install -r requirements.txt`
3. Copy `.env.example` to `.env` and set `SECRET_KEY`
4. `uvicorn backend.main:app --reload`
5. Serve `frontend/` on port 5500, for example with VS Code Live Server.
6. Open `http://127.0.0.1:5500`

API docs: `http://127.0.0.1:8000/docs`

## Interview summary
V2 demonstrates REST API design, ORM relationships, authentication, authorization, validation, database constraints, DSA, natural-language parsing, analytics, and frontend-backend integration.
