from typing import List, Optional
from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.models.opportunity import Opportunity
from app.schemas.opportunity import (
    OpportunityCreate,
    OpportunityStatus,
    OpportunityType,
    OpportunityUpdate,
)


def create_opportunity(db: Session, opportunity: OpportunityCreate) -> Opportunity:
    opportunity_data = opportunity.model_dump()
    db_opportunity = Opportunity(**opportunity_data)
    db.add(db_opportunity)
    db.commit()
    db.refresh(db_opportunity)
    return db_opportunity


def get_opportunity_by_id(db: Session, opportunity_id: int) -> Optional[Opportunity]:
    return db.query(Opportunity).filter(Opportunity.id == opportunity_id).first()


def get_opportunities(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    status: Optional[OpportunityStatus] = None,
    opportunity_type: Optional[OpportunityType] = None,
    search: Optional[str] = None,
) -> List[Opportunity]:
    query = db.query(Opportunity)
    if status is not None:
        query = query.filter(Opportunity.status == (status.value if hasattr(status, "value") else status))
    if opportunity_type is not None:
        query = query.filter(
            Opportunity.opportunity_type == (opportunity_type.value if hasattr(opportunity_type, "value") else opportunity_type)
        )
    if search:
        search_filter = f"%{search}%"
        query = query.filter(
            or_(
                Opportunity.title.ilike(search_filter),
                Opportunity.organization.ilike(search_filter),
                Opportunity.notes.ilike(search_filter),
            )
        )
    return query.order_by(Opportunity.id.desc()).offset(skip).limit(limit).all()


def update_opportunity(
    db: Session,
    db_opportunity: Opportunity,
    update_data: OpportunityUpdate,
) -> Opportunity:
    update_dict = update_data.model_dump(exclude_unset=True)
    for field, value in update_dict.items():
        setattr(db_opportunity, field, value)
    db.commit()
    db.refresh(db_opportunity)
    return db_opportunity


def delete_opportunity(db: Session, db_opportunity: Opportunity) -> None:
    db.delete(db_opportunity)
    db.commit()
