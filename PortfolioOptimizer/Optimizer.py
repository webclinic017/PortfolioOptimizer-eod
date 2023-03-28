"""
An optimizer for portfolio optimization.
:class Optimizer: Helps with the setup and run of an optimization.
"""

import numpy as np
import pandas as pd

from scipy.optimize import minimize
from typing import Union


def max_return(weights: Union[list, np.ndarray],
               returns: Union[pd.DataFrame, np.ndarray]) -> float:
    """
    Calculate the maximum return.
    :param weights: The weights for the portfolio.
    :param returns: The returns for the portfolio.
    :return avg_return: The average return.
    """
    max_return = np.dot(weights, returns.T)
    avg_return = np.average(max_return)

    return avg_return


class Optimizer(object):
    """
    Helps with the setup and run of an optimization.
    """
    def __init__(self, returns: pd.DataFrame) -> None:
        """
        :param returns: The returns of the different assets you want in
            the portfolio.
        """
        self.returns = returns

    def sharpe_ratio(self, weights: Union[list, np.ndarray]) -> float:
        """
        Calculate the Sharpe Ratio.
        :param weights: The weights for the portfolio.
        :return neg_sharpe_ratio: The negative of the Sharpe Ratio since
            we want to maximize it, but are using a minimizer.
        """
        avg = np.average(np.dot(weights, self.returns.T))
        stddev = np.std(np.dot(weights, self.returns.T))
        sharpe_ratio = avg / stddev
        neg_sharpe_ratio = -1 * sharpe_ratio

        return neg_sharpe_ratio

    def optimize(self, method: str = 'sharpe_ratio') -> pd.DataFrame:
        """
        Run the optimization to get the weights for the portfolio.
        :param method: The method to use for optimization. Takes either
            'sharpe_ratio' or 'max_return'.
        :return results: The results of the optimization.
        """
        # set up the starting weights
        x0 = np.ones(self.returns.shape[1]) / self.returns.shape[1]

        # set up the constraints
        # we want the holdings to be long-only
        bnds = tuple((0, 1) for _ in range(self.returns.shape[1]))
        # we want the sum of the weights to be 1
        cons = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1})

        # get the objective function
        if method == 'sharpe_ratio':
            func = self.sharpe_ratio
        else:
            func = max_return

        # run the optimization
        results = minimize(func, x0, bounds=bnds, constraints=cons).x

        return results
