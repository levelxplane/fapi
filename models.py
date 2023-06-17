from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship

from database import Base


class User(Base):
    __tablename__ = "User"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime)

    notes = relationship("Note", back_populates="owner")
    # categories = relationship("Category", back_populates="owner")


class Category(Base):
    __tablename__ = "Category"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    created_at = Column(DateTime)
    # owner_id = Column(Integer, ForeignKey("User.id"))

    # owner = relationship("User", back_populates="categories")
    
    
class Note(Base):
    __tablename__ = "Note"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    parent_id = Column(Integer, ForeignKey("Note.id"), index=True, nullable=True)
    category_id = Column(Integer, ForeignKey("Category.id"), index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    owner_id = Column(Integer, ForeignKey("User.id"))
    created_at = Column(DateTime)



    owner = relationship("User", back_populates="notes")