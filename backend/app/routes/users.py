from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db import models, schemas
from app.db.database import get_db
from fastapi import HTTPException
from typing import List

router = APIRouter()


@router.get("/", response_model=List[schemas.User])
def get_users(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return users


@router.get("/{user_id}", response_model=schemas.User)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.post("/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = models.User(
        name=user.name, country=user.country, user_type=user.user_type, email=user.email
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
