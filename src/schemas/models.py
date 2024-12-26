from pydantic import BaseModel, constr
from datetime import date, datetime
from enum import Enum
from typing import Optional

# Enums (matching our SQLAlchemy models)
class LegislatorPosition(str, Enum):
    SENATOR = "Senator"
    REPRESENTATIVE = "Representative"

class LegislatorParty(str, Enum):
    DEMOCRATIC = "Democratic"
    REPUBLICAN = "Republican"
    INDEPENDENT = "Independent"

class TradeType(str, Enum):
    BUY = "buy"
    SELL = "sell"

# Base Models (for creating/updating)
class LegislatorBase(BaseModel):
    first_name: str
    last_name: str
    party: LegislatorParty
    state: constr(min_length=2, max_length=2)  # Ensures 2-letter state code
    position: LegislatorPosition
    term_start_date: date
    term_end_date: Optional[date] = None

class LegislatorCreate(LegislatorBase):
    pass

class LegislatorResponse(LegislatorBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class CommitteeBase(BaseModel):
    name: str
    subject_matter: Optional[str] = None

class CommitteeCreate(CommitteeBase):
    pass

class CommitteeResponse(CommitteeBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class CommitteeMembershipBase(BaseModel):
    committee_id: int
    legislator_id: int
    membership_start_date: date
    membership_end_date: Optional[date] = None

class CommitteeMembershipCreate(CommitteeMembershipBase):
    pass

class CommitteeMembershipResponse(CommitteeMembershipBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class TradeBase(BaseModel):
    legislator_id: int
    security_ticker: str
    trade_date: date
    disclosure_date: date
    trade_type: TradeType
    amount_range: Optional[str] = None
    volume: Optional[int] = None
    price_per_share: Optional[float] = None

class TradeCreate(TradeBase):
    pass

class TradeResponse(TradeBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

# Optional: Enhanced response models with relationships
class LegislatorWithRelations(LegislatorResponse):
    trades: list[TradeResponse] = []
    committee_memberships: list[CommitteeMembershipResponse] = []

class CommitteeWithMembers(CommitteeResponse):
    memberships: list[CommitteeMembershipResponse] = []