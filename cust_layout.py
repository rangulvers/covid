import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from corona import dataset


card_fig_cases_by_country = [
    dbc.CardHeader("New daily cases"),
    dbc.CardBody(
        [
            dcc.Graph(
                id='fig_cases_by_country'
            ),
        ]
    ),
]

card_fig_overall = [
    dbc.CardHeader("Overall cases"),
    dbc.CardBody(
        [
            dcc.Graph(
                id='fig_overall_cases'
            ),
        ]
    ),
]


view = html.Div(className='container-fluid', children=[

    html.Div(className='jumbotron', children=[
        dcc.Markdown('''
        # COVID-19 Dashboard
        All information is pulled from the Johns Hopkins University [Github Page](https://www.github.com/CSSEGISandData)''')
    ]),
    dbc.Row(
        dbc.Col([
            dcc.Dropdown(
                id='filter_by_country',
                options=[{'label': i, 'value': i}
                         for i in dataset.filter],
                value='Germany'
            ),
        ])
    ),
    dbc.Row(
        [
            dbc.Col(dbc.Card(card_fig_cases_by_country,
                             color="dark", inverse=True)),
            dbc.Col(dbc.Card(card_fig_overall,
                             color="dark", inverse=True)),

        ]
    )
])
