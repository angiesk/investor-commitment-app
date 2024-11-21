from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import models, schemas
from app.db.database import get_db
from typing import List
from sqlalchemy.exc import IntegrityError
from app.commons import InvestorType, UserType
from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

router = APIRouter()


@router.get("/", response_model=List[schemas.Investor])
def get_investors(db: Session = Depends(get_db)):
    investors = db.query(models.Investor).all()
    return investors


@router.get("/{investor_id}", response_model=schemas.Investor)
def get_investor(investor_id: int, db: Session = Depends(get_db)):
    investor = (
        db.query(models.Investor).filter(models.Investor.id == investor_id).first()
    )
    if investor is None:
        raise HTTPException(status_code=404, detail="Investor not found")
    return investor


@router.post("/investors/", response_model=schemas.Investor)
def create_investor(investor: schemas.InvestorCreate, db: Session = Depends(get_db)):
    # Ensure either user_id or email is provided
    if not investor.email:
        raise HTTPException(
            status_code=400, detail="Either user_id or email must be provided."
        )

    # Check if user with the given email already exists
    db_user = db.query(models.User).filter(models.User.email == investor.email).first()

    # If no user is found with the given email, create a new user
    if not db_user:
        db_user = models.User(
            name=investor.name,
            country=investor.country,
            user_type=UserType.INVESTOR,  # Ensure user_type is an enum
            email=investor.email,
        )
        db.add(db_user)
        try:
            db.commit()  # Commit the user to the DB
            db.refresh(db_user)  # Refresh to get the user ID after commit
        except IntegrityError:
            db.rollback()
            raise HTTPException(status_code=500, detail="Error saving user data.")

    # Check if the investor already exists based on user_id
    db_investor = (
        db.query(models.Investor).filter(models.Investor.user_id == db_user.id).first()
    )

    # If no investor exists, create a new investor entry and associate it with the user
    if not db_investor:
        db_investor = models.Investor(
            name=investor.name,
            investor_type=InvestorType(investor.investor_type),
            country=investor.country,
            email=investor.email,
            user_id=db_user.id,  # Linking the user_id to the investor
        )
        db.add(db_investor)
        try:
            db.commit()  # Commit the investor to the DB
            db.refresh(db_investor)  # Refresh to get the investor details after commit
        except IntegrityError:
            db.rollback()
            raise HTTPException(status_code=500, detail="Error saving investor data.")

    return db_investor


@router.get("/{investor_id}/commitments/", response_model=List[schemas.Commitment])
def get_investor_commitments(investor_id: int, db: Session = Depends(get_db)):
    commitments = (
        db.query(models.Commitment)
        .filter(models.Commitment.investor_id == investor_id)
        .order_by(models.Commitment.updated_at)
        .all()
    )  # Add .all() to return a list
    if not commitments:
        raise HTTPException(status_code=404, detail="Commitments not found")
    return commitments
