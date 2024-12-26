from dagster import asset, AssetExecutionContext
import pandas as pd
import numpy as np

from src.models.trade import Trade
from src.models.legislator import Legislator
from src.database import SessionLocal

@asset
def staged_trades(context: AssetExecutionContext,
                 raw_legislator_securities: dict,
                 staged_legislators: pd.DataFrame) -> pd.DataFrame:
    """Store trade data with legislator relationships"""
    trades_df = raw_legislator_securities['trades']
    trades_df = trades_df.replace({np.nan: None})
    print(trades_df.type.unique())
    with SessionLocal() as db:
        for _, row in trades_df.iterrows():
            trade = Trade(
                legislator_id=get_legislator_id(db, row['name']),
                security_ticker=row['ticker'],
                trade_date=row['traded'],
                disclosure_date=row['published'],
                trade_type=row['type'].upper(),
                amount_range=row['size']
            )
            db.add(trade)
        db.commit()
    return trades_df

def get_legislator_id(db, full_name):
    first_name = full_name.split()[0]
    last_name = ' '.join(full_name.split()[1:])
    legislator = db.query(Legislator).filter_by(
        first_name=first_name,
        last_name=last_name
    ).first()
    return legislator.id if legislator else None