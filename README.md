Bitcoin Dominance Visualization Tool - Welcome!!

A Python Dash app to visualize and analyze Bitcoin's dominance in the overall cryptocurrency market over time. This tool fetches and processes market capitalization data, allowing interactive exploration with customizable charts, date filtering, rolling averages, and export capabilities.

Features:

Interactive time series charts displaying Bitcoin dominance (% of total crypto market cap)

Multiple chart types: Line, Scatter with color gradient, Bar categorized by year

Adjustable date range with synchronized slider and date picker inputs

Rolling average smoothing for clearer trend visualization

Data aggregation granularity: daily, weekly, monthly, yearly

Dynamic color scales and year-based color coding

Fetch latest data on demand and export filtered data as CSV

Responsive design optimized for desktop and mobile

Reset filters button to restore default view and controls

Installation
Clone this repository:

git clone https://github.com/Adean2/bitcoin-dominance-dash.git
cd bitcoin-dominance-app

Create and activate a Python virtual environment (recommended):

python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

Install dependencies:
pip install -r requirements.txt


Ensure the data files are present under data/processed/ or run the fetch pipeline via:

python run_pipeline.py --fetch --process

Usage
Run the Dash app locally with:

python app.py
Open your browser at http://127.0.0.1:8050 to interact with the dashboard.



Project Structure
app.py - Main Dash app script

run_pipeline.py - Data fetching and processing pipeline

data/ - Raw and processed data CSV files

src/ - Source modules for data fetching and processing

assets/ - CSS and static assets for styling


License
This project is licensed under the MIT License.

Contact
Developed by Aidan Engler

GitHub: Adean2

LinkedIn: https://www.linkedin.com/in/aidanengler
