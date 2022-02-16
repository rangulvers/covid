import plotly.express as px
import plotly.graph_objects as go


class Graph(object):
    theme = "simple_white"

    def overall_cases_graph(overall, country_filter):

        fig_overall_cases = go.Figure(data=[
            go.Line(
                x=overall["Date"],
                y=overall["count"],
                name="Overall cases"
            )
        ])

        fig_overall_cases.update_layout(template=Graph.theme)

        fig_overall_cases.update_layout(
            xaxis=dict(
                rangeselector=dict(
                    buttons=list([
                        dict(count=1,
                             label="1m",
                             step="month",
                             stepmode="backward"),
                        dict(count=6,
                             label="6m",
                             step="month",
                             stepmode="backward"),
                        dict(count=1,
                             label="YTD",
                             step="year",
                             stepmode="todate"),
                        dict(count=1,
                             label="1y",
                             step="year",
                             stepmode="backward"),
                        dict(step="all")
                    ])
                ),
                rangeslider=dict(
                    visible=True
                ),
                type="date"
            )
        )

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

        fig_cases_by_country.update_layout(template=Graph.theme)

        fig_cases_by_country.update_layout(
            xaxis=dict(
                rangeselector=dict(
                    buttons=list([
                        dict(count=1,
                             label="1m",
                             step="month",
                             stepmode="backward"),
                        dict(count=6,
                             label="6m",
                             step="month",
                             stepmode="backward"),
                        dict(count=1,
                             label="YTD",
                             step="year",
                             stepmode="todate"),
                        dict(count=1,
                             label="1y",
                             step="year",
                             stepmode="backward"),
                        dict(step="all")
                    ])
                ),
                rangeslider=dict(
                    visible=True
                ),
                type="date"
            )
        )

        return fig_cases_by_country
