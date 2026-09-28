from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.crud import opportunity as crud_opportunity
from app.schemas.opportunity import (
    OpportunityCreate,
    OpportunityResponse,
    OpportunityStatus,
    OpportunityType,
    OpportunityUpdate,
)

router = APIRouter()


@router.post(
    "",
    response_model=OpportunityResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new opportunity",
)
@router.post(
    "/",
    response_model=OpportunityResponse,
    status_code=status.HTTP_201_CREATED,
    include_in_schema=False,
)
def create_opportunity(
    opportunity: OpportunityCreate,
    db: Session = Depends(get_db),
):
    return crud_opportunity.create_opportunity(db=db, opportunity=opportunity)


@router.get(
    "",
    response_model=List[OpportunityResponse],
    summary="Get all opportunities",
)
@router.get(
    "/",
    response_model=List[OpportunityResponse],
    include_in_schema=False,
)
def get_opportunities(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    status_filter: Optional[OpportunityStatus] = Query(None, alias="status"),
    opportunity_type: Optional[OpportunityType] = Query(None),
    search: Optional[str] = Query(None),
    db: Session = Depends(get_db),
):
    return crud_opportunity.get_opportunities(
        db=db,
        skip=skip,
        limit=limit,
        status=status_filter,
        opportunity_type=opportunity_type,
        search=search,
    )


@router.get(
    "/{id}",
    response_model=OpportunityResponse,
    summary="Get opportunity by ID",
)
def get_opportunity(
    id: int,
    db: Session = Depends(get_db),
):
    opportunity = crud_opportunity.get_opportunity_by_id(db=db, opportunity_id=id)
    if not opportunity:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Opportunity with ID {id} not found",
        )
    return opportunity


@router.patch(
    "/{id}",
    response_model=OpportunityResponse,
    summary="Update an opportunity",
)
def patch_opportunity(
    id: int,
    opportunity_update: OpportunityUpdate,
    db: Session = Depends(get_db),
):
    db_opportunity = crud_opportunity.get_opportunity_by_id(db=db, opportunity_id=id)
    if not db_opportunity:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Opportunity with ID {id} not found",
        )
    return crud_opportunity.update_opportunity(
        db=db,
        db_opportunity=db_opportunity,
        update_data=opportunity_update,
    )


@router.delete(
    "/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete an opportunity",
)
def delete_opportunity(
    id: int,
    db: Session = Depends(get_db),
):
    db_opportunity = crud_opportunity.get_opportunity_by_id(db=db, opportunity_id=id)
    if not db_opportunity:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Opportunity with ID {id} not found",
        )
    crud_opportunity.delete_opportunity(db=db, db_opportunity=db_opportunity)
    return None
