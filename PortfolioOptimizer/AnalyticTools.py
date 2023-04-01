"""
Tools for data analytics.
:class AnalyticTools: Tools for data analytics.
"""

from PortfolioOptimizer import GlobalVariables as gv
from PortfolioOptimizer.PortfolioMetrics import PortfolioMetrics

import pandas as pd


class AnalyticTools(object):
    def __init__(self) -> None:
        pass

    def stock_bond_vol(self, return_data: pd.DataFrame,
                       objective_selection: str) -> float:
        """Calculate the volatility of the stock and bond portfolio given
            a desired weight in each."""
        bench_rets = return_data * 100
        # the weights are defined in the GlobalVariables file
        bench_weights = gv.OBJECTIVE_CHOICES[objective_selection][1]
        metrics_engine = PortfolioMetrics(bench_rets, bench_weights)
        bench_stddev = metrics_engine.stddev()

        return bench_stddev
