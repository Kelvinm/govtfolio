from datetime import datetime 

import pandas as pd


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


def calculate_percentage_change(df):
    df['%change'] = df['close'].pct_change() * 100
    return df