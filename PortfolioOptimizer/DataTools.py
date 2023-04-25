"""
Tools for handling data and the info around it.
:class DataTools: Tools for handling data and the info around it.
"""

from PortfolioOptimizer import GlobalVariables as gv
from PortfolioOptimizer.GCPTools import GCPTools

import pandas as pd
import streamlit as st

from arch.bootstrap import optimal_block_length
from arch.bootstrap import StationaryBootstrap
from statsmodels.imputation import mice
from typing import Tuple, Union


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
            curr_price_data = gcp_engine.pull_df_bigquery(
                'portfoliooptimization-364417', 'assetclassprices', table,
                'date')
            curr_price_data.index = pd.to_datetime(curr_price_data.index)
            curr_price_data = curr_price_data[['adjclose']]
            col_name = table.split('_')[0]
            curr_price_data.columns = [col_name]
            if i == 0:
                price_data = curr_price_data
            else:
                price_data = pd.concat([price_data, curr_price_data], axis=1)

        # calculate returns
        returns = price_data.pct_change()
        returns = returns.iloc[1:, :]

        return returns

    def get_user_data(self, investment_selection: list,
                      return_data: pd.DataFrame) -> Tuple[pd.DataFrame, bool]:
        """
        Get the return data for the investments the user selected, as well
            as an indicator for whether any data is missing.
        :param investment_selection: The investments the user selected.
        :param return_data: The return data for all investments.
        :return user_data: The return data for the selected investments.
        :return missing_data: An indicator for whether any data is
            missing.
        """
        # get data for the selected investments
        user_tickers = [gv.SECURITY_MAPPING[x][0] for x in
                        investment_selection]
        # remove the .US from the ticker if it's there and make it
        # lowercase
        user_tickers = [x.split('.')[0].lower() for x in user_tickers]

        # get the data for the selected investments
        user_data = return_data[user_tickers]
        # also get an indicator for whether any data is missing
        missing_data = user_data.isnull().values.any()

        return user_data, missing_data

    def get_bootstrap_data_ts(self, data: Union[pd.DataFrame, pd.Series],
                              seed: int, bs_count: int,
                              opt_col: str = None, exponent: int = 1) \
            -> Union[pd.DataFrame, pd.Series]:
        """
        Gets bootstrap data from a set of time series data.
        :param seed: The seed for bootstrapping for reproducibility.
        :param bs_count: The number of iterations of the bootstrap.
        :param opt_col: The name of the column to optimize the bootstrap
            length on if we have a DataFrame (we don't need this with a
            Series). If None, we will calculate for all columns and then
            take the max.
        :param exponent: The exponent to use for the data when determining
            the optimal block length. So if exponent is 2, we will use the
            squared data.
        :return data[0][0]: The resulting data after bootstrap. This is a
            generator, so it will only output the current data.
        """
        # alter the data to use the exponent
        if exponent != 1:
            data = data ** exponent

        # get the optimal value for the block length either as a given
        # column or the max of all columns
        if isinstance(data, pd.Series):
            opt = optimal_block_length(data)
            opt_value = round(opt["stationary"], 0)
        # this is the case of choosing a column in a DataFrame to use
        elif opt_col is not None:
            opt = optimal_block_length(data.loc[:, opt_col])
            opt_value = round(opt.loc[opt_col, "stationary"], 0)
        # this is the case of using the max of all columns
        else:
            opt = optimal_block_length(data)
            opt_value = round(opt.max(axis=0)["stationary"], 0)

        # run the bootstrap
        bs = StationaryBootstrap(opt_value, data, seed=seed)
        for bs_data in bs.bootstrap(bs_count):
            yield bs_data[0][0]

    def pmm(self, data: pd.DataFrame, d: int) -> pd.DataFrame:
        """
        Perform predictive mean matching and yield a result.
        :param data: The data to perform PMM on.
        :param d: The number of imputations to perform.
        :return imp_data: The data with PMM applied.
        """
        # set up the imputer
        imp = mice.MICEData(data)
        for i in range(d):
            # perform PMM
            imp.update_all()
            # get the imputed data
            imp_data = imp.data
            imp_data.index = data.index

            yield imp_data
