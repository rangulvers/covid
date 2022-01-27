import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc


# URLS
url_confirmed = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv"


# Create Datasets
df_confirmed = pd.read_csv(url_confirmed, error_bad_lines=False)
df_confirmed.iloc[:, 4:] = df_confirmed.iloc[:, 4:].clip(lower=0)

# Flatten Datasets to fit charts
df_confirmed_flat = df_confirmed.melt(var_name="Date", value_name="count", id_vars=[
                                      "Province/State", "Country/Region", "Lat", "Long"])

# create filter based on countrys

filter = df_confirmed_flat["Country/Region"].unique()

# Fix -1 and 0 values
# df_confirmed_flat = df_confirmed_flat[(
#     df_confirmed_flat[['count']] > 0).all(axis=1)]
# df_death_flat = df_death_flat[(df_death_flat[['count']] > 0).all(axis=1)]
# df_recoverd_flat = df_recoverd_flat[(
#     df_recoverd_flat[['count']] > 0).all(axis=1)]

# Change Dateformat of Date Column
df_confirmed_flat["Date"] = pd.to_datetime(df_confirmed_flat["Date"])

# Confirmed Cases prep step
df_byDateCountry = df_confirmed_flat.groupby(
    ["Date", "Country/Region"], as_index=False).sum()

# df_byDateCountry = df_byDateCountry.sort_values("count")
byDateWorldWide = df_byDateCountry.groupby("Date", as_index=False).sum()
# byDateWorldWide = byDateWorldWide.drop(columns=["Lat", "Long"])
# byDateWorldWide["pct_change"] = byDateWorldWide['count'].pct_change()
byDateWorldWide["diff"] = byDateWorldWide['count'].diff()
# current_confirmend = byDateWorldWide.tail(2)


# # Create Dateset to compare Total Cases vs Diff for the top 5 Coutries
df_dateCountryDiffTotal = df_confirmed_flat.groupby(
    ["Country/Region", "Date"]).sum()
df_dateCountryDiffTotal["diff"] = df_dateCountryDiffTotal['count'].diff()
# df_dateCountryDiffTotal["pct_change"] = df_dateCountryDiffTotal['count'].pct_change()
# df_dateCountryDiffTotal["time2double"] = np.log(
#     2) / np.log(1+df_dateCountryDiffTotal["pct_change"])
# df_dateCountryDiffTotal["time2double"] = df_dateCountryDiffTotal["time2double"].replace(
#     [np.inf, -np.inf], np.nan)

# df_dateCountryDiffTotal = df_dateCountryDiffTotal.reset_index()
# df_filter_list = pd.DataFrame(
#     df_confirmed_flat.groupby("Country/Region")["count"].sum())
# filter_list = df_filter_list.sort_values("count", ascending=False).head(10)
# filter_list = list(filter_list.index)
# if "China" not in filter_list:
#     filter_list.append("China")
# df_dateCountryDiffTotal = df_dateCountryDiffTotal[df_dateCountryDiffTotal["Country/Region"].isin(
#     filter_list)]
# df_byDateCountryTop5 = df_byDateCountry[df_byDateCountry["Country/Region"].isin(
#     filter_list)]


# Setup Charts


# fig_byDateWorldWidePct = px.line(x=byDateWorldWide["Date"],
#                                  y=byDateWorldWide["pct_change"],
#                                  title="% Change by Date")

# fig_WorldWideChange = px.scatter(byDateWorldWide, x="count",
#                                  y="diff", marginal_x="rug", marginal_y="histogram", title="Change cases by date")

# fig_byDateWorldWide.update_layout(yaxis_type="log")
# fig_byDateWorldWidePct.update_layout(yaxis_type="log")

# '
# fig_df_byDateCountry = px.line(x=df_byDateCountryTop5["Date"],
#                                y=df_byDateCountryTop5["count"],
#                                color=df_byDateCountryTop5["Country/Region"],
#                                title="Confirmed Cases by Date and Country")'

# fig_changesDiffTotal = px.scatter(df_dateCountryDiffTotal, x="count",
#                                   y="diff", color="Country/Region", hover_name="Date", marginal_x="rug", marginal_y="histogram",  title="Total Cases and Diff by Date")


# fig_changesDiffTotal.update_layout(xaxis_type="log", yaxis_type="log")

# fig_activeCasesByDate = px.line(df_dateCountryDiffTotal, x="Date",
#                                 y="active", color="Country/Region", hover_name="Date",  title="Total Active Cases by Date")

fig_cases_by_country = px.line(
    df_confirmed_flat, x="Date", y="count", color="Country/Region")

fig_cases_overall_diff = px.line(byDateWorldWide, x="Date", y="diff")

# Configure Dash layout
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server
app.layout = html.Div(className='container-fluid', children=[

    html.Div(className='jumbotron', children=[
        dcc.Markdown(f'''
        # COVID-19 Dashboard
        All information is pulled from the Johns Hopkins University [Github Page](https://www.github.com/CSSEGISandData)''')
    ]),
    dbc.Row(
        dbc.Col([
            dcc.Graph(
                id='fig_cases_by_country',
                figure=fig_cases_by_country
            ),
        ])
    ),
    dbc.Row(
        dbc.Col([
            dcc.Graph(
                id='fig_cases_overall_diff',
                figure=fig_cases_overall_diff
            ),
        ])
    ),
])

if __name__ == '__main__':
    app.run_server(debug=False)
