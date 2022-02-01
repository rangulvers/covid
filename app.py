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
df_confirmed_flat["Date"] = pd.to_datetime(df_confirmed_flat["Date"])
# create filter based on countrys
filter = df_confirmed_flat["Country/Region"].unique()


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
            dcc.Dropdown(
                id='filter_by_country',
                options=[{'label': i, 'value': i} for i in filter],
                value='Germany'
            ),
        ])
    ),
    dbc.Row(
        dbc.Col([
            dcc.Graph(
                id='fig_cases_by_country'
            ),
        ])
    )
])


@app.callback(
    dash.dependencies.Output('fig_cases_by_country', 'figure'),
    [dash.dependencies.Input('filter_by_country', 'value')]
)
def update_graph(country_filter):
    dfcf = df_confirmed_flat[df_confirmed_flat["Country/Region"]
                             == country_filter]
    dfcf["diff"] = dfcf["count"].diff()
    dfcf["7days"] = dfcf["count"].rolling(7).sum()

    fig_cases_by_country = px.bar(
        dfcf, x="Date", y="diff", title=f"New daily cases for : {country_filter}")
    return fig_cases_by_country


if __name__ == '__main__':
    app.run_server(debug=False)
