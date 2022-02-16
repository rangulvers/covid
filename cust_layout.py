import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from corona import dataset


view = html.Div(className='container-fluid', children=[

    html.Div(className='jumbotron', children=[
        dcc.Markdown('''
        # COVID-19 Dashboard
        All information is pulled from the Johns Hopkins University [Github Page](https://www.github.com/CSSEGISandData)''')
    ]),
    html.Div(id='select_chart_theme_output'),
    dbc.Row(
        dbc.Col(
            dbc.Card(
                dbc.CardBody(
                    [
                        dbc.Col(dbc.InputGroup(
                            [
                                dbc.InputGroupText("Select Country"),
                                dbc.Select(
                                    id='filter_by_country',
                                    options=[{'label': i, 'value': i}
                                             for i in dataset.filter],
                                    value='Germany'
                                )

                            ]
                        )),
                        dbc.Col(dbc.InputGroup(
                            [
                                dbc.InputGroupText("Select Chart Theme"),
                                dbc.Select(
                                    id='select_chart_theme',
                                    options=[{'label': i, 'value': i}
                                             for i in dataset.chart_themes],
                                    value='simple_white'
                                )

                            ]
                        ))
                    ]
                )
            )
        )
    ),
    html.Br(),
    dbc.Row(
        [
            dbc.Col(
                dbc.Card(
                    [
                        dbc.CardHeader("New daily cases"),
                        dbc.CardBody(
                            [
                                dcc.Graph(
                                    id='fig_cases_by_country'
                                ),
                            ]
                        ),
                    ],
                    color="primary", outline=True)),
            dbc.Col(
                dbc.Card(
                    [
                        dbc.CardHeader("Overall cases"),
                        dbc.CardBody(
                            [
                                dcc.Graph(
                                    id='fig_overall_cases'
                                ),
                            ]
                        ),
                    ],
                    color="primary", outline=True)),
        ]
    )
])
