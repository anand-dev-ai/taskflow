from datetime import date, datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator

class UserCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)
    @field_validator("name")
    @classmethod
    def clean_name(cls, value):
        value = value.strip()
        if not value: raise ValueError("Name cannot be blank")
        return value

class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=1, max_length=128)

class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

class AuthResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse

class ProjectCreate(BaseModel):
    name: str = Field(min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, max_length=2000)
    @field_validator("name")
    @classmethod
    def clean_name(cls, value):
        value=value.strip()
        if not value: raise ValueError("Project name cannot be blank")
        return value

class ProjectResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    owner_id: int
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)

class TaskCreate(BaseModel):
    title: str = Field(min_length=1, max_length=255)
    description: Optional[str] = Field(default=None, max_length=5000)
    status: str = Field(default="pending", pattern="^(pending|in_progress|completed)$")
    priority: str = Field(default="medium", pattern="^(low|medium|high)$")
    due_date: Optional[date] = None
    project_id: int
    @field_validator("title")
    @classmethod
    def clean_title(cls, value):
        value=value.strip()
        if not value: raise ValueError("Title cannot be blank")
        return value

class TaskUpdate(BaseModel):
    title: Optional[str] = Field(default=None, max_length=255)
    description: Optional[str] = Field(default=None, max_length=5000)
    status: Optional[str] = Field(default=None, pattern="^(pending|in_progress|completed)$")
    priority: Optional[str] = Field(default=None, pattern="^(low|medium|high)$")
    due_date: Optional[date] = None
    project_id: Optional[int] = None
    @field_validator("title")
    @classmethod
    def clean_title(cls, value):
        if value is None: return None
        value=value.strip()
        if not value: raise ValueError("Title cannot be blank")
        return value

class TaskResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    status: str
    priority: str
    due_date: Optional[date]
    project_id: int
    user_id: int
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)

class QuickAddRequest(BaseModel):
    description: str = Field(min_length=1, max_length=1000)
    project_id: int
    @field_validator("description")
    @classmethod
    def clean_description(cls, value):
        value=value.strip()
        if not value: raise ValueError("Description cannot be blank")
        return value

class ProjectStatistics(BaseModel):
    project_id: int
    project_name: str
    task_count: int
    completed_count: int
    pending_count: int
