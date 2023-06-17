from pydantic import BaseModel, Field
from datetime import datetime

class NoteBase(BaseModel):
    title: str
    description: str | None = None
    created_at: datetime = Field(default_factory=datetime.now)


class NoteCreate(NoteBase):
    pass


class Note(NoteBase):
    id: int
    owner_id: int
    category_id: int
    created_at: datetime = Field(default_factory=datetime.now)

    class Config:
        orm_mode = True


class CategoryBase(BaseModel):
    title: str
    description: str | None = None


class CategoryCreate(CategoryBase):
    pass


class Category(CategoryBase):
    id: int
    created_at: datetime = Field(default_factory=datetime.now)
    # owner_id: int

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool
    Notes: list[Note] = []
    created_at: datetime = Field(default_factory=datetime.now)

    class Config:
        orm_mode = True