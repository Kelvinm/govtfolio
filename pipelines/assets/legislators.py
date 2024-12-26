# pipelines/assets/legislators.py
from dagster import asset, AssetExecutionContext


import pandas as pd
from src.models.legislator import Legislator
from src.database import SessionLocal

@asset
def staged_legislators(context: AssetExecutionContext, 
                      raw_legislator_securities: dict) -> pd.DataFrame:
    """Store legislator data"""
    legislators_df = raw_legislator_securities['legislators']

    # # Debug logging
    # null_party = legislators_df[legislators_df['party'].isnull()]
    # if not null_party.empty:
    #     context.log.warn(f"Found legislators with null party: {null_party.to_dict('records')}")
    

    with SessionLocal() as db:
        for _, row in legislators_df.iterrows():
            legislator = Legislator(
                first_name=row['name'].split()[0],
                last_name=' '.join(row['name'].split()[1:]),
                party = row['party'].upper() if pd.notna(row['party']) else 'INDEPENDENT',
                state=row['state'],
                position=row['chamber']
            )
            db.merge(legislator)
        db.commit()
    return legislators_df

assets = [staged_legislators]