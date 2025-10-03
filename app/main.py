# app/main.py
from fastapi import FastAPI, Depends, HTTPException, Query, Path
from sqlmodel import Session, select, func
from typing import List, Optional

from app.database import get_session
from app.models import (
    Investor, Commitment, InvestorSummary, 
    CommitmentRead, AssetClassSummary
)

app = FastAPI(
    title="BlackRock - Investor Commitments API",
    description="API to manage investor commitments across different asset classes",
    version="1.0.0"
)

@app.get("/", summary="Root endpoint")
def read_root(session: Session = Depends(get_session)):
    """Welcome message for the API"""
    
    # Query investors from database
    investors = session.exec(
        select(Investor.id, Investor.name)
        .order_by(Investor.name)
    ).all()
    
    # Convert to list of dictionaries
    investor_list = [
        {"id": investor.id, "name": investor.name} 
        for investor in investors
    ]
    
    return {
        "message": "BlackRock - Investor Commitments API", 
        "docs": "/docs",
        "endpoints": ["/investors", "/asset-classes", "/investors/{investor_id}/summary", "/investors/{investor_id}/commitments", "/investors/{investor_id}/commitments/filter?asset_class=Hedge%20Funds"],
        "available_investors": investor_list,
        "total_investors": len(investor_list)
    }

@app.get("/investors", response_model=List[InvestorSummary], summary="Get all investors with total commitments")
def get_investors(session: Session = Depends(get_session)):
    """
    Retrieve all investors with their total commitment amounts.
    Investors are ordered alphabetically by name.
    """
    # Query to get investors with their total commitments
    statement = (
        select(
            Investor.id,
            Investor.name,
            Investor.type,
            Investor.country,
            Investor.date_added,
            func.sum(Commitment.amount).label("total_commitment")
        )
        .join(Commitment)
        .group_by(Investor.id)
        .order_by(Investor.name)
    )
    
    results = session.exec(statement).all()
    
    return [
        InvestorSummary(
            id=result.id,
            name=result.name,
            type=result.type,
            country=result.country,
            date_added=result.date_added,
            total_commitment=result.total_commitment
        )
        for result in results
    ]

@app.get("/investors/{investor_id}/commitments", response_model=List[CommitmentRead], 
         summary="Get commitments for a specific investor")
def get_investor_commitments(
    investor_id: int,
    asset_class: Optional[str] = Query(None, description="Filter by asset class"),
    session: Session = Depends(get_session)
):
    """
    Retrieve all commitments for a specific investor.
    Optionally filter by asset class.
    """
    # Check if investor exists
    investor = session.get(Investor, investor_id)
    if not investor:
        raise HTTPException(status_code=404, detail=f"Investor with ID {investor_id} not found")
    
    # Build query for commitments
    statement = select(Commitment).where(Commitment.investor_id == investor_id)
    
    if asset_class:
        statement = statement.where(Commitment.asset_class == asset_class)
    
    commitments = session.exec(statement).all()
    
    return commitments


@app.get("/asset-classes", response_model=List[str], summary="Get all available asset classes")
def get_asset_classes(session: Session = Depends(get_session)):
    """Retrieve all unique asset classes available in the system."""
    statement = select(Commitment.asset_class).distinct()
    asset_classes = session.exec(statement).all()
    return sorted(asset_classes)



@app.get("/investors/{investor_id}/summary", response_model=List[AssetClassSummary], 
         summary="Get investor commitment summary by asset class")
def get_investor_asset_summary(
    investor_id: int,
    session: Session = Depends(get_session)
):
    """
    Get the sum of commitments for each asset class for a specific investor.
    Returns total commitment amount and count of commitments per asset class.
    """
    
    # Check if investor exists
    investor = session.get(Investor, investor_id)
    if not investor:
        raise HTTPException(
            status_code=404, 
            detail=f"Investor with ID {investor_id} not found"
        )
    
    # Group by asset class and sum commitments
    statement = (
        select(
            Commitment.asset_class,
            func.sum(Commitment.amount).label("total_commitment"),
            func.count(Commitment.id).label("commitment_count")
        )
        .where(Commitment.investor_id == investor_id)
        .group_by(Commitment.asset_class)
        .order_by(func.sum(Commitment.amount).desc())  # Order by total commitment (highest first)
    )
    
    results = session.exec(statement).all()
    
    if not results:
        return []  # Return empty list if no commitments found
    
    return [
        AssetClassSummary(
            asset_class=result.asset_class,
            total_commitment=float(result.total_commitment),
            commitment_count=result.commitment_count
        )
        for result in results
    ]


@app.get(
    "/investors/{investor_id}/commitments/filter",
    response_model=List[CommitmentRead],
    summary="Commitments filtered by investor and asset class"
)
def get_commitments_by_investor_and_asset(
    investor_id: int = Path(..., description="Investor ID"),
    asset_class: str = Query(..., description="Asset class to filter by"),
    session: Session = Depends(get_session)
):
    """
    Return all commitments that belong to the *given* investor **and**
    match the required *asset_class*.
    """
    # validate that the investor exists
    if session.get(Investor, investor_id) is None:
        raise HTTPException(
            status_code=404,
            detail=f"Investor with ID {investor_id} not found"
        )

    # query commitments with BOTH conditions
    stmt = (
        select(Commitment)
        .where(
            Commitment.investor_id == investor_id,
            Commitment.asset_class == asset_class
        )
        .order_by(Commitment.amount.desc())          # (optional) largest first
    )
    results = session.exec(stmt).all()

    return results
