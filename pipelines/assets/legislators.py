# pipelines/assets/legislators.py
from dagster import asset, AssetExecutionContext
import requests
from bs4 import BeautifulSoup

import pandas as pd

from sqlalchemy.orm import Session
from src.database import engine
from src.models.legislator import Legislator

@asset
def extract_legislators():
    """
    Extract unique legislators from the trade data
    """
    # Example URL - you'll need to provide the actual URL
    base_url = "https://www.capitoltrades.com/trades"
    response = requests.get(base_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Extract unique legislators
    legislators_data = []  # This would be populated from your scraping
    
    with Session(engine) as session:
        for leg_data in legislators_data:
            legislator = Legislator(**leg_data)
            session.add(legislator)
        session.commit()

    return legislators_data




@asset
def raw_politicians(context: AssetExecutionContext, staged_committees: pd.DataFrame) -> pd.DataFrame:
    """Extract raw politician data from each committee page"""
    politicians = []
    for _, committee in staged_committees.iterrows():
        url = committee['url']
        # Scrape politician data from committee page
        # Add to politicians list
    return pd.DataFrame(politicians)

@asset
def staged_politicians(context: AssetExecutionContext, raw_politicians: pd.DataFrame):
    """Clean and load politician data into PostgreSQL"""
    # Database operations for politicians
    pass

# pipelines/assets/trades.py

@asset
def raw_trades(context: AssetExecutionContext, staged_politicians: pd.DataFrame) -> pd.DataFrame:
    """Extract trade data for each politician"""
    trades = []
    for _, politician in staged_politicians.iterrows():
        pass
        # Scrape trade data from politician page
        # Add to trades list
    return pd.DataFrame(trades)

@asset
def staged_trades(context: AssetExecutionContext, raw_trades: pd.DataFrame):
    """Clean and load trade data into PostgreSQL"""
    # Database operations for trades
    pass



assets = [extract_legislators]