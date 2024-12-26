from dagster import Definitions
from .committees import raw_committees, staged_committees
from .trading_activity import committees_from_db, raw_legislator_securities
from .legislators import staged_legislators
from .trades import staged_trades

defs = Definitions(
    assets=[
        raw_committees, 
        staged_committees,
        committees_from_db,
        raw_legislator_securities,
        staged_legislators,
        staged_trades
    ]
)