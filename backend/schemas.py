from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator


class UserCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    email: str = Field(min_length=3, max_length=255)


class UserResponse(BaseModel):
    id: int
    name: str
    email: str

    model_config = ConfigDict(from_attributes=True)


class ProjectCreate(BaseModel):
    name: str = Field(min_length=1, max_length=200)
    owner_id: int


class ProjectResponse(BaseModel):
    id: int
    name: str
    owner_id: int

    model_config = ConfigDict(from_attributes=True)


class TaskCreate(BaseModel):
    title: str = Field(min_length=1, max_length=255)
    priority: str = Field(
        default="medium",
        pattern="^(low|medium|high)$"
    )
    due_date: Optional[str] = None
    project_id: int

    @field_validator("title")
    @classmethod
    def validate_title(cls, value: str) -> str:
        cleaned = value.strip()

        if not cleaned:
            raise ValueError("Title cannot be blank")

        return cleaned


class TaskUpdate(BaseModel):
    title: Optional[str] = Field(
        default=None,
        max_length=255
    )
    priority: Optional[str] = Field(
        default=None,
        pattern="^(low|medium|high)$"
    )
    due_date: Optional[str] = None
    project_id: Optional[int] = None

    @field_validator("title")
    @classmethod
    def validate_title(cls, value: Optional[str]) -> Optional[str]:
        if value is None:
            return None

        cleaned = value.strip()

        if not cleaned:
            raise ValueError("Title cannot be blank")

        return cleaned


class TaskResponse(BaseModel):
    id: int
    title: str
    priority: str
    due_date: Optional[str]
    project_id: int

    model_config = ConfigDict(from_attributes=True)


class ProjectStatistics(BaseModel):
    project_id: int
    project_name: str
    task_count: int


class QuickAddRequest(BaseModel):
    description: str = Field(..., min_length=1)
    project_id: int

    @field_validator("description")
    @classmethod
    def validate_description(cls, value):
        if not value.strip():
            raise ValueError("Description cannot be blank")
        return value