import pandas as pd
from pathlib import Path


def load_data(file_path):
    try:
        df = pd.read_csv(file_path, parse_dates=['date'])
        if df['bitcoin_dominance'].isnull().any():
            print("Warning: Missing values found in bitcoin_dominance column.")
        return df
    except FileNotFoundError:
        print(f"Error: File not found: {file_path}")
        raise


def summary_statistics(df):
    stats = {
        'start_date': df['date'].min(),
        'end_date': df['date'].max(),
        'min_dominance': df['bitcoin_dominance'].min(),
        'max_dominance': df['bitcoin_dominance'].max(),
        'mean_dominance': df['bitcoin_dominance'].mean(),
        'median_dominance': df['bitcoin_dominance'].median()
    }
    return stats


def additional_processing(df, rolling_window=30):
    df['rolling_avg'] = df['bitcoin_dominance'].rolling(window=rolling_window).mean()
    return df


def process_and_save(rolling_window=30):
    data_path = Path('data') / 'merged' / 'bitcoin_dominance_updated.csv'
    df = load_data(data_path)

    stats = summary_statistics(df)
    print("Bitcoin Dominance Summary Statistics:")
    for key, value in stats.items():
        print(f"{key}: {value}")

    df_processed = additional_processing(df, rolling_window=rolling_window)

    output_path = Path('data') / 'processed' / 'bitcoin_dominance_processed.csv'
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df_processed.to_csv(output_path, index=False)
    print(f"Processed data saved to {output_path}")

    return df_processed


def main():
    process_and_save()


if __name__ == "__main__":
    main()
