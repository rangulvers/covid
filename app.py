import numpy as np  # linear algebra
import pandas as pd  # data processing, CSV file I/O (e.g. pd.read_csv)
# import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px
import os
import wget
import dash
import dash_core_components as dcc
import dash_html_components as html


file_list = ['covid_confirmed.csv',
             "covid_death.csv",
             "covid_recovered.csv"]
for file in file_list:
    if os.path.exists(file):
        os.remove(file)

url_con = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv"
urL_death = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv"
url_recover = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv"

wget.download(url_con, 'covid_confirmed.csv', )
wget.download(urL_death, 'covid_death.csv', )
wget.download(url_recover, 'covid_recovered.csv', )


df_confirmed = pd.read_csv("covid_confirmed.csv", error_bad_lines=False)
df_death = pd.read_csv("covid_death.csv", error_bad_lines=False)
df_recovered = pd.read_csv("covid_recovered.csv", error_bad_lines=False)

df_confirmed_flat = df_confirmed.melt(var_name="Date", value_name="count", id_vars=[
    "Province/State", "Country/Region", "Lat", "Long"])


df_death_flat = df_death.melt(var_name="Date", value_name="count", id_vars=[
    "Province/State", "Country/Region", "Lat", "Long"])

df_recoverd_flat = df_recovered.melt(var_name="Date", value_name="count", id_vars=[
    "Province/State", "Country/Region", "Lat", "Long"])

df_confirmed_flat = df_confirmed_flat[(
    df_confirmed_flat[['count']] > 0).all(axis=1)]
df_death_flat = df_death_flat[(df_death_flat[['count']] > 0).all(axis=1)]
df_recoverd_flat = df_recoverd_flat[(
    df_recoverd_flat[['count']] > 0).all(axis=1)]


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


# Death Cases prep step
df_death_flat = df_death_flat.groupby(
    ["Date", "Country/Region"], as_index=False).sum()


fig_byDateWorldWide = px.scatter()
fig_byDateWorldWide.add_scatter(x=byDateWorldWide["Date"], y=byDateWorldWide["count"],
                                name="Confirmed Cases World Wide")
fig_byDateWorldWide.add_bar(x=byDateWorldWide["Date"],
                            y=byDateWorldWide["diff"],
                            name="Diff by Date")

fig_byDateWorldWidePct = px.line(x=byDateWorldWide["Date"],
                                 y=byDateWorldWide["pct_change"],
                                 title="PCT Change")

fig_byDateCountry = px.line(x=byDateCountry["Date"], y=byDateCountry["count"],
                            color=byDateCountry["Country/Region"],
                            title="Confirmed Cases by Date")

fig_death = px.line(x=df_death_flat["Date"], y=df_death_flat["count"],
                    color=df_death_flat["Country/Region"],
                    title="Death")

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.layout = html.Div(children=[

    dcc.Graph(
        id='con-graph-wordlwide',
        figure=fig_byDateWorldWide
    ),
    dcc.Graph(
        id='con-graph-wordlwide-pct',
        figure=fig_byDateWorldWidePct
    ),
    dcc.Graph(
        id='con-graph-by-date',
        figure=fig_byDateCountry
    ),
    dcc.Graph(
        id='con-map',
        figure=fig_death
    )

])


if __name__ == '__main__':
    app.run_server(debug=True)
