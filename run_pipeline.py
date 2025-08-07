import argparse
import os
from src.fetch_data import main as fetch_data_main
from src.process_data import main as process_data_main
from app import app

"""
run_pipeline.py

Usage:
  python run_pipeline.py --fetch        # Fetch latest data
  python run_pipeline.py --process      # Process fetched data
  python run_pipeline.py --serve        # Run Dash app server (development)
  python run_pipeline.py --fetch --process --serve  # Run all steps sequentially
"""

def run_fetch():
    print("Fetching latest data...")
    fetch_data_main()


def run_process():
    print("Processing data...")
    process_data_main()


def run_dash():
    print("Starting Dash app...")
    port = int(os.environ.get("PORT", 8050))
    app.run_server(debug=False, host='0.0.0.0', port=port)

def main():
    parser = argparse.ArgumentParser(description="BTC Tracker pipeline commands")
    parser.add_argument('--fetch', action='store_true', help='Fetch latest data')
    parser.add_argument('--process', action='store_true', help='Process data for stats and smoothing')
    parser.add_argument('--serve', action='store_true', help='Run Dash app to serve plots')


    args = parser.parse_args()


    # Execute requested commands
    if args.fetch:
        run_fetch()
    if args.process:
        run_process()
    if args.serve:
        run_dash()


    # Print if no arguments provided
    if not (args.fetch or args.process or args.serve):
        parser.print_help()


if __name__ == "__main__":
    main()
