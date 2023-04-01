"""
Tools for data analytics.
:class AnalyticTools: Tools for data analytics.
"""

from PortfolioOptimizer import GlobalVariables as gv
from PortfolioOptimizer.Optimizer import Optimizer
from PortfolioOptimizer.PortfolioMetrics import PortfolioMetrics

import pandas as pd


class AnalyticTools(object):
    def __init__(self) -> None:
        pass

    def _stock_bond_vol(self, return_data: pd.DataFrame,
                       objective_selection: str) -> float:
        """Calculate the volatility of the stock and bond portfolio given
            a desired weight in each."""
        bench_rets = return_data * 100
        # the weights are defined in the GlobalVariables file
        bench_weights = gv.OBJECTIVE_CHOICES[objective_selection][1]
        metrics_engine = PortfolioMetrics(bench_rets, bench_weights)
        bench_stddev = metrics_engine.stddev()

        return bench_stddev

    def run_optimization(self, user_return_data: pd.DataFrame,
                         objective_selection: str,
                         return_data: pd.DataFrame) -> pd.DataFrame:
        """Run the optimization based on the user's asset choices returns
            and the objective function selected by the user."""
        opt_engine = Optimizer(user_return_data)
        obj_func = gv.OBJECTIVE_CHOICES[objective_selection][0]
        if obj_func == 'max_return':
            # if we want the max return, we need to find the vol of
            # the benchmark mix of stocks and bonds
            bench_stddev = self._stock_bond_vol(
                return_data[['acwi', 'bnd']], objective_selection)
            weights = opt_engine.optimize(obj_func, bench_stddev)
        else:
            weights = opt_engine.optimize(obj_func)

        return weights

    def average_weights(self, imp_weights: list) -> pd.DataFrame:
        """Calculate the average weights for the portfolio."""
        avg_weights = pd.DataFrame(imp_weights).mean()
        import streamlit as st
        st.write(avg_weights)
        avg_weights = avg_weights / avg_weights.sum()

        return avg_weights
