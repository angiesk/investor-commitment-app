from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import models, schemas
from app.db.database import get_db
from typing import List

router = APIRouter()


@router.get("/", response_model=List[schemas.Commitment])
def get_commitments(db: Session = Depends(get_db)):
    commitments = db.query(models.Commitment).all()
    return commitments


@router.get("/{commitment_id}", response_model=schemas.Commitment)
def get_commitment(commitment_id: int, db: Session = Depends(get_db)):
    commitment = (
        db.query(models.Commitment)
        .filter(models.Commitment.id == commitment_id)
        .first()
    )
    if commitment is None:
        raise HTTPException(status_code=404, detail="Commitment not found")
    return commitment


@router.post("/commitments/bulk/", response_model=List[schemas.Commitment])
def create_multiple_commitments(
    multiple_commitments: schemas.BulkCommitmentsCreate, db: Session = Depends(get_db)
):
    # Look for the investor using their email
    db_investor = (
        db.query(models.Investor)
        .join(models.User)
        .filter(models.User.email == multiple_commitments.investor_email)
        .first()
    )

    if not db_investor:
        raise HTTPException(status_code=404, detail="Investor not found")

    created_commitments = []
    total_commitment = 0

    # Iterate through the commitments and create each one
    for commitment in multiple_commitments.commitments:
        db_commitment = models.Commitment(
            investor_id=db_investor.id,
            asset_class=commitment.asset_class,
            amount=commitment.amount,
            currency=commitment.currency,
        )
        db.add(db_commitment)
        db.commit()
        db.refresh(db_commitment)

        # Update the total commitment for the investor
        total_commitment += commitment.amount

        created_commitments.append(db_commitment)

    # Update the total commitment for the investor after all commitments are added
    # db_investor.total_commitment = total_commitment
    db.add(db_investor)
    db.commit()
    db.refresh(db_investor)

    return created_commitments
