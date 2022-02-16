import corona
import dash
import cust_layout
import graph


# Configure the Dash App
app = dash.Dash(__name__, external_stylesheets=[
                cust_layout.dbc.themes.MINTY])
app.layout = cust_layout.view
server = app.server


@app.callback(
    dash.dependencies.Output('select_chart_theme_output', 'children'),
    [dash.dependencies.Input('select_chart_theme', 'value')]
)
def set_chart_theme(chart_theme):
    graph.Graph.theme = chart_theme


@app.callback(
    dash.dependencies.Output('fig_cases_by_country', 'figure'),
    [dash.dependencies.Input('filter_by_country', 'value')]
)
def create_new_cases_graph(country_filter):
    bycountry = corona.dataset.new_cases_graph_data(country_filter)
    fig_cases_by_country = graph.Graph.new_cases_graph(bycountry)
    return fig_cases_by_country


@app.callback(
    dash.dependencies.Output('fig_overall_cases', 'figure'),
    [dash.dependencies.Input('filter_by_country', 'value')]
)
def create_overall_cases_graph(country_filter):
    overall = corona.dataset.new_overall_cases_graph(country_filter)
    fig_overall_cases = graph.Graph.overall_cases_graph(
        overall, country_filter)

    return fig_overall_cases


if __name__ == '__main__':
    app.run_server(debug=False)
