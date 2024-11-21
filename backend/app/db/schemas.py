from pydantic import BaseModel, EmailStr
from typing import List, Optional

from app.commons import InvestorType, UserType, AssetClass


class CommitmentBase(BaseModel):
    asset_class: str
    amount: float
    currency: str


class Commitment(CommitmentBase):
    id: int

    class Config:
        orm_mode = True


class InvestorBase(BaseModel):
    name: str
    country: str
    email: EmailStr
    investor_type: InvestorType


class InvestorCreate(InvestorBase):
    commitments: List[CommitmentBase]


class Investor(InvestorBase):
    id: int
    commitments: List[Commitment] = []

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    name: str
    country: str
    email: EmailStr
    user_type: UserType  # Use enum for user_type


class UserCreate(UserBase):
    pass


class User(UserBase):
    id: int
    investors: Investor = []  # Linking with Investor

    class Config:
        orm_mode = True


# You could potentially keep a different model for creating investors with related user information
class InvestorCreateWithUser(BaseModel):
    name: str
    country: str
    total_commitment: float
    asset_class: str
    user_id: Optional[int] = None
    email: Optional[EmailStr] = None  # Email field is optional

    class Config:
        orm_mode = True


class CommitmentCreate(BaseModel):
    asset_class: str
    amount: float
    currency: str = "GBP"  # Defaulting to GBP


class BulkCommitmentsCreate(BaseModel):
    investor_email: EmailStr  # Email of the investor
    commitments: List[CommitmentCreate]
