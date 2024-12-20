import argparse
from bs4 import BeautifulSoup
import pandas as pd
import requests
from urllib.parse import urljoin
import yfinance as yf
from datetime import datetime

import warnings

with warnings.catch_warnings():
    warnings.simplefilter(action='ignore', category=FutureWarning)

def convert_dates(df, columns):
    """
    Converts specified columns in the DataFrame to datetime format.
    Replaces entries with 'today' (case-insensitive) with the current date.

    Parameters:
    - df (pd.DataFrame): The DataFrame containing the date columns.
    - columns (list): List of column names to convert.

    Returns:
    - pd.DataFrame: DataFrame with converted date columns.
    """
    for column in columns:
        # Replace 'today' (case-insensitive) with today's date as string
        df[column] = df[column].replace(
            to_replace=r'(?i)^today$',  # Regex to match 'today' case-insensitively
            value=datetime.today().strftime('%Y-%m-%d'),
            regex=True
        )
        
        # Convert the column to datetime
        df[column] = pd.to_datetime(df[column], errors='coerce')
        
    return df

def extract_trade_table_with_links(response, base_url):
    soup = BeautifulSoup(response.text, 'html.parser')
    table = soup.find('table')  # Modify selector if needed
    df = pd.read_html(str(table))[0]

    detail_links = []
    tickers = []
    currencies = []

    for row in table.find_all('tr')[1:]:  # Skip header
        link_tag = row.find('a', href=True)
        if link_tag:
            full_url = urljoin(base_url, link_tag['href'])
            detail_links.append(full_url)
        else:
            detail_links.append(None)

        issuer_ticker_span = row.find('span', class_='q-field issuer-ticker')
        if issuer_ticker_span:
            issuer_ticker_text = issuer_ticker_span.get_text(strip=True)
            parts = issuer_ticker_text.split(':')
            if len(parts) == 2:
                ticker, currency = parts
            else:
                ticker, currency = None, None
        else:
            ticker, currency = None, None

        tickers.append(ticker)
        currencies.append(currency)

    df['detail_link'] = detail_links
    df['ticker'] = tickers
    df['currency'] = currencies
    df = convert_dates(df, ['Published', 'Traded'])  # Convert date columns to datetime    

    # Convert all column names to lower case
    df.columns = df.columns.str.lower()

    return df

def calculate_percentage_change(df):
    
    df['%change'] = df['close'].pct_change() * 100
    return df

def fetch_ticker_history(tickers, period='3mo'):
    """
    Fetches historical data for a list of tickers from yfinance and formats it into a clean DataFrame
    
    Parameters:
    ticker_series (pd.Series): Series containing tickers (can contain None values)
    period (str): Time period to fetch ('1d','5d','1mo','3mo','6mo','1y','2y','5y','10y','ytd','max')
    
    Returns:
    pd.DataFrame: Clean DataFrame with Date index and ticker data
    """
    
   
    # Download data
    df = yf.download(tickers, group_by='Ticker', period=period)
    
    # Stack and reset index
    df = df.stack(level=0).rename_axis(['Date', 'Ticker']).reset_index(level=1)
    
    # df columns to lower case
    df.columns = df.columns.str.lower()

    # index name to lower case
    df.index.name = df.index.name.lower()

    return df

# Usage example:

# filtered_list = list(filter(lambda x: x is not None, trade_df['Ticker']))
# df = fetch_ticker_history(trade_table.Ticker)
def calculate_returns(trade_df, price_df):
    """
    Calculate T+5 and T+10 returns from published date for each trade,
    excluding trades from today
    """
    
    # Convert trade_df dates to datetime and filter out today's trades
    trade_df['published'] = pd.to_datetime(trade_df['published'])
    today = pd.Timestamp.today().normalize()  # Get today's date without time
    trade_df = trade_df[trade_df['published'] < today]
    
    results = []
    
    # Group by ticker to avoid refiltering price data for each trade
    for ticker, trades in trade_df.groupby('ticker'):
        # Get price data for this ticker
        ticker_prices = price_df[price_df['ticker'] == ticker].copy()
        ticker_prices = ticker_prices.reset_index()  # Reset index to get date as column
        
        if ticker_prices.empty:
            continue
            
        for _, trade in trades.iterrows():
            pub_date = trade['published']
            
            # Find the closest trading day on or after published date
            base_price_data = ticker_prices[ticker_prices['date'] >= pub_date].iloc[0] if not ticker_prices[ticker_prices['date'] >= pub_date].empty else None
            
            if base_price_data is None:
                continue
                
            # Get base price and date
            base_date = base_price_data['date']
            base_price = base_price_data['close']
            
            # Find T+5 and T+10 prices
            t5_price = ticker_prices[ticker_prices['date'] >= (base_date + pd.Timedelta(days=5))]['close'].iloc[0] \
                if not ticker_prices[ticker_prices['date'] >= (base_date + pd.Timedelta(days=5))].empty else None
                
            t10_price = ticker_prices[ticker_prices['date'] >= (base_date + pd.Timedelta(days=10))]['close'].iloc[0] \
                if not ticker_prices[ticker_prices['date'] >= (base_date + pd.Timedelta(days=10))].empty else None
            
            # Calculate returns
            t5_return = ((t5_price - base_price) / base_price * 100) if t5_price is not None else None
            t10_return = ((t10_price - base_price) / base_price * 100) if t10_price is not None else None
            
            results.append({
                'ticker': ticker,
                'published_date': pub_date,
                'trading_date': base_date,
                'base_price': base_price,
                't5_price': t5_price,
                't10_price': t10_price,
                't5_return_%': round(t5_return, 2) if t5_return is not None else None,
                't10_return_%': round(t10_return, 2) if t10_return is not None else None
            })
    
    return pd.DataFrame(results)

def merge_trade_and_hist(trade_table, df):
    df_reset = df.reset_index()
    merged_df = pd.merge(trade_table, df_reset, on=['ticker', 'date'], how='inner')
    return merged_df

def main(base_url):
    response = requests.get(base_url)
    response.raise_for_status()

    trade_table = extract_trade_table_with_links(response, base_url)
    print(trade_table)
    filtered_list = list(filter(lambda x: x is not None, trade_table['ticker']))
    hist_df = fetch_ticker_history(filtered_list, period='3mo')
        
    percentage_changes = calculate_returns(trade_table, hist_df)
    print(percentage_changes)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process trade data from a given base URL.")
    parser.add_argument('base_url', type=str, help='The base URL to fetch trade data from.')
    args = parser.parse_args()
    main(args.base_url)