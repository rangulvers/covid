import numpy as np  # linear algebra
import pandas as pd  # data processing, CSV file I/O (e.g. pd.read_csv)
import plotly.express as px
import plotly.graph_objects as go
import dash
import dash_core_components as dcc
import dash_html_components as html


# URLS
url_con = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv"
urL_death = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv"
url_recover = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv"

# Create Datasets
df_confirmed = pd.read_csv(url_con, error_bad_lines=False)
df_death = pd.read_csv(urL_death, error_bad_lines=False)
df_recovered = pd.read_csv(url_recover, error_bad_lines=False)

# Flatten Datasets to fit charts
df_confirmed_flat = df_confirmed.melt(var_name="Date", value_name="count", id_vars=[
                                      "Province/State", "Country/Region", "Lat", "Long"])
df_death_flat = df_death.melt(var_name="Date", value_name="count", id_vars=[
                              "Province/State", "Country/Region", "Lat", "Long"])
df_recoverd_flat = df_recovered.melt(var_name="Date", value_name="count", id_vars=[
                                     "Province/State", "Country/Region", "Lat", "Long"])

# Fix -1 and 0 values
df_confirmed_flat = df_confirmed_flat[(
    df_confirmed_flat[['count']] > 0).all(axis=1)]
df_death_flat = df_death_flat[(df_death_flat[['count']] > 0).all(axis=1)]
df_recoverd_flat = df_recoverd_flat[(
    df_recoverd_flat[['count']] > 0).all(axis=1)]

# Change Dateformat of Date Column
df_confirmed_flat["Date"] = pd.to_datetime(df_confirmed_flat["Date"])
df_death_flat["Date"] = pd.to_datetime(df_death_flat["Date"])
df_recoverd_flat["Date"] = pd.to_datetime(df_recoverd_flat["Date"])
df_death_flat = df_death_flat.drop(columns=["Province/State", "Lat", "Long"])

# Confirmed Cases prep step
byDateCountry = df_confirmed_flat.groupby(
    ["Date", "Country/Region"], as_index=False).sum()
byDateCountry = byDateCountry.drop(columns=["Lat", "Long"])
byDateWorldWide = byDateCountry.groupby("Date", as_index=False).sum()
byDateWorldWide["pct_change"] = byDateWorldWide['count'].pct_change()
byDateWorldWide["diff"] = byDateWorldWide['count'].diff()
df_death_flat = df_death_flat.groupby(
    ["Date", "Country/Region"], as_index=False).sum()


current_confirmend = byDateWorldWide.tail(1)

# Setup Charts
fig_byDateWorldWide = px.scatter()
fig_byDateWorldWide.add_scatter(x=byDateWorldWide["Date"],
                                y=byDateWorldWide["count"],
                                name="Confirmed Cases World Wide")

fig_byDateWorldWide.add_bar(x=byDateWorldWide["Date"],
                            y=byDateWorldWide["diff"],
                            name="Diff by Date")


fig_byDateWorldWidePct = px.line(x=byDateWorldWide["Date"],
                                 y=byDateWorldWide["pct_change"],
                                 title="PCT Change")

fig_byDateCountry = px.line(x=byDateCountry["Date"],
                            y=byDateCountry["count"],
                            color=byDateCountry["Country/Region"],
                            title="Confirmed Cases by Date")

fig_death = px.line(x=df_death_flat["Date"],
                    y=df_death_flat["count"],
                    color=df_death_flat["Country/Region"],
                    title="Death")

fig_confirmed_heatmap = go.Figure(data=go.Heatmap(
    z=byDateCountry["count"],
    x=byDateCountry["Country/Region"],
    y=byDateCountry["Date"],
    colorscale='Viridis'))

external_stylesheets = [
    'https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.layout = html.Div(className='container-fluid', children=[

    html.Div(className='jumbotron', children=[
        dcc.Markdown(f'''
        # COVID-19 Dashboard
        All information is pulled from the Johns Hopkins University Github Page [links](https://www.github.com/CSSEGISandData) ({current_confirmend["Date"].values[0]})'''),
        dcc.Markdown(
            f''' ## Total Cases  {current_confirmend["count"].values[0]}  | Diff to day before : {current_confirmend["diff"].values[0]}  | PCT_Change : {current_confirmend["pct_change"].values[0]}''')
    ]),
    html.Div(className='row', children=[
        html.Div(className='col-sm-6', children=[
            dcc.Graph(
                id='fig_byDateWorldWide',
                figure=fig_byDateWorldWide
            ),
        ]),
        html.Div(className='col-sm-6', children=[
            dcc.Graph(
                id='fig_confirmed_heatmap',
                figure=fig_confirmed_heatmap
            ),
        ])
    ]),
    html.Div(className='row', children=[
        html.Div(className='col-sm-6', children=[
            dcc.Graph(
                       id='fig_byDateWorldWidePct',
                       figure=fig_byDateWorldWidePct
            )
        ]),
        html.Div(className='col-sm-6', children=[
            dcc.Graph(
                id='fig_byDateCountry',
                figure=fig_byDateCountry
            ),
        ]),
    ])
])

if __name__ == '__main__':
    app.run_server(debug=False)
