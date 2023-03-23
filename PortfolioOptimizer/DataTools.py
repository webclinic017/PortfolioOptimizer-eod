"""
Tools for handling data and the info around it.
:class DataTools: Tools for handling data and the info around it.
"""

from PortfolioOptimizer import GlobalVariables as gv


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
