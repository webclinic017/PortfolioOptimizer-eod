"""
An optimizer for portfolio optimization.
:class Optimizer: Helps with the setup and run of an optimization.
"""

import numpy as np
import pandas as pd

from typing import Union


def sharpe_ratio(weights: Union[list, np.ndarray],
                 returns: Union[pd.DataFrame, np.ndarray]) -> float:
    """
    Calculate the Sharpe Ratio.
    :param weights: The weights for the portfolio.
    :param returns: The returns for the portfolio.
    :return sharpe_ratio: The Sharpe Ratio.
    """
    avg = np.average(np.dot(weights, returns.T))
    stddev = np.std(np.dot(weights, returns.T))
    sharpe_ratio = avg / stddev

    return sharpe_ratio


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
    def __init__(self) -> None:
        pass
