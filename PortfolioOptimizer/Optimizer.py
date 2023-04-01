"""
An optimizer for portfolio optimization.
:class Optimizer: Helps with the setup and run of an optimization.
"""

import numpy as np
import pandas as pd

from scipy.optimize import minimize
from typing import Union


class Optimizer(object):
    """
    Helps with the setup and run of an optimization.
    """
    def __init__(self, returns: pd.DataFrame) -> None:
        """
        :param returns: The returns of the different assets you want in
            the portfolio.
        """
        # the optimizer can fail to move if the returns are too small
        self.returns = returns * 100
        # set up the starting weights
        self.x0 = np.ones(self.returns.shape[1]) / self.returns.shape[1]
        # set up the bounds - we want the holdings to be long-only
        self.bnds = tuple((0, 1) for _ in range(self.returns.shape[1]))
        # set up constraints later
        self.cons = None

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

    def max_return(self, weights: Union[list, np.ndarray]) -> float:
        """
        Calculate the maximum return.
        :param weights: The weights for the portfolio.
        :return neg_avg_return: The negative of the average return since
            we want to maximize it, but are using a minimizer.
        """
        avg = np.mean(np.dot(weights, self.returns.T))
        neg_avg_return = -1 * avg

        return neg_avg_return

    def stddev(self, weights: Union[list, np.ndarray]) -> float:
        """
        Calculate the standard deviation.
        :param weights: The weights for the portfolio.
        :return stddev: The standard deviation of the portfolio.
        """
        stddev = np.std(np.dot(weights, self.returns.T))

        return stddev

    def optimize(self, method: str = 'sharpe_ratio',
                 tgt_stddev: float = None) -> pd.DataFrame:
        """
        Run the optimization to get the weights for the portfolio.
        :param method: The method to use for optimization. Takes either
            'sharpe_ratio' or 'max_return'.
        :param tgt_stddev: The target standard deviation for the portfolio
            if you need it to optimize with 'max_return'.
        :return results: The results of the optimization.
        """
        # get the objective function and set constraints
        if method == 'sharpe_ratio':
            func = self.sharpe_ratio
            # we want the sum of the weights to be 1
            self.cons = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1})
        else:
            func = self.max_return
            # we want the sum of the weights to be 1 and the std dev
            # to be equal to the target
            self.cons = (
                {'type': 'eq', 'fun': lambda x: np.sum(x) - 1},
                {'type': 'eq', 'fun': lambda x: self.stddev(x) - tgt_stddev})

        # run the optimization
        results = minimize(func, self.x0, bounds=self.bnds,
                           constraints=self.cons)

        # if the optimization failed and we are looking for max return,
        # try again with the standard deviation as a constraint but allow
        # the weights to be between 0 and 1, which would mean that if this
        # succeeds, we would have a portfolio with less than 100% invested
        # and the rest would be cash
        if not results.success and method == 'max_return':
            self.cons = (
                {'type': 'eq', 'fun': lambda x: self.stddev(x) - tgt_stddev},
                {'type': 'ineq', 'fun': lambda x: np.sum(x)},
                {'type': 'ineq', 'fun': lambda x: 1 - np.sum(x)})
            results = minimize(func, self.x0, bounds=self.bnds,
                               constraints=self.cons)

        # if the optimization fails, return None
        # this should only happen if the target standard deviation is
        # higher than the standard deviation of any asset in the portfolio
        if not results.success:
            return None

        return results.x
