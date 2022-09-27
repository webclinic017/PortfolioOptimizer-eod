"""
Sets up connections and pulls data.
"""

import requests

from eodhd import APIClient


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

    def get_data(self): #, ticker, start_date, end_date):
        """
        Gets data from eodhd.

        Args:
            ticker(string): The ticker to pull data for.
            start_date(string): The start date to pull data for.
            end_date(string): The end date to pull data for.

        Returns:
            data(pandas DataFrame): The data.
        """

        client = APIClient(self.api_key)

        # demo url: 'https://eodhistoricaldata.com/api/eod/MCD.US'
        # use with 'api_token': 'demo'
        url = 'https://eodhistoricaldata.com/api/eod/MCD.US'
        params = {'api_token': 'demo', 'period': 'd', 'fmt': 'json'}
        response = requests.get(url, params=params)

        data = response.json()

        return data
