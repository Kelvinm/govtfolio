# from .legislators import assets as legislator_assets
# from .committees import assets as committee_assets
# from .trades import assets as trade_assets

# assets = [
#     *legislator_assets,
#     *committee_assets,
#     *trade_assets,
# ]

from dagster import Definitions
from .committees import raw_committees, staged_committees

defs = Definitions(
    assets=[raw_committees, staged_committees]
)
