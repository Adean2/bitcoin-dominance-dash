import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output, callback_context, no_update
import dash
import os
from datetime import datetime
import random

app = Dash(__name__)
server = app.server

# Import fetch and process pipeline functions
from src.fetch_data import main as fetch_data_main
from src.process_data import main as process_data_main



# Generate random dark colors
def random_dark_color():
    def rand_channel():
        return random.randint(20, 200)  # medium brightness range
    return f'rgb({rand_channel()}, {rand_channel()}, {rand_channel()})'

# Load CSV
script_dir = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(script_dir, 'data', 'processed', 'bitcoin_dominance_processed.csv')
df = pd.read_csv(data_path)
df['date'] = pd.to_datetime(df['date'])
df.rename(columns={'bitcoin_dominance': 'Dominance'}, inplace=True)

# Add 'year' column for categorical coloring
df['year'] = df['date'].dt.year.astype(str)

# Generate a fixed random color mapping for each unique year
unique_years = df['year'].unique()
color_map = {year: random_dark_color() for year in unique_years}

COLOR_SCALES = [
    'Viridis', 'Cividis', 'Plasma', 'Magma', 'Inferno',
    'Turbo', 'Blues', 'Greens', 'Reds', 'Purples', 'Jet'
]

# unique sorted dates for slider indexing
unique_dates = df['date'].sort_values().dt.date.unique()
date_to_index = {date: i for i, date in enumerate(unique_dates)}
index_to_date = {i: date for i, date in enumerate(unique_dates)}

slider_marks = {}
step_for_marks = max(1, len(unique_dates)//10)
for i, date in index_to_date.items():
    if i % step_for_marks == 0 or i == len(unique_dates) - 1:
        slider_marks[i] = date.strftime('%Y-%m-%d')

app.layout = html.Div(className="container", children=[

  
    html.Div(className="header", children=[
        html.Img(src="/assets/logo.png", className="logo"),
        html.H1("Bitcoin Dominance", className="title")
    ]),

 
    html.Div(className="main-content", children=[

        html.Div(className="left-column", children=[
            dcc.Graph(
                id='btc-dominance-graph',
                style={'height': '600px', 'width': '100%'}
            ),

            html.Label("Range Slider", style={"marginTop": "10px", "fontSize": "16px"}),
            dcc.RangeSlider(
                id='date-slider',
                min=0,
                max=len(unique_dates) - 1,
                value=[0, len(unique_dates) - 1],
                marks={},  # no marks (hidden)
                allowCross=False,
                tooltip={"placement": "bottom", "always_visible": True}
            ),

            html.Label("Rolling Average", style={"marginTop": "10px", "fontSize": "16px"}),
            html.Div(
                dcc.Slider(
                    id='rolling-window',
                    min=1,
                    max=30,
                    step=1,
                    value=1,
                    marks={1: '1', 7: '7', 14: '14', 30: '30'},
                    tooltip={"placement": "bottom", "always_visible": False},
                    updatemode='drag'
                ),
                style={"width": "100%"} 
            ),
        ]),

        
        html.Div(className="right-column", children=[

            html.Label("Select Date Range:"),
            dcc.DatePickerRange(
                id='date-range',
                className="inputs",
                min_date_allowed=unique_dates[0],
                max_date_allowed=unique_dates[-1],
                start_date=unique_dates[0],
                end_date=unique_dates[-1],
            ),

            html.Label("Graph Type:"),
            dcc.Dropdown(
                id='graph-type',
                options=[
                    {'label': 'Line', 'value': 'line'},
                    {'label': 'Scatter (Gradient)', 'value': 'scatter'},
                    {'label': 'Bar (Categorical Colors)', 'value': 'bar'}
                ],
                value='line',
                className="inputs",
                clearable=False,
                style={'width': '100%'}
            ),

            html.Label("Color Gradient:"),
            dcc.Dropdown(
                id='color-scale',
                className="inputs",
                options=[{'label': scale, 'value': scale} for scale in COLOR_SCALES],
                value='Viridis',
                clearable=False,
                style={'width': '100%'}
            ),

            html.Label("Data Granularity:"),
            dcc.Dropdown(
                id='granularity',
                options=[
                    {'label': 'Daily', 'value': 'day'},
                    {'label': 'Weekly', 'value': 'week'},
                    {'label': 'Monthly', 'value': 'month'},
                    {'label': 'Yearly', 'value': 'year'},
                ],
                value='day',
                className="inputs",
                clearable=False,
                style={'width': '100%'}
            ),

            # Reset Filters button
            html.Button("Reset Filters", id="reset-filters-btn", n_clicks=0, className="buts", style={"marginTop": "15px"}),

            # Fetch Data and Export CSV buttons
            html.Button("Fetch Data", id="fetch-data-btn", n_clicks=0, className="buts", style={"marginTop": "15px"}),
            html.Button("Export CSV", id="export-csv-btn", n_clicks=0, className="buts", style={"marginTop": "10px"}),
            dcc.Download(id="download-csv"),
        ]),
    ]),

    # Project Description
    html.Div(className="project-description", children=[
        html.H2("Project Description", style={"color": "#faad14", "marginBottom": "15px"}),
        html.P(
            "The Bitcoin Dominance Visualization Tool is a Python project designed to help users "
            "track and analyze Bitcoin’s share of the overall cryptocurrency market over time. "
            "The tool fetches live or historical data from a public API (such as CoinGecko), calculates "
            "Bitcoin’s percentage of total market capitalization (known as \"Bitcoin dominance\"), and "
            "visualizes these trends in clear, customizable charts.",
            style={"color": "#ddd", "lineHeight": "1.5", "marginBottom": "15px"}
        ),
        html.H3("Key Features:", style={"color": "#faad14", "marginBottom": "10px"}),
        html.Ul([
            html.Li("Data Retrieval: Automatically downloads up-to-date market capitalization data for Bitcoin and the entire cryptocurrency market.", style={"color": "#eee", "marginBottom": "5px"}),
            html.Li("Data Processing: Calculates Bitcoin’s dominance as a percentage for each day or chosen time interval.", style={"color": "#eee", "marginBottom": "5px"}),
            html.Li("Visualization: Plots Bitcoin dominance across your selected date range using static or interactive charts.", style={"color": "#eee", "marginBottom": "5px"}),
            html.Li("User Control: Allows users to specify date ranges, data granularity (daily, weekly, monthly), chart type, and options to display or export results.", style={"color": "#eee", "marginBottom": "5px"}),
            html.Li("Reproducibility: Clean, modular project structure for easy expansion, reuse, or integration into personal or academic projects.", style={"color": "#eee", "marginBottom": "5px"}),
        ], style={"paddingLeft": "20px", "marginBottom": "15px"}),
        html.H3("Goal:", style={"color": "#faad14", "marginBottom": "10px"}),
        html.P(
            "Provide an easy-to-use, open-source tool that visualizes how Bitcoin’s market position evolves—helping students, enthusiasts, and researchers "
            "better understand the dynamics between Bitcoin and the wider crypto market.",
            style={"color": "#ddd", "lineHeight": "1.5"}),
        html.H3("*Importance*:", style={"color": "#faad14", "marginBottom": "10px"}),
        html.P(
            "Bitcoin dominance reflects Bitcoin’s share of the total cryptocurrency market, serving as a vital indicator of market sentiment and investor confidence.",
            style={"color": "#ddd", "lineHeight": "1.5"}),
        html.Ul([
            html.Li("Measures Bitcoin’s market capitalization relative to the entire crypto market.", style={"color": "#eee", "marginBottom": "5px"}),
            html.Li("High dominance indicates strong confidence in Bitcoin as a stable asset.", style={"color": "#eee", "marginBottom": "5px"}),
            html.Li("Low dominance signals growing interest in altcoins and market diversification.", style={"color": "#eee", "marginBottom": "5px"}),
            html.Li("Helps traders and investors tailor strategies by signaling shifts between Bitcoin and altcoin investments.", style={"color": "#eee", "marginBottom": "5px"}),
            html.Li("Provides insights into overall market trends and the evolving maturity of the crypto ecosystem.", style={"color": "#eee", "marginBottom": "5px"}),
        ], style={"paddingLeft": "20px", "marginBottom": "15px"}),
        html.H3("Developer:", style={"color": "#faad14", "marginBottom": "10px"}),
        html.P(
            "Hi, I'm Aidan Engler, President of the Blockchain Club at NC State. I've been involved in the crypto space for over six years, and I’m passionate about continuously learning and adapting to the rapidly evolving blockchain technology landscape. A big thanks to Benjamin Cowen from IntoTheCryptoverse for his clear explanations and for being the true authority on Bitcoin dominance.",
            style={"color": "#ddd", "lineHeight": "1.5"}),
        html.P([
            "IntoTheCryptoverse (",
             html.A("YouTube Channel", href="https://www.youtube.com/watch?v=jHFc0dQakGs", target="_blank", style={"color": "#faad14", "textDecoration": "underline"}),") for his clear explanations and for being the true authority on Bitcoin dominance."],
            style={"color": "#ddd", "lineHeight": "1.5"}),
        html.P([
             "Learn blockchain @ ",
            html.A("NC State Blockchain Club", href="https://sites.google.com/ncsu.edu/blockchainatncstate/home/", target="_blank", style={"color": "#faad14", "textDecoration": "underline"})," for more info."],
            style={"color": "#ddd", "lineHeight": "1.5"}),
        html.P([
             "Check out my ",
            html.A("github", href="https://github.com/Adean2", target="_blank", style={"color": "#faad14", "textDecoration": "underline"})," for new projects!"],
            style={"color": "#ddd", "lineHeight": "1.5"}),
        html.P([
             "Follow me on ",
            html.A("linkedin", href="https://www.linkedin.com/in/aidanengler/", target="_blank", style={"color": "#faad14", "textDecoration": "underline"})," lets connect :)"],
            style={"color": "#ddd", "lineHeight": "1.5"}),
    ], style={
        "marginTop": "40px",
        "padding": "20px",
        "backgroundColor": "#23272a",
        "borderRadius": "10px",
        "boxShadow": "0 0 10px rgba(250, 173, 20, 0.5)"
    }),
])


def aggregate_data(df, granularity):
    numeric_cols = df.select_dtypes(include='number').columns
    df_numeric = df[['date'] + list(numeric_cols)].set_index('date')

    if granularity == 'day':
        resampled = df_numeric.resample('D').mean().dropna().reset_index()
    elif granularity == 'week':
        resampled = df_numeric.resample('W-MON').mean().dropna().reset_index()
    elif granularity == 'month':
        resampled = df_numeric.resample('MS').mean().dropna().reset_index()
    elif granularity == 'year':
        resampled = df_numeric.resample('YS').mean().dropna().reset_index()
    else:
        resampled = df_numeric.reset_index()

    return resampled


@app.callback(
    Output('btc-dominance-graph', 'figure'),
    Input('date-range', 'start_date'),
    Input('date-range', 'end_date'),
    Input('date-slider', 'value'),
    Input('graph-type', 'value'),
    Input('color-scale', 'value'),
    Input('granularity', 'value'),
    Input('rolling-window', 'value'),
)
def update_graph(start_date, end_date, slider_range, graph_type, color_scale, granularity, rolling_window):
    ctx = callback_context
    triggered_id = ctx.triggered[0]['prop_id'].split('.')[0] if ctx.triggered else None

   
    if triggered_id == 'date-slider' and slider_range:
        start_date = index_to_date[slider_range[0]]
        end_date = index_to_date[slider_range[1]]
    else:
        if isinstance(start_date, str):
            start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
        if isinstance(end_date, str):
            end_date = datetime.strptime(end_date, "%Y-%m-%d").date()

    mask = (df['date'].dt.date >= start_date) & (df['date'].dt.date <= end_date)
    filtered = df.loc[mask].copy()

    if filtered.empty:
        return px.scatter(title="No data available for the selected date range.")

    agg_df = aggregate_data(filtered, granularity)

    if rolling_window > 1:
        agg_df['Dominance_Roll'] = agg_df['Dominance'].rolling(window=rolling_window, min_periods=1).mean()
    else:
        agg_df['Dominance_Roll'] = None

    agg_df['year'] = agg_df['date'].dt.year.astype(str)

    if graph_type == 'line':
        fig = px.line(agg_df, x='date', y='Dominance', title='Dominance Over Time')
        fig.update_traces(line_color='orange')

        if rolling_window > 1:
            fig.add_scatter(
                x=agg_df['date'], y=agg_df['Dominance_Roll'],
                mode='lines',
                name=f'{rolling_window}-Day Rolling Avg',
                line=dict(color='red', dash='dash')
            )

    elif graph_type == 'scatter':
        fig = px.scatter(
            agg_df, x='date', y='Dominance',
            color='Dominance',
            color_continuous_scale=color_scale,
            title='Dominance (Gradient)'
        )
    elif graph_type == 'bar':
        fig = px.bar(
            agg_df, x='date', y='Dominance',
            color='year',
            color_discrete_map=color_map,
            title='Dominance by Year with Improved Colors',
            template='plotly_dark'
        )

        fig.update_traces(
            marker_line_color='rgba(255,255,255,0.3)',
            marker_line_width=1,
            marker_opacity=1
        )

        fig.update_layout(
            barmode='group'
        )
    else:
        fig = px.line(agg_df, x='date', y='Dominance', title='Dominance Over Time')

    fig.update_layout(
        xaxis_title='Date',
        yaxis_title='Dominance (%)',
        plot_bgcolor='#2c2f33',
        paper_bgcolor='#23272a',
        font=dict(color='white')
    )
    return fig

@app.callback(
    [
        Output('date-range', 'start_date'),
        Output('date-range', 'end_date'),
        Output('date-slider', 'value'),
        Output('graph-type', 'value'),
        Output('color-scale', 'value'),
        Output('granularity', 'value'),
        Output('rolling-window', 'value'),
    ],
    [
        Input('date-slider', 'value'),
        Input('reset-filters-btn', 'n_clicks'),
    ],
    prevent_initial_call=True
)
def update_filters(slider_range, reset_n_clicks):
    ctx = callback_context
    if not ctx.triggered:
        raise dash.exceptions.PreventUpdate

    triggered_id = ctx.triggered[0]['prop_id'].split('.')[0]

    initial_start_date = unique_dates[0]
    initial_end_date = unique_dates[-1]
    slider_default = [0, len(unique_dates) - 1]
    graph_type_default = 'line'
    color_scale_default = 'Viridis'
    granularity_default = 'day'
    rolling_window_default = 1

    if triggered_id == 'reset-filters-btn':
        # Reset all controls to defaults
        return (
            initial_start_date,
            initial_end_date,
            slider_default,
            graph_type_default,
            color_scale_default,
            granularity_default,
            rolling_window_default,
        )
    elif triggered_id == 'date-slider':
        
        if slider_range is None or len(slider_range) != 2:
            raise dash.exceptions.PreventUpdate

        start_date = index_to_date[slider_range[0]]
        end_date = index_to_date[slider_range[1]]

        return (
            start_date,
            end_date,
            no_update,  
            no_update,  
            no_update,  
            no_update,  
            no_update,  
        )
    else:
        raise dash.exceptions.PreventUpdate


# Fetch Data button callback: runs fetch and process pipeline, reloads data, updates button text
@app.callback(
    Output("fetch-data-btn", "children"),
    Input("fetch-data-btn", "n_clicks"),
    prevent_initial_call=True
)
def on_fetch_data_click(n_clicks):
    if not n_clicks:
        raise dash.exceptions.PreventUpdate

    # Run fetch and process
    fetch_data_main()
    process_data_main()

    # Reload the global dataframe
    global df
    df_path = os.path.join(script_dir, 'data', 'processed', 'bitcoin_dominance_processed.csv')
    df = pd.read_csv(df_path)
    df['date'] = pd.to_datetime(df['date'])
    df.rename(columns={'bitcoin_dominance': 'Dominance'}, inplace=True)
    df['year'] = df['date'].dt.year.astype(str)

    return "Data Fetched!"


# Export CSV button callback
@app.callback(
    Output("download-csv", "data"),
    Input("export-csv-btn", "n_clicks"),
    [Input('date-range', 'start_date'),
     Input('date-range', 'end_date'),
     Input('granularity', 'value')],
    prevent_initial_call=True,
)
def export_filtered_data(n_clicks, start_date, end_date, granularity):
    if not n_clicks:
        raise dash.exceptions.PreventUpdate

    start_date_dt = pd.to_datetime(start_date).date() if isinstance(start_date, str) else start_date
    end_date_dt = pd.to_datetime(end_date).date() if isinstance(end_date, str) else end_date

    mask = (df['date'].dt.date >= start_date_dt) & (df['date'].dt.date <= end_date_dt)
    filtered = df.loc[mask]

    agg_df = aggregate_data(filtered, granularity)

    return dcc.send_data_frame(agg_df.to_csv, "bitcoin_dominance.csv", index=False)


if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 8050))
    app.run(debug=False, host='0.0.0.0', port=port)

