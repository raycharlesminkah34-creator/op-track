from sqlalchemy import Column, Date, DateTime, Integer, String, Text
from sqlalchemy.sql import func
from app.database import Base


class Opportunity(Base):
    __tablename__ = "opportunities"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    organization = Column(String(255), nullable=False)
    opportunity_type = Column(String(50), nullable=False)
    status = Column(String(50), nullable=False, default="discovered")
    deadline = Column(Date, nullable=True)
    url = Column(Text, nullable=True)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(
        DateTime,
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    def __repr__(self) -> str:
        return (
            f"<Opportunity id={self.id!r} title={self.title!r} "
            f"status={self.status!r}>"
        )
