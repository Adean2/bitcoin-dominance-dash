import pandas as pd
import requests
from datetime import datetime
from pathlib import Path


def load_processed_data(processed_csv_path):
    # Load existing merged Bitcoin dominance data
    if processed_csv_path.exists():
        df = pd.read_csv(processed_csv_path, parse_dates=['date'])
    else:
        df = pd.DataFrame(columns=['date', 'bitcoin_market_cap', 'total_market_cap', 'bitcoin_dominance'])
    return df


def fetch_latest_total_market_cap():
    # Fetch latest total crypto market cap USD from CoinGecko global API
    url = "https://api.coingecko.com/api/v3/global"
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    return data['data']['total_market_cap']['usd']


def fetch_latest_bitcoin_market_cap():
    # Fetch latest Bitcoin market cap USD from CoinGecko.
    url = "https://api.coingecko.com/api/v3/coins/bitcoin"
    params = {
        'localization': 'false',
        'tickers': 'false',
        'market_data': 'true',
        'community_data': 'false',
        'developer_data': 'false',
        'sparkline': 'false'
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()
    return data['market_data']['market_cap']['usd']


def update_with_latest_day(processed_csv_path):
    
    df = load_processed_data(processed_csv_path)

    # Get last date in existing data
    last_date = df['date'].max().date() if not df.empty else None

    # Use current UTC date as the 'latest' date to record
    latest_date = datetime.utcnow().date()

    # Check if today's data is already present
    if last_date == latest_date:
        print(f"Data is already up to date for {latest_date}")
        return df

    # Fetch latest market caps
    total_market_cap = fetch_latest_total_market_cap()
    bitcoin_market_cap = fetch_latest_bitcoin_market_cap()

    # Calculate dominance %
    bitcoin_dominance = (bitcoin_market_cap / total_market_cap) * 100

    
    new_row = {
        'date': pd.Timestamp(latest_date),
        'bitcoin_market_cap': bitcoin_market_cap,
        'total_market_cap': total_market_cap,
        'bitcoin_dominance': bitcoin_dominance
    }

    # Append new row to dataframe
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)

    # Sort and reset index
    df.sort_values('date', inplace=True)
    df.reset_index(drop=True, inplace=True)

    # Ensure directory exists
    processed_csv_path.parent.mkdir(parents=True, exist_ok=True)

    # Save
    df.to_csv(processed_csv_path, index=False)

    print(f"Added new data for {latest_date}, saved to {processed_csv_path}")

    return df


def main():
    processed_csv_path = Path('data/merged/bitcoin_dominance_updated.csv')
    update_with_latest_day(processed_csv_path)


if __name__ == "__main__":
    main()
