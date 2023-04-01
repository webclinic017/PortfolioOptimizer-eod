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

    def mean(self):
        """
        Calculate the mean.
        :return mean: The mean of the portfolio.
        """
        mean = np.mean(np.dot(self.weights, self.returns.T))

        return mean

    def sharpe_ratio(self):
        """
        Calculate the Sharpe ratio.
        :return sharpe_ratio: The Sharpe ratio of the portfolio.
        """
        sharpe_ratio = self.mean() / self.stddev()

        return sharpe_ratio
