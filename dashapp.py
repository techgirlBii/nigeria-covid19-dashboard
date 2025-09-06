import dash
from dash import dcc, html, Input, Output
import pandas as pd
import plotly.express as px

# Load dataset
df = pd.read_csv("COVID19_cases_Nigeria.csv")  
df['Date'] = pd.to_datetime(df['Date'])

# Initialize app
app = dash.Dash(__name__)

# Layout
app.layout = html.Div([
    html.H1("COVID-19 Dashboard: Nigeria (NCDC Data)", style={"textAlign": "center"}),

    # Date range filter
    dcc.DatePickerRange(
        id='date-range',
        start_date=df['Date'].min(),
        end_date=df['Date'].max(),
        display_format='YYYY-MM-DD'
    ),

    # Charts
    html.Div([
        dcc.Graph(id="daily-trend"),
        dcc.Graph(id="state-bar")
    ], style={"display": "flex", "flexWrap": "wrap"}),

    html.Div([
        dcc.Graph(id="cumulative-pie")
    ])
])

# Callback
@app.callback(
    [Output("daily-trend", "figure"),
     Output("state-bar", "figure"),
     Output("cumulative-pie", "figure")],
    [Input("date-range", "start_date"),
     Input("date-range", "end_date")]
)
def update_charts(start_date, end_date):
    # Filter by date range
    filtered = df[(df["Date"] >= start_date) & (df["Date"] <= end_date)]

    # Daily trend line chart
    trend = filtered.groupby("Date")[["Daily Confirmed Cases",
                                      "Daily Recovered Cases",
                                      "Daily Death Cases"]].sum().reset_index()
    fig_trend = px.line(trend, x="Date",
                        y=["Daily Confirmed Cases", "Daily Recovered Cases", "Daily Death Cases"],
                        title="Daily COVID-19 Cases in Nigeria")

    # Bar chart by state (cumulative confirmed cases)
    state_totals = filtered.groupby("State")[["Cumulative Confirmed cases"]].max().reset_index()
    fig_state = px.bar(state_totals, x="State", y="Cumulative Confirmed cases",
                       title="Cumulative Confirmed Cases by State", color="Cumulative Confirmed cases")

    # Pie chart of cumulative totals
    totals = {
        "Confirmed": filtered["Cumulative Confirmed cases"].max(),
        "Recovered": filtered["Cumulative recovered Cases"].max(),
        "Deaths": filtered["Cumulative Death Cases"].max()
    }
    fig_pie = px.pie(values=totals.values(), names=totals.keys(),
                     title="Cumulative COVID-19 Distribution (Nigeria)")

    return fig_trend, fig_state, fig_pie


if __name__ == "__main__":
    app.run(debug=True)
