from datetime import date, datetime
from enum import Enum
from typing import Optional
from pydantic import BaseModel


class OpportunityType(str, Enum):
    job = "job"
    internship = "internship"
    scholarship = "scholarship"
    graduate_program = "graduate_program"


class OpportunityStatus(str, Enum):
    discovered = "discovered"
    saved = "saved"
    applying = "applying"
    applied = "applied"
    interviewing = "interviewing"
    offered = "offered"
    rejected = "rejected"
    withdrawn = "withdrawn"


class OpportunityBase(BaseModel):
    title: str
    organization: str
    opportunity_type: OpportunityType
    status: OpportunityStatus = OpportunityStatus.discovered
    deadline: Optional[date] = None
    url: Optional[str] = None
    notes: Optional[str] = None


class OpportunityCreate(OpportunityBase):
    pass


class OpportunityUpdate(BaseModel):
    title: Optional[str] = None
    organization: Optional[str] = None
    opportunity_type: Optional[OpportunityType] = None
    status: Optional[OpportunityStatus] = None
    deadline: Optional[date] = None
    url: Optional[str] = None
    notes: Optional[str] = None


class OpportunityResponse(OpportunityBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
