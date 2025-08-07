import pandas as pd
import matplotlib.pyplot as plt
import os


def visualize(data_path=None):
    if data_path is None:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        data_path = os.path.join(script_dir, '..', 'data', 'processed', 'bitcoin_dominance_processed.csv')
    
    print("Loading data from:", data_path)
    
    df = pd.read_csv(data_path)
    
    # Print columns for debugging
    print("Columns found in CSV:", df.columns.tolist())
    
    # Converted the 'date' column to datetime
    df['date'] = pd.to_datetime(df['date'])
    
    plt.figure(figsize=(10, 5))
    plt.plot(df['date'], df['bitcoin_dominance'], marker='o', linestyle='-', color='orange')
    plt.title('Bitcoin Dominance Over Time')
    plt.xlabel('Date')
    plt.ylabel('Bitcoin Dominance (%)')
    plt.grid(True)
    plt.tight_layout()
    
    # Save plot image
    output_path = os.path.join(script_dir, '..', 'data', 'btc_dominance_plot.png')
    plt.savefig(output_path)
    plt.show()
    
    print(f"Chart displayed and saved as {output_path}")


if __name__ == "__main__":
    visualize()
