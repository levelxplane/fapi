from typing import Annotated
from fastapi import FastAPI, Path, Query, HTTPException, Depends
import json, aiofiles
from sqlalchemy.orm import Session

import crud, models, schemas
from models import User, Note, Category
from database import SessionLocal, engine

app = FastAPI()


@app.get("/")
async def root():
    # data = await get_notes_from_file()
    return {"lol": "go away"}


# async def get_notes_from_file(category=None):
#     async with aiofiles.open("notes/notes.json", mode="r") as file:
#         content = await file.read()

#     data = json.loads(content)
#     if not category:
#         return data
#     else:
#         return data.get(category, {'first':'post'})


# async def save_notes(note_data):
#     data = get_notes_from_file()
#     i = len(data.keys()) + 1
#     data[i] = note_data
#     async with aiofiles.open('notes/notes.json', 'w') as tmp_file:
#         json.dump(data, tmp_file, indent=4)


# TODO: redo this
# @app.get("/notes/{category}")
# async def read_note(
#     category: Annotated[str, Path(title="The category of the notes to get")],
#     # q: Annotated[str | None, Query(alias="note-query")] = None,
# ):
#     results = await get_notes_from_file(category)
#     # if q:
#     #     results.update({"q": q})
#     return results


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/u/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)


@app.get("/u/", response_model=list[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@app.get("/u/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.post("/u/{user_id}/notes/", response_model=schemas.Note)
def create_note_for_user(
    user_id: int, note: schemas.NoteCreate, db: Session = Depends(get_db)
):
    return crud.create_user_note(db=db, note=note, user_id=user_id)


# @app.get("/notes/", response_model=list[schemas.Note])
# def read_notes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
#     notes = crud.get_notes(db, skip=skip, limit=limit)
#     return notes


@app.post("/c/}", response_model=schemas.Category)
def create_category(category: schemas.CategoryCreate, db: Session = Depends(get_db)):
    db_category = crud.get_category_by_title(db, title=category.title)
    if db_category:
        raise HTTPException(status_code=400, detail="Title already registered")
    return crud.create_category(db=db, category=category)


@app.get("/c/", response_model=list[schemas.Category])
def read_categories(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    notes = crud.get_categories(db, skip=skip, limit=limit)
    return notes


@app.get("/c/{category}", response_model=list[schemas.Note])
def read_notes_from_category(
    category: str = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    notes = crud.get_notes_from_category(
        db, category=category, skip=skip, limit=limit
    )
    return notes


# @app.post("/c/{category_name}}", response_model=schemas.Note)
@app.post("/c/{category}", response_model=schemas.Note)
def post_new_note(
    category: str = None,
    note: schemas.Note = None,
    post: str = "new",
    db: Session = Depends(get_db),
):
    db_category = crud.get_category_by_title(db, title=category)
    if not db_category:
        raise HTTPException(status_code=400, detail="No existing category!")

    note.category_id = db_category.id
    return {
        "new": crud.create_user_note(db, note),
    }.get(post)
    # notes = crud.get_notes_from_category(db, category_name=category_name, skip=skip, limit=limit)
    # return note
