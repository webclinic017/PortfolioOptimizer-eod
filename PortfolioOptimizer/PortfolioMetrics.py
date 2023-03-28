"""
Define metrics about the portfolio.
:class PortfolioMetrics: Calculate metrics about the portfolio.
"""

import numpy as np
import pandas as pd


class PortfolioMetrics(object):
    """
    Calculate metrics about the portfolio.
    """
    def __init__(self, returns: pd.DataFrame, weights: list) -> None:
        """
        :param returns: The returns of the different assets you want in
            the portfolio.
        :param weights: The weights for the portfolio.
        """
        self.returns = returns
        self.weights = weights

    def stddev(self):
        """
        Calculate the standard deviation.
        :return stddev: The standard deviation of the portfolio.
        """
        stddev = np.std(np.dot(self.weights, self.returns.T))

        return stddev
