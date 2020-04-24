import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc


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

df_death_flat = df_death_flat.drop(columns=["Lat", "Long"])
df_recoverd_flat = df_recoverd_flat.drop(
    columns=["Lat", "Long"])

df_death_flat = df_death_flat.rename(columns={"count": "death_count"})
df_recoverd_flat = df_recoverd_flat.rename(
    columns={"count": "recoverd_count"})

df_confirmed_flat = pd.merge(df_confirmed_flat, df_recoverd_flat, how="outer", on=[
                             "Province/State", "Country/Region", "Date"])
df_confirmed_flat = pd.merge(df_confirmed_flat, df_death_flat, how="outer", on=[
                             "Province/State", "Country/Region", "Date"])


# Confirmed Cases prep step
df_byDateCountry = df_confirmed_flat.groupby(
    ["Date", "Country/Region"], as_index=False).sum()

df_byDateCountry = df_byDateCountry.sort_values("count")
byDateWorldWide = df_byDateCountry.groupby("Date", as_index=False).sum()
byDateWorldWide = byDateWorldWide.drop(columns=["Lat", "Long"])
byDateWorldWide["pct_change"] = byDateWorldWide['count'].pct_change()
byDateWorldWide["diff"] = byDateWorldWide['count'].diff()
byDateWorldWide["death_pct_change"] = byDateWorldWide['death_count'].pct_change()
byDateWorldWide["deaeth_diff"] = byDateWorldWide['death_count'].diff()
byDateWorldWide["recoverd_pct_change"] = byDateWorldWide['recoverd_count'].pct_change()
byDateWorldWide["recoverd_diff"] = byDateWorldWide['recoverd_count'].diff()
byDateWorldWide["time2double"] = np.log(
    2) / np.log(1+byDateWorldWide["pct_change"])
byDateWorldWide["death_time2double"] = np.log(
    2) / np.log(1+byDateWorldWide["death_pct_change"])
byDateWorldWide["recoverd_time2double"] = np.log(
    2) / np.log(1+byDateWorldWide["recoverd_pct_change"])
current_confirmend = byDateWorldWide.tail(2)

# Create DataSet for Combined World Chart Map
# take the first columns for country, province, lat and lon
# dfc = df_confirmed.iloc[:, :4]
# df_global_1 = df_confirmed.iloc[:, -1]  # take last column for latest data
# dfCombined = pd.concat([df_global, df_global_1], axis=1, sort=False)
# dfCombined.set_axis([*dfCombined.columns[:-1], 'count'], axis=1, inplace=True)
df_confirmed_wordmap = df_confirmed.iloc[:, [0, 1, 2, 3, -1]]
df_confirmed_wordmap.set_axis(
    [*df_confirmed_wordmap.columns[:-1], 'count'], axis=1, inplace=True)

df_death_worldmap = df_death.iloc[:, [0, 1, 2, 3, -1]]
df_death_worldmap.set_axis(
    [*df_death_worldmap.columns[:-1], 'count'], axis=1, inplace=True)

df_recoverd_worldmap = df_recovered.iloc[:, [0, 1, 2, 3, -1]]
df_recoverd_worldmap.set_axis(
    [*df_recoverd_worldmap.columns[:-1], 'count'], axis=1, inplace=True)

# Create Dateset to compare Total Cases vs Diff for the top 5 Coutries
df_dateCountryDiffTotal = df_confirmed_flat.groupby(
    ["Country/Region", "Date"]).sum()
df_dateCountryDiffTotal["diff"] = df_dateCountryDiffTotal['count'].diff()
df_dateCountryDiffTotal["pct_change"] = df_dateCountryDiffTotal['count'].pct_change()
df_dateCountryDiffTotal["time2double"] = np.log(
    2) / np.log(1+df_dateCountryDiffTotal["pct_change"])
df_dateCountryDiffTotal["time2double"] = df_dateCountryDiffTotal["time2double"].replace(
    [np.inf, -np.inf], np.nan)

df_dateCountryDiffTotal = df_dateCountryDiffTotal.reset_index()
filter_list = df_confirmed_wordmap.sort_values("count", ascending=False).head(10)[
    "Country/Region"]
filter_list = filter_list.to_list()
if "China" not in filter_list:
    filter_list.append("China")
df_dateCountryDiffTotal = df_dateCountryDiffTotal[df_dateCountryDiffTotal["Country/Region"].isin(
    filter_list)]
df_byDateCountryTop5 = df_byDateCountry[df_byDateCountry["Country/Region"].isin(
    filter_list)]


# Setup Charts
fig_byDateWorldWide = px.scatter(title="Global Overview")

fig_byDateWorldWide.add_scatter(x=byDateWorldWide["Date"],
                                y=byDateWorldWide["death_count"],
                                name="Confirmed death World Wide")
fig_byDateWorldWide.add_scatter(x=byDateWorldWide["Date"],
                                y=byDateWorldWide["recoverd_count"],
                                name="Confirmed Recovered World Wide")
fig_byDateWorldWide.add_scatter(x=byDateWorldWide["Date"],
                                y=byDateWorldWide["count"],
                                name="Confirmed Cases World Wide")

fig_byDateWorldWide.add_bar(x=byDateWorldWide["Date"],
                            y=byDateWorldWide["time2double"],
                            name="Time 2 Double")
fig_byDateWorldWide.add_bar(x=byDateWorldWide["Date"],
                            y=byDateWorldWide["death_time2double"],
                            name="Death Time 2 Double")
fig_byDateWorldWide.add_bar(x=byDateWorldWide["Date"],
                            y=byDateWorldWide["recoverd_time2double"],
                            name="recoverd Time 2 Double")


fig_byDateWorldWidePct = px.line(x=byDateWorldWide["Date"],
                                 y=byDateWorldWide["pct_change"],
                                 title="% Change by Date")

fig_WorldWideChange = px.scatter(byDateWorldWide, x="count",
                                 y="diff", marginal_x="rug", marginal_y="histogram", title="Change cases by date")

fig_byDateWorldWide.update_layout(yaxis_type="log")
fig_byDateWorldWidePct.update_layout(yaxis_type="log")


fig_df_byDateCountry = px.line(x=df_byDateCountryTop5["Date"],
                               y=df_byDateCountryTop5["count"],
                               color=df_byDateCountryTop5["Country/Region"],
                               title="Confirmed Cases by Date and Country")

fig_changesDiffTotal = px.scatter(df_dateCountryDiffTotal, x="count",
                                  y="diff", color="Country/Region", hover_name="Date", marginal_x="rug", marginal_y="histogram",  title="Total Cases and Diff by Date")
fig_changesDiffTotal.update_layout(xaxis_type="log", yaxis_type="log")


fig_worldmap = px.scatter_mapbox(df_confirmed_wordmap, lat="Lat", lon="Long", hover_name="Country/Region", hover_data=["count"],
                                 zoom=0, height=300, size="count", color="count", color_continuous_scale=px.colors.sequential.Agsunset)
# fig_worldmap.add_scattermapbox(df_death_worldmap, lat="Lat", lon="Long", hover_name="Country/Region", hover_data=["count"],
#                                color_discrete_sequence=["fuchsia"], zoom=0, height=300)
# fig_worldmap.add_scattermapbox(df_recoverd_worldmap, lat="Lat", lon="Long", hover_name="Country/Region", hover_data=["count"],
#                                color_discrete_sequence=["fuchsia"], zoom=0, height=300)

fig_worldmap.update_layout(mapbox_style="open-street-map")
fig_worldmap.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})

fig_confirmed_heatmap = go.Figure(data=go.Heatmap(
    z=df_byDateCountry["count"],
    x=df_byDateCountry["Country/Region"],
    y=df_byDateCountry["Date"],
    colorscale='Viridis'))

# Configure Dash layout
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server
app.layout = html.Div(className='container-fluid', children=[

    html.Div(className='jumbotron', children=[
        dcc.Markdown(f'''
        # COVID-19 Dashboard
        All information is pulled from the Johns Hopkins University [Github Page](https://www.github.com/CSSEGISandData) ({current_confirmend["Date"].values[0]})'''),
        dbc.Progress(
            [
                dbc.Progress(current_confirmend["count"].tail(
                    1).values[0], value=100, color="warning", bar=True),
                dbc.Progress(current_confirmend["recoverd_count"].tail(
                    1).values[0], value=(current_confirmend["recoverd_count"].tail(
                        1).values[0] / current_confirmend["count"].tail(
                        1).values[0])*100, color="success", bar=True),
                dbc.Progress(current_confirmend["death_count"].tail(
                    1).values[0], value=(current_confirmend["death_count"].tail(
                        1).values[0] / current_confirmend["count"].tail(
                        1).values[0])*100, color="dark", bar=True),
            ],
            multi=True,
        )
    ]),

    dbc.Row(
        [

            dbc.Col([
                dcc.Graph(
                    id='fig_worldmap',
                    figure=fig_worldmap
                )
            ]),

            dbc.Col(dbc.Card([
                dbc.CardHeader("Confirmed"),
                dbc.CardBody(
                    [
                        html.H5(current_confirmend["count"].tail(
                            1).values[0], className="card-title"),
                        html.P(
                            f"This is a change of {current_confirmend['diff'].tail(1).values[0]} or {current_confirmend['pct_change'].tail(1).values[0]} (PCT_CHANGE) to yesterday")
                    ]
                )], color="warning", inverse=True
            )),
            dbc.Col(dbc.Card([
                dbc.CardHeader("Recoverd"),
                dbc.CardBody(
                    [
                        html.H5(current_confirmend["recoverd_count"].tail(
                            1).values[0], className="card-title")
                    ]
                )], color="success", inverse=True
            )),        dbc.Col(dbc.Card([
                dbc.CardHeader("Death"),
                dbc.CardBody(
                    [
                        html.H5(current_confirmend["death_count"].tail(
                                1).values[0], className="card-title")
                    ]
                )], color="dark", inverse=True
            ))
        ]
    ),
    dbc.Row(
        dbc.Col([
        ])
    ),

    dbc.Row(
        dbc.Col([
            dcc.Graph(
                id='fig_byDateWorldWide',
                figure=fig_byDateWorldWide
            ),
        ])
    ),

    dbc.Row(
        dbc.Col([
            dcc.Graph(
                id='fig_WorldWideChange',
                figure=fig_WorldWideChange
            )
        ])
    ),
    dbc.Row(
        dbc.Col([
            dcc.Graph(
                id='fig_changesDiffTotal',
                figure=fig_changesDiffTotal
            )
        ])
    ),

    dbc.Row(
        dbc.Col([
            dcc.Graph(
                id='fig_confirmed_heatmap',
                figure=fig_confirmed_heatmap
            ),
        ])
    ),
    dbc.Row(
        dbc.Col([
            dcc.Graph(
                id='fig_byDateWorldWidePct',
                figure=fig_byDateWorldWidePct
            )
        ])
    ),
    dbc.Row(
        dbc.Col([
            dcc.Graph(
                id='fig_df_byDateCountry',
                figure=fig_df_byDateCountry
            ),
        ])
    ),
])

if __name__ == '__main__':
    app.run_server(debug=False)
