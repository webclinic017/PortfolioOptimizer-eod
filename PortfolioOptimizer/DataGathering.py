"""
Sets up connections and pulls data.
"""

import pandas as pd
import requests


class EodhdDataGathering(object):
    """
    Connects to eodhd and pulls data.
    """

    def __init__(self, api_key):
        """
        Args:
            api_key(string): The API key for eodhd.
        """

        self.api_key = api_key

    def get_data(self, ticker, start_date=None, end_date=None):
        """
        Gets data from eodhd.

        Args:
            ticker(string): The ticker to pull data for. Should really
                be ticker.exchange, such as AAPL.US.
            start_date(string): The start date to pull data for.
                Format as YYYY-MM-DD.
            end_date(string): The end date to pull data for.
                Format as YYYY-MM-DD.

        Returns:
            df(pandas DataFrame): The data.
        """

        # demo url (the MCD.US is part of the demo url):
        # 'https://eodhistoricaldata.com/api/eod/MCD.US'
        params = {'api_token': 'demo', 'from': start_date, 'to': end_date, 'period': 'd', 'fmt': 'json'}
        url = 'https://eodhistoricaldata.com/api/eod/' + ticker
        #params = {'api_token': self.api_key, 'from': start_date, 'to': end_date, 'period': 'd', 'fmt': 'json'}
        response = requests.get(url, params=params)

        data = response.json()
        df = pd.DataFrame(data)

        return df
