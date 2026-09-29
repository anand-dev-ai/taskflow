import time
from datetime import date
from fastapi import Depends, FastAPI, HTTPException, Query, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import func, case
from sqlalchemy.orm import Session
from .database import Base, engine, get_db
from . import models, schemas
from .algorithms import insertion_sort, binary_search, linear_search
from .ai_parser import build_task_prompt, parse_task_description
from .auth import create_access_token, get_current_user, hash_password, verify_password

Base.metadata.create_all(bind=engine)
app=FastAPI(title="TaskFlow V2", version="2.0.0", description="Authenticated task and project management API")
app.add_middleware(CORSMiddleware, allow_origins=[
    "http://localhost:5500",
    "http://127.0.0.1:5500",
    "https://taskflow-18gt.onrender.com"
], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

@app.middleware("http")
async def log_requests(request, call_next):
    start=time.perf_counter(); response=await call_next(request); elapsed=(time.perf_counter()-start)*1000
    response.headers["X-Process-Time-ms"]=f"{elapsed:.2f}"
    return response

@app.get("/")
def root(): return {"message":"TaskFlow API is running","version":"2.0.0"}

@app.get("/health")
def health(db: Session=Depends(get_db)):
    db.query(models.User).limit(1).count()
    return {"status":"healthy","service":"taskflow-api","version":"2.0.0"}

@app.post("/auth/register", response_model=schemas.AuthResponse, status_code=status.HTTP_201_CREATED)
def register(data: schemas.UserCreate, db: Session=Depends(get_db)):
    if db.query(models.User).filter(models.User.email==data.email).first(): raise HTTPException(409,"Email already registered")
    user=models.User(name=data.name,email=data.email,password_hash=hash_password(data.password)); db.add(user); db.commit(); db.refresh(user)
    return {"access_token":create_access_token(user.id),"user":user}

@app.post("/auth/login", response_model=schemas.AuthResponse)
def login(data: schemas.LoginRequest, db: Session=Depends(get_db)):
    user=db.query(models.User).filter(models.User.email==data.email).first()
    if not user or not verify_password(data.password,user.password_hash): raise HTTPException(401,"Invalid email or password",headers={"WWW-Authenticate":"Bearer"})
    return {"access_token":create_access_token(user.id),"user":user}

@app.get("/auth/me", response_model=schemas.UserResponse)
def me(current_user=Depends(get_current_user)): return current_user

@app.post("/projects", response_model=schemas.ProjectResponse, status_code=201)
def create_project(data: schemas.ProjectCreate, db: Session=Depends(get_db), user=Depends(get_current_user)):
    project=models.Project(name=data.name,description=data.description,owner_id=user.id); db.add(project); db.commit(); db.refresh(project); return project

@app.get("/projects", response_model=list[schemas.ProjectResponse])
def list_projects(db: Session=Depends(get_db), user=Depends(get_current_user)):
    return db.query(models.Project).filter(models.Project.owner_id==user.id).order_by(models.Project.id.desc()).all()

@app.delete("/projects/{project_id}")
def delete_project(project_id:int, db:Session=Depends(get_db), user=Depends(get_current_user)):
    project=db.query(models.Project).filter(models.Project.id==project_id,models.Project.owner_id==user.id).first()
    if not project: raise HTTPException(404,"Project not found")
    db.delete(project); db.commit(); return {"message":"Project deleted"}

@app.post("/tasks", response_model=schemas.TaskResponse, status_code=201)
def create_task(data:schemas.TaskCreate, db:Session=Depends(get_db), user=Depends(get_current_user)):
    project=db.query(models.Project).filter(models.Project.id==data.project_id,models.Project.owner_id==user.id).first()
    if not project: raise HTTPException(404,"Project not found")
    task=models.Task(**data.model_dump(),user_id=user.id); db.add(task); db.commit(); db.refresh(task); return task

@app.post("/tasks/quick-add", response_model=schemas.TaskResponse, status_code=201)
def quick_add(data:schemas.QuickAddRequest, db:Session=Depends(get_db), user=Depends(get_current_user)):
    project=db.query(models.Project).filter(models.Project.id==data.project_id,models.Project.owner_id==user.id).first()
    if not project: raise HTTPException(404,"Project not found")
    parsed=parse_task_description(build_task_prompt(data.description)[1]["content"])
    task=models.Task(title=parsed["title"],priority=parsed["priority"],due_date=parsed["due_date"],project_id=data.project_id,user_id=user.id)
    db.add(task); db.commit(); db.refresh(task); return task

@app.get("/tasks", response_model=list[schemas.TaskResponse])
def list_tasks(status_filter: str|None=Query(default=None,alias="status"), priority:str|None=None, project_id:int|None=None, search:str|None=None, sort:str="created", db:Session=Depends(get_db), user=Depends(get_current_user)):
    q=db.query(models.Task).filter(models.Task.user_id==user.id)
    if status_filter: q=q.filter(models.Task.status==status_filter)
    if priority: q=q.filter(models.Task.priority==priority)
    if project_id: q=q.filter(models.Task.project_id==project_id)
    if search: q=q.filter(models.Task.title.ilike(f"%{search}%"))
    tasks=q.all()
    if sort=="priority":
        records=[{"task":t,"priority_rank":{"low":1,"medium":2,"high":3}[t.priority]} for t in tasks]; insertion_sort(records,"priority_rank"); return [r["task"] for r in records]
    if sort=="due_date": return sorted(tasks,key=lambda t:t.due_date or date.max)
    if sort not in {"created","priority","due_date"}: raise HTTPException(422,"Invalid sort. Use created, priority, or due_date")
    return sorted(tasks,key=lambda t:t.created_at,reverse=True)

@app.get("/tasks/search", response_model=schemas.TaskResponse)
def search_task(title:str, algo:str="binary", db:Session=Depends(get_db), user=Depends(get_current_user)):
    tasks=db.query(models.Task).filter(models.Task.user_id==user.id).all(); records=[{"id":t.id,"title":t.title} for t in tasks]
    if algo=="binary": insertion_sort(records,"title"); index=binary_search(records,title,"title")
    elif algo=="linear": index=linear_search(records,title,"title")
    else: raise HTTPException(422,"Invalid search algorithm")
    if index==-1: raise HTTPException(404,"Task not found")
    return db.query(models.Task).filter(models.Task.id==records[index]["id" if algo=="binary" else "id"],models.Task.user_id==user.id).first()

@app.get("/tasks/{task_id}", response_model=schemas.TaskResponse)
def get_task(task_id:int, db:Session=Depends(get_db), user=Depends(get_current_user)):
    task=db.query(models.Task).filter(models.Task.id==task_id,models.Task.user_id==user.id).first()
    if not task: raise HTTPException(404,"Task not found")
    return task

@app.put("/tasks/{task_id}", response_model=schemas.TaskResponse)
def update_task(task_id:int, data:schemas.TaskUpdate, db:Session=Depends(get_db), user=Depends(get_current_user)):
    task=db.query(models.Task).filter(models.Task.id==task_id,models.Task.user_id==user.id).first()
    if not task: raise HTTPException(404,"Task not found")
    values=data.model_dump(exclude_unset=True)
    if "project_id" in values and not db.query(models.Project).filter(models.Project.id==values["project_id"],models.Project.owner_id==user.id).first(): raise HTTPException(404,"Project not found")
    for key,value in values.items(): setattr(task,key,value)
    db.commit(); db.refresh(task); return task

@app.delete("/tasks/{task_id}")
def delete_task(task_id:int, db:Session=Depends(get_db), user=Depends(get_current_user)):
    task=db.query(models.Task).filter(models.Task.id==task_id,models.Task.user_id==user.id).first()
    if not task: raise HTTPException(404,"Task not found")
    db.delete(task); db.commit(); return {"message":"Task deleted"}

@app.get("/projects/statistics", response_model=list[schemas.ProjectStatistics])
def project_statistics(db:Session=Depends(get_db), user=Depends(get_current_user)):
    rows=(db.query(models.Project.id,models.Project.name,func.count(models.Task.id),func.sum(case((models.Task.status=="completed",1),else_=0)),func.sum(case((models.Task.status!="completed",1),else_=0)))
        .outerjoin(models.Task,models.Project.id==models.Task.project_id).filter(models.Project.owner_id==user.id).group_by(models.Project.id,models.Project.name).all())
    return [{"project_id":r[0],"project_name":r[1],"task_count":r[2],"completed_count":int(r[3] or 0),"pending_count":int(r[4] or 0)} for r in rows]
