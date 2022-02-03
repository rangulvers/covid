import pandas as pd


class Corona(object):
    def __init__(self):
        self.url_confirmed = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv"
        self.df_confirmed = None
        self.df_confirmed_flat = None
        self.filter = None

    def create_df(self):

        # Create Datasets
        self.df_confirmed = pd.read_csv(
            self.url_confirmed, error_bad_lines=False)
        self.df_confirmed.iloc[:,
                               4:] = self.df_confirmed.iloc[:, 4:].clip(lower=0)

        # Flatten Datasets to fit charts
        self.df_confirmed_flat = self.df_confirmed.melt(var_name="Date", value_name="count", id_vars=[
            "Province/State", "Country/Region", "Lat", "Long"])
        self.df_confirmed_flat["Date"] = pd.to_datetime(
            self.df_confirmed_flat["Date"])
        # create filter based on countrys
        self.filter = self.df_confirmed_flat["Country/Region"].unique()

    def new_cases_graph_data(self, country_filter):
        bycountry = self.df_confirmed_flat[self.df_confirmed_flat["Country/Region"]
                                           == country_filter]
        bycountry["diff"] = bycountry["count"].diff()
        bycountry["7days"] = bycountry["count"].rolling(7).sum()

        return bycountry

    def new_overall_cases_graph(self, country_filter):
        overall = self.df_confirmed_flat[self.df_confirmed_flat["Country/Region"]
                                         == country_filter]

        return overall


dataset = Corona()
dataset.create_df()