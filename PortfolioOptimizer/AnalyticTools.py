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
        # multiply by 100 since the optimizer needs higher values to work
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
        # multiply by 100 since the optimizer needs higher values to work
        opt_engine = Optimizer(user_return_data * 100)
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

    def portfolio_metrics(self, returns: pd.DataFrame, weights: list) -> dict:
        """Calculate the metrics for the portfolio."""
        metrics_engine = PortfolioMetrics(returns, weights)
        metrics = {
            'Average': [metrics_engine.mean()],
            'Volatility': [metrics_engine.stddev()],
            'Sharpe Ratio': [metrics_engine.sharpe_ratio()]
        }

        return metrics

    def label_imp_metrics(self, metrics: pd.Series) -> dict:
        """Label the imputed metrics."""
        metrics = {
            'Average': [metrics.iloc[0]],
            'Volatility': [metrics.iloc[1]],
            'Sharpe Ratio': [metrics.iloc[2]]
        }

        return metrics
