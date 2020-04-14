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
# df_death_flat["Date"] = pd.to_datetime(df_death_flat["Date"])
# df_recoverd_flat["Date"] = pd.to_datetime(df_recoverd_flat["Date"])
# df_death_flat = df_death_flat.drop(columns=["Province/State", "Lat", "Long"])

# Confirmed Cases prep step
df_byDateCountry = df_confirmed_flat.groupby(
    ["Date", "Country/Region"], as_index=False).sum()

df_byDateCountry = df_byDateCountry.sort_values("count")
byDateWorldWide = df_byDateCountry.groupby("Date", as_index=False).sum()
byDateWorldWide = byDateWorldWide.drop(columns=["Lat", "Long"])
byDateWorldWide["pct_change"] = byDateWorldWide['count'].pct_change()
byDateWorldWide["diff"] = byDateWorldWide['count'].diff()
current_confirmend = byDateWorldWide.tail(2)
# df_death_flat = df_death_flat.groupby(
#     ["Date", "Country/Region"], as_index=False).sum()


# Create DataSet for Combined World Chart Map
# take the first columns for country, province, lat and lon
df_global = df_confirmed.iloc[:, :4]
df_global_1 = df_confirmed.iloc[:, -1]  # take last column for latest data
dfCombined = pd.concat([df_global, df_global_1], axis=1, sort=False)
dfCombined.set_axis([*dfCombined.columns[:-1], 'count'], axis=1, inplace=True)


# Create Dateset to compare Total Cases vs Diff for the top 5 Coutries
df_dateCountryDiffTotal = df_confirmed_flat.groupby(
    ["Country/Region", "Date"]).sum()
df_dateCountryDiffTotal["diff"] = df_dateCountryDiffTotal['count'].diff()
df_dateCountryDiffTotal = df_dateCountryDiffTotal.reset_index()
filter_list = dfCombined.sort_values("count").tail(5)["Country/Region"]
filter_list = filter_list.to_list()
filter_list.append("China") 
df_dateCountryDiffTotal = df_dateCountryDiffTotal[df_dateCountryDiffTotal["Country/Region"].isin(
    filter_list)]
df_byDateCountryTop5 = df_byDateCountry[df_byDateCountry["Country/Region"].isin(
    filter_list)]


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

fig_byDateWorldWide.update_layout(yaxis_type="log")
fig_byDateWorldWidePct.update_layout(yaxis_type="log")

fig_df_byDateCountry = px.line(x=df_byDateCountryTop5["Date"],
                               y=df_byDateCountryTop5["count"],
                               color=df_byDateCountryTop5["Country/Region"],
                               title="Confirmed Cases by Date")

fig_changesDiffTotal = px.scatter(df_dateCountryDiffTotal, x="count",
                                  y="diff", color="Country/Region")
fig_changesDiffTotal.update_layout(xaxis_type="log", yaxis_type="log")

fig_worldmap = px.scatter_mapbox(dfCombined, lat="Lat", lon="Long", hover_name="Country/Region", hover_data=["count"],
                                 color_discrete_sequence=["fuchsia"], zoom=0, height=300)

fig_worldmap.update_layout(mapbox_style="open-street-map")
fig_worldmap.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})

fig_confirmed_heatmap = go.Figure(data=go.Heatmap(
    z=df_byDateCountry["count"],
    x=df_byDateCountry["Country/Region"],
    y=df_byDateCountry["Date"],
    colorscale='Viridis'))

# Configure Dash layout and load data
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
            f'''
            ### Total Cases :  {current_confirmend["count"].tail(1).values[0]} ({current_confirmend["count"].head(1).values[0]})
            ### Diff to day before : {current_confirmend["diff"].tail(1).values[0]} ({current_confirmend["diff"].head(1).values[0]}) 
            ### PCT_Change : {current_confirmend["pct_change"].tail(1).values[0]} ({current_confirmend["pct_change"].head(1).values[0]})''')
    ]),

    html.Div(className='row', children=[
        html.Div(className='col-xl-6', children=[
             dcc.Graph(
                 id='fig_byDateWorldWide',
                 figure=fig_byDateWorldWide
             ),
             ]),
        html.Div(className='col-xl-6', children=[
            dcc.Graph(
                id='fig_changesDiffTotal',
                figure=fig_changesDiffTotal
            ),
        ]),
    ]),
    html.Div(className='row', children=[
        html.Div(className='col-xl-4', children=[
            dcc.Graph(
                id='fig_worldmap',
                figure=fig_worldmap
            ),
        ]),
        html.Div(className='col-xl-8', children=[
            dcc.Graph(
                id='fig_confirmed_heatmap',
                figure=fig_confirmed_heatmap
            ),
        ])
    ]),
    html.Div(className='row', children=[
        html.Div(className='col-xl-6', children=[
            dcc.Graph(
                       id='fig_byDateWorldWidePct',
                       figure=fig_byDateWorldWidePct
            )
        ]),
        html.Div(className='col-xl-6', children=[
            dcc.Graph(
                id='fig_df_byDateCountry',
                figure=fig_df_byDateCountry
            ),
        ]),
    ])
])

if __name__ == '__main__':
    app.run_server(debug=True)
