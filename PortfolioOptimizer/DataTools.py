"""
Tools for handling data and the info around it.
:class DataTools: Tools for handling data and the info around it.
"""

from PortfolioOptimizer import GlobalVariables as gv
from PortfolioOptimizer.GCPTools import GCPTools

import pandas as pd
import streamlit as st


class DataTools(object):
    """
    Tools for handling data and the info around it.
    """
    def __init__(self) -> None:
        pass

    def pull_ticker_tables(self) -> list:
        """Pull all table names for tickers that we will need for BQ."""
        tickers = list(gv.SECURITY_MAPPING.values())
        tickers = [value[0] for value in tickers]
        tickers = [ticker.split('.')[0] for ticker in tickers]
        tables = [ticker.lower() + '_daily' for ticker in tickers]

        return tables

    def pull_return_data(self, tables: list) -> pd.DataFrame:
        """
        Pull return data from BigQuery.
        :param tables: The set of tables to pull from.
        :return returns: The returns for each ticker.
        """
        gcp_engine = GCPTools('bigquery',
                              'https://www.googleapis.com/auth/bigquery',
                              st.secrets['gcp_bigquery_service_account'])

        # get each set of price data and take the adjusted close
        # combine all so they are in one dataframe
        for i, table in enumerate(tables):
            if i == 0:
                price_data = gcp_engine.pull_df_bigquery(
                    'portfoliooptimization-364417', 'assetclassprices', table)
                price_data = price_data[['adjclose']]
                price_data.columns = [table]
            else:
                curr_price_data = gcp_engine.pull_df_bigquery(
                    'portfoliooptimization-364417', 'assetclassprices', table)
                curr_price_data = curr_price_data[['adjclose']]
                curr_price_data.columns = [table]
                price_data = pd.concat([price_data, curr_price_data], axis=1)

        # calculate returns
        returns = price_data.pct_change()

        return returns
