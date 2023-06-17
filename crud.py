from sqlalchemy.orm import Session

import models, schemas

from models import Note, Category, User


def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = models.User(email=user.email, hashed_password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def create_category(db: Session, category: schemas.CategoryCreate):
    new_category = models.Category(
        title=category.title,
        description=category.description if category.description else f'A category for dicussing {category.title}',
        # owner_id=user_id
    )
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    return new_category


def get_notes_from_category(db: Session, category: str, parent: int = 0, skip: int = 0, limit: int = 100):
    return db.query(Note).filter(Category.title == category, Note.parent_id == parent).all()

def get_notes(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Note).offset(skip).limit(limit).all()

def get_category_by_title(db: Session, title: str = None):
    return db.query(Category).filter(Category.title == title).first()
    
def get_categories(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Category).offset(skip).limit(limit).all()
    

def create_user_note(db: Session, note: schemas.NoteCreate):

    tmp_note = note.dict()
    tmp_note.pop('id')
    db_note = models.Note(**tmp_note)
    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    return db_note
