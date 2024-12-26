from sqlalchemy import Column, Integer, String, Date, Enum, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from enum import Enum as PyEnum
from src.database import Base

class LegislatorPosition(PyEnum):  
    SENATOR = "Senator"
    REPRESENTATIVE = "Representative"

class LegislatorParty(PyEnum):     
    DEMOCRATIC = "Democratic"
    REPUBLICAN = "Republican"
    INDEPENDENT = "Independent"

class Legislator(Base):
    __tablename__ = "legislators"

    id = Column(Integer, primary_key=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    party = Column(Enum(LegislatorParty), nullable=False)  
    state = Column(String(2), nullable=False)
    position = Column(Enum(LegislatorPosition), nullable=False)  
    term_start_date = Column(Date, nullable=False)
    term_end_date = Column(Date)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


    # Relationships
    trades = relationship("Trade", back_populates="legislator")
    committee_memberships = relationship("CommitteeMembership", back_populates="legislator")
