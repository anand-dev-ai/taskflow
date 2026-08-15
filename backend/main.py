import time

from fastapi import Depends, FastAPI, HTTPException, Request, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import func
from sqlalchemy.orm import Session
from backend.ai_parser import (
    parse_task_description,
    build_task_prompt
)
from backend.schemas import QuickAddRequest

from .database import Base, engine, get_db
from . import models, schemas
from .algorithms import (
    insertion_sort,
    binary_search,
    linear_search
)

Base.metadata.create_all(bind=engine)

app = FastAPI(title="TaskFlow")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5500",
        "http://127.0.0.1:5500"
    ],
    allow_credentials=True,
    allow_methods=[
        "GET",
        "POST",
        "PUT",
        "DELETE",
        "OPTIONS"
    ],
    allow_headers=[
        "Content-Type",
        "Authorization"
    ]
)

@app.middleware("http")
async def request_logging_middleware(request: Request, call_next):
    start_time = time.perf_counter()

    response = await call_next(request)

    processing_time = (time.perf_counter() - start_time) * 1000

    print(
        f"{request.method} {request.url.path} "
        f"- {processing_time:.2f} ms"
    )

    return response


@app.get("/")
def root():
    return {
        "message": "TaskFlow API is running"
    }


@app.get("/database-test")
def database_test(db: Session = Depends(get_db)):
    user_count = db.query(models.User).count()

    return {
        "message": "Database connection works",
        "user_count": user_count
    }


# -------------------------
# User endpoints
# -------------------------

@app.post(
    "/users",
    response_model=schemas.UserResponse,
    status_code=status.HTTP_201_CREATED
)
def create_user(
    user: schemas.UserCreate,
    db: Session = Depends(get_db)
):
    existing_user = (
        db.query(models.User)
        .filter(models.User.email == user.email)
        .first()
    )

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    new_user = models.User(
        name=user.name,
        email=user.email
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@app.get(
    "/users",
    response_model=list[schemas.UserResponse]
)
def list_users(db: Session = Depends(get_db)):
    return db.query(models.User).all()
# -------------------------
# Project endpoints
# -------------------------

@app.post(
    "/projects",
    response_model=schemas.ProjectResponse,
    status_code=status.HTTP_201_CREATED
)
def create_project(
    project: schemas.ProjectCreate,
    db: Session = Depends(get_db)
):
    owner = (
        db.query(models.User)
        .filter(models.User.id == project.owner_id)
        .first()
    )

    if owner is None:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    new_project = models.Project(
        name=project.name,
        owner_id=project.owner_id
    )

    db.add(new_project)
    db.commit()
    db.refresh(new_project)

    return new_project


@app.get(
    "/projects",
    response_model=list[schemas.ProjectResponse]
)
def list_projects(db: Session = Depends(get_db)):
    return db.query(models.Project).all()
# -------------------------
# Task endpoints
# -------------------------

@app.post(
    "/tasks",
    response_model=schemas.TaskResponse,
    status_code=status.HTTP_201_CREATED
)
def create_task(
    task: schemas.TaskCreate,
    db: Session = Depends(get_db)
):
    project = (
        db.query(models.Project)
        .filter(models.Project.id == task.project_id)
        .first()
    )

    if project is None:
        raise HTTPException(
            status_code=404,
            detail="Project not found"
        )

    new_task = models.Task(
        title=task.title,
        priority=task.priority,
        due_date=task.due_date,
        project_id=task.project_id
    )

    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    return new_task

@app.post(
    "/tasks/quick-add",
    response_model=schemas.TaskResponse,
    status_code=status.HTTP_201_CREATED
)
def quick_add_task(
    data: QuickAddRequest,
    db: Session = Depends(get_db)
    ):
    # Check that the project exists
    project = db.query(models.Project).filter(
        models.Project.id == data.project_id
    ).first()

    if project is None:
        raise HTTPException(
            status_code=422,
            detail=[
                {
                    "type": "value_error",
                    "loc": ["body", "project_id"],
                    "msg": "Value error, project_id does not reference an existing project",
                    "input": data.project_id
                }
            ]
        )

    # Parse the natural-language description
    prompt = build_task_prompt(data.description)

    parsed = parse_task_description(
        prompt[1]["content"]
    )
    # Create a real Task database row
    validated_task = schemas.TaskCreate(
        title=parsed["title"],
        priority=parsed["priority"],
        due_date=parsed["due_date_hint"],
        project_id=data.project_id
    )

    task = models.Task(
        title=validated_task.title,
        priority=validated_task.priority,
        due_date=validated_task.due_date,
        project_id=validated_task.project_id
    )

    # Save to the same database used by normal CRUD
    db.add(task)
    db.commit()
    db.refresh(task)

    return task

@app.get("/tasks", response_model=list[schemas.TaskResponse])
def get_tasks(
    sort: str | None = None,
    db: Session = Depends(get_db)
):
    task_records = db.query(models.Task).all()

    if sort == "priority":
        records = [
            {
                "id": task.id,
                "title": task.title,
                "priority": task.priority,
                "priority_rank": {
                    "low": 1,
                    "medium": 2,
                    "high": 3
                }[task.priority],
                "due_date": task.due_date,
                "project_id": task.project_id
            }
            for task in task_records
        ]

        insertion_sort(records, "priority_rank")

        return records

    return task_records



@app.get("/tasks/search")
def search_tasks(
    title: str,
    algo: str = "binary",
    db: Session = Depends(get_db)
):
    tasks = db.query(models.Task).all()

    search_index = [
        {
            "id": task.id,
            "title": task.title
        }
        for task in tasks
    ]

    if algo == "binary":
        insertion_sort(search_index, "title")

        index = binary_search(
            search_index,
            title,
            "title"
        )

    elif algo == "linear":
        index = linear_search(
            search_index,
            title,
            "title"
        )

    else:
        raise HTTPException(
            status_code=422,
            detail="algo must be 'binary' or 'linear'"
        )

    if index == -1:
        raise HTTPException(
            status_code=404,
            detail="Task with that exact title was not found"
        )

    task_id = search_index[index]["id"]

    task = db.query(models.Task).filter(
        models.Task.id == task_id
    ).first()

    if task is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    return task


@app.get(
    "/tasks/{task_id}",
    response_model=schemas.TaskResponse
)
def get_task(
    task_id: int,
    db: Session = Depends(get_db)
):
    task = (
        db.query(models.Task)
        .filter(models.Task.id == task_id)
        .first()
    )

    if task is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    return task


@app.put(
    "/tasks/{task_id}",
    response_model=schemas.TaskResponse
)
def update_task(
    task_id: int,
    task_data: schemas.TaskUpdate,
    db: Session = Depends(get_db)
):
    task = (
        db.query(models.Task)
        .filter(models.Task.id == task_id)
        .first()
    )

    if task is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    update_data = task_data.model_dump(exclude_unset=True)

    if "project_id" in update_data:
        project = (
            db.query(models.Project)
            .filter(models.Project.id == update_data["project_id"])
            .first()
        )

        if project is None:
            raise HTTPException(
                status_code=404,
                detail="Project not found"
            )

    for field, value in update_data.items():
        setattr(task, field, value)

    db.commit()
    db.refresh(task)

    return task


@app.delete(
    "/tasks/{task_id}"
)
def delete_task(
    task_id: int,
    db: Session = Depends(get_db)
):
    task = (
        db.query(models.Task)
        .filter(models.Task.id == task_id)
        .first()
    )

    if task is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    db.delete(task)
    db.commit()

    return {
        "message": "Task deleted successfully"
    }
# -------------------------
# Project statistics
# -------------------------

@app.get(
    "/projects/statistics",
    response_model=list[schemas.ProjectStatistics]
)
def project_statistics(db: Session = Depends(get_db)):
    results = (
        db.query(
            models.Project.id.label("project_id"),
            models.Project.name.label("project_name"),
            func.count(models.Task.id).label("task_count")
        )
        .outerjoin(
            models.Task,
            models.Project.id == models.Task.project_id
        )
        .group_by(
            models.Project.id,
            models.Project.name
        )
        .all()
    )

    return [
        {
            "project_id": row.project_id,
            "project_name": row.project_name,
            "task_count": row.task_count
        }
        for row in results
    ]

