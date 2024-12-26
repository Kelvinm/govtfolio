from urllib.parse import urljoin

import requests
from dagster import asset, AssetExecutionContext
import pandas as pd
from bs4 import BeautifulSoup

from src.utils import convert_dates
from src.database import SessionLocal
from src.models.committee import Committee


@asset
def committees_from_db(context: AssetExecutionContext) -> pd.DataFrame:
    """
    Reads all committees from the database and returns a DataFrame.
    """
    with SessionLocal() as db:
        committees = db.query(Committee).all()

    if not committees:
        context.log.warn("No committees found in DB.")
        return pd.DataFrame()

    data = []
    for c in committees:
        data.append({
            'id': c.id,
            'name': c.name,
            'url': c.url,  # Assuming you have a url column on Committee
        })
    df = pd.DataFrame(data)
    
    context.add_output_metadata({
        "num_committees_in_db": len(df),
        "sample": df.head(3).to_dict(orient="records"),
    })

    return df



def extract_trade_table_with_links(base_url):
    response = requests.get(base_url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')
    table = soup.find('table')  # Modify selector if needed
    
    title = soup.find('h1').get_text(strip=True)
    df = pd.read_html(str(table))[0]

    detail_links = []
    tickers = []
    currencies = []
    names = []
    parties = []
    chambers = []
    states = []
    issuers = []

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
        party, chamber, state = split_name_string(row.find('div', class_='politician-info').get_text(strip=True))
        
        names.append(row.find('h2', class_='politician-name').get_text(strip=True))
        issuers.append( row.find(class_ = 'issuer-name').get_text(strip=True))
        parties.append(party)
        chambers.append(chamber)    
        states.append(state)
        tickers.append(ticker)
        currencies.append(currency)

    df['committee'] = title
    df['party'], df['chamber'], df['state'] = parties, chambers, states
    df['issuer'] = issuers
    df['name'] = names
    df['detail_link'] = detail_links
    df['ticker'] = tickers
    df['currency'] = currencies
    df = convert_dates(df, ['Published', 'Traded'])  # Convert date columns to datetime    

    # Convert all column names to lower case
    df.columns = df.columns.str.lower()

    return df[['committee', 'name', 'party', 'chamber', 'state', 'issuer', 'ticker', 'currency', 'published', 'traded', 'type', 'size', 'detail_link']]


@asset
def raw_legislator_securities(context: AssetExecutionContext, committees_from_db: pd.DataFrame) -> pd.DataFrame:
    """
    For each committee's URL, fetch the detail page, parse trades (legislators, securities, etc.).
    Returns a DataFrame of combined results.
    """
    if committees_from_db.empty:
        context.log.warn("No committees to process for legislator/securities data.")
        return pd.DataFrame()

    all_rows = []

    for _, row in committees_from_db.iterrows():
        url = row.get("url")
        if not url:
            continue
        
        try:
            resp = requests.get(url, timeout=10)
            resp.raise_for_status()
            
            # Parse the detail page:
            detail_df = extract_trade_table_with_links(resp, base_url="https://www.capitoltrades.com")
            
            # Tag these rows with committee info
            detail_df["committee_id"] = row["id"]
            detail_df["committee_name"] = row["name"]

            all_rows.append(detail_df)
        except requests.RequestException as e:
            context.log.error(f"Failed to fetch detail for committee {row['name']}: {e}")
        except Exception as e:
            context.log.error(f"Error parsing detail for committee {row['name']}: {e}")

    if not all_rows:
        return pd.DataFrame()

    combined_df = pd.concat(all_rows, ignore_index=True)

    context.add_output_metadata({
        "num_detail_rows": len(combined_df),
        "sample": combined_df.head(3).to_dict(orient="records"),
    })

    return combined_df

def split_name_string(s):
    if 'Republican' in s:
        party = 'Republican'
    elif 'Democrat' in s:
        party = 'Democrat'
    else:
        party = None

    if 'Senate' in s:
        chamber = 'Senate'
    elif 'House' in s:
        chamber = 'House'
    else:
        chamber = None

    state = s[-2:]
    return party, chamber, state
