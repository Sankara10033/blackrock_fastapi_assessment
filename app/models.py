# app/models.py
from sqlmodel import SQLModel, Field, Relationship, Index
from pydantic import field_serializer
from typing import Optional, List
from datetime import date

class InvestorBase(SQLModel):
    name: str = Field(index=True)
    type: str
    country: str
    date_added: date

class Investor(InvestorBase, table=True):
    __tablename__ = "investors"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    
    # Relationship to commitments
    commitments: List["Commitment"] = Relationship(back_populates="investor")


class InvestorSummary(SQLModel):
    # ID comes first by defining it first
    id: int
    name: str
    type: str
    country: str
    date_added: date
    total_commitment: float
    
    @field_serializer('total_commitment')
    def format_total_commitment(self, value: float) -> str:
        """Format total commitment in M (millions) or B (billions)"""
        if value >= 1000000000:  # 1 billion = 1000M
            return f"{value/1000000000:.1f}B"
        else:
            return f"{value/1000000:.1f}M"

class CommitmentBase(SQLModel):
    asset_class: str = Field(index=True)
    amount: float
    currency: str

class Commitment(CommitmentBase, table=True):
    __tablename__ = "commitments"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    investor_id: int = Field(foreign_key="investors.id", index=True)
    
    # Relationship to investor
    investor: Optional[Investor] = Relationship(back_populates="commitments")
    
    # Composite index for common query patterns
    __table_args__ = (
        Index('idx_investor_asset', 'investor_id', 'asset_class'),  # For filtering commitments by investor + asset class
    )

class CommitmentRead(SQLModel):
    # ID comes first by defining it first
    id: int
    investor_id: int
    asset_class: str
    amount: float
    currency: str
    
    @field_serializer('amount')
    def format_amount(self, value: float) -> str:
        """Format amount in M (millions) or B (billions)"""
        if value >= 1000000000:  # 1 billion = 1000M
            return f"{value/1000000000:.1f}B"
        else:
            return f"{value/1000000:.1f}M"


class AssetClassSummary(SQLModel):
    asset_class: str
    total_commitment: float
    commitment_count: int

    @field_serializer('total_commitment')
    def format_total_commitment(self, value: float) -> str:
        """Format total commitment in M (millions) or B (billions)"""
        if value >= 1000000000:  # 1 billion = 1000M
            return f"{value/1000000000:.1f}B"
        else:
            return f"{value/1000000:.1f}M"
