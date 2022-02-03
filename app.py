from tkinter import BEVEL
import corona
import plotly.express as px
import plotly.graph_objects as go
import dash
import cust_layout


# Configure the Dash App
app = dash.Dash(__name__, external_stylesheets=[
                cust_layout.dbc.themes.BOOTSTRAP])
app.layout = cust_layout.view
server = app.server


@app.callback(
    dash.dependencies.Output('fig_cases_by_country', 'figure'),
    [dash.dependencies.Input('filter_by_country', 'value')]
)
def create_new_cases_graph(country_filter):
    bycountry = corona.dataset.new_cases_graph_data(country_filter)

    fig_cases_by_country = px.bar(
        bycountry, x="Date", y="diff", title=f"New daily cases for : {country_filter}", template="simple_white")

    return fig_cases_by_country


@app.callback(
    dash.dependencies.Output('fig_overall_cases', 'figure'),
    [dash.dependencies.Input('filter_by_country', 'value')]
)
def create_overall_cases_graph(country_filter):
    overall = corona.dataset.new_overall_cases_graph(country_filter)
    fig_overall_cases = px.line(
        overall, x="Date", y="count", title=f"Overall cases for : {country_filter}", template="simple_white")

    return fig_overall_cases


if __name__ == '__main__':
    app.run_server(debug=False)
