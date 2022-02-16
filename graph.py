import plotly.express as px
import plotly.graph_objects as go


class Graph(object):

    def overall_cases_graph(overall, country_filter):
        fig_overall_cases = px.line(
            overall, x="Date", y="count", title=f"Overall cases for : {country_filter}", template="simple_white")

        return fig_overall_cases

    def new_cases_graph(bycountry):
        fig_cases_by_country = go.Figure(data=[
            go.Bar(x=bycountry["Date"],
                   y=bycountry["diff"],
                   name="# of Cases"),
            go.Line(x=bycountry["Date"],
                    y=bycountry["7days"],
                    name="7 days avg.")
        ])

        return fig_cases_by_country
