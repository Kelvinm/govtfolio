# pipelines/assets/committees.py

from dagster import asset, AssetExecutionContext, MetadataValue, RetryPolicy
from src.models.committee import Committee
from src.database import SessionLocal
from bs4 import BeautifulSoup
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import pandas as pd
from datetime import datetime
from sqlalchemy.exc import IntegrityError

def create_session_with_retries():
    session = requests.Session()
    retries = Retry(
        total=3,
        backoff_factor=0.5,
        status_forcelist=[500, 502, 503, 504]
    )
    session.mount('https://', HTTPAdapter(max_retries=retries))
    return session

def extract_committee_data(html):
    soup = BeautifulSoup(html, 'html.parser')
    committees = []
    
    links = soup.find_all('a', class_='index-card-link')
    
    for link in links:
        url = f"https://www.capitoltrades.com{link['href']}"
        name = link.get_text(strip=True).split('Trades')[0]
        # For subject matter, need to traverse up and find sibling or parent element
        # Will need to inspect HTML structure for accurate path
        
        committees.append({
            'name': name,
            'url': url,
            'created_at': datetime.now(),
            'updated_at': datetime.now()
        })

    return committees

@asset(
    retry_policy=RetryPolicy(max_retries=3, delay=30)
)
def raw_committees(context: AssetExecutionContext) -> pd.DataFrame:
    """Extract raw committee data from CapitolTrades.com"""
    url = "https://www.capitoltrades.com/committees"
    session = create_session_with_retries()
    
    try:
        response = session.get(url, timeout=10)
        response.raise_for_status()
        
        committees = extract_committee_data(response.text)
        
        if not committees:
            raise ValueError("No committee data found on page")
        
        df = pd.DataFrame(committees)
        
        context.add_output_metadata({
            "num_committees": MetadataValue.int(len(df)),
            "preview": MetadataValue.md(df.head().to_markdown())
        })
        
        return df
        
    except requests.exceptions.RequestException as e:
        context.log.error(f"Error fetching committee data: {str(e)}")
        raise
    finally:
        session.close()
@asset
def staged_committees(context: AssetExecutionContext, raw_committees: pd.DataFrame) -> pd.DataFrame:
    if raw_committees.empty:
        context.log.warn("No committee data to stage")
        return pd.DataFrame()

    df = raw_committees.copy()
    df['name'] = df['name'].str.strip()
    df['subject_matter'] = "to be added later"
    
    inserted = 0
    updated = 0
    errors = 0

    with SessionLocal() as db:
        for _, row in df.iterrows():
            try:
                existing_committee = (
                    db.query(Committee)
                    .filter(Committee.name == row['name'])
                    .one_or_none()
                )

                if existing_committee:
                    # Update existing
                    existing_committee.subject_matter = row['subject_matter']
                    existing_committee.url = row['url']
                    # updated_at should be handled automatically if you set onupdate=func.now()
                    updated += 1
                else:
                    # Insert new
                    committee = Committee(
                        name=row['name'],
                        subject_matter=row['subject_matter'],
                        url=row['url'],
                    )
                    db.add(committee)
                    inserted += 1

                db.commit()

            except IntegrityError as e:
                db.rollback()
                context.log.error(
                    f"Error upserting committee {row['name']}: {str(e)}"
                )
                errors += 1
            except Exception as e:
                db.rollback()
                context.log.error(
                    f"Unexpected error processing committee {row['name']}: {str(e)}"
                )
                errors += 1

    context.add_output_metadata({
        "records_processed": MetadataValue.int(len(df)),
        "records_updated": MetadataValue.int(updated),
        "records_inserted": MetadataValue.int(inserted),
        "errors": MetadataValue.int(errors)
    })
    
    return df


if __name__ == "__main__":
    
    url = "https://www.capitoltrades.com/committees"
    response = requests.get(url)
    data = extract_committee_data(response.text)
    
    print("\nFound committees:")
    for committee in data:
        print(f"Name: {committee['name']}")
        print(f"URL: {committee['url']}")
        print("---")
