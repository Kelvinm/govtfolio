from sqlalchemy import Column, Integer, String, Date, ForeignKey, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from src.database import Base

class Committee(Base):
    __tablename__ = "committees"
    
    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False, unique=True)
    subject_matter = Column(String(200))
    url = Column(String(500))

    # Note the combination of server_default and onupdate:
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),     # sets a default when the record is first inserted
        nullable=False
    )
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),     # sets a default on insert
        onupdate=func.now(),           # automatically updates this column on UPDATE
        nullable=False
    )

    # Relationships
    memberships = relationship("CommitteeMembership", back_populates="committee")


class CommitteeMembership(Base):
    __tablename__ = "committee_memberships"
    
    id = Column(Integer, primary_key=True)
    committee_id = Column(Integer, ForeignKey("committees.id"))
    legislator_id = Column(Integer, ForeignKey("legislators.id"))
    membership_start_date = Column(Date, nullable=False)
    membership_end_date = Column(Date)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )

    # Relationships
    committee = relationship("Committee", back_populates="memberships")
    legislator = relationship("Legislator", back_populates="committee_memberships")
