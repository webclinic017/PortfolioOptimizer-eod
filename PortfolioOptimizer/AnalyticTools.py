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
        opt_engine = Optimizer(bench_rets)
        bench_stddev = opt_engine.stddev(bench_weights)

        return bench_stddev

    def run_optimization(self, user_return_data: pd.DataFrame,
                         obj_func: str, objective_selection: str,
                         return_data: pd.DataFrame) -> pd.DataFrame:
        """Run the optimization based on the user's asset choices returns
            and the objective function selected by the user."""
        # multiply by 100 since the optimizer needs higher values to work
        opt_engine = Optimizer(user_return_data * 100)
        if obj_func == 'max_return':
            # if we want the max return, we need to find the vol of
            # the benchmark mix of stocks and bonds
            bench_stddev = self._stock_bond_vol(
                return_data[['acwi', 'bnd']], objective_selection)
            weights = opt_engine.optimize(obj_func, bench_stddev)
        else:
            weights = opt_engine.optimize(obj_func)

        return weights

    def portfolio_metrics(self, port_returns: pd.DataFrame, weights: list,
                          obj_func: str, objective_selection: str,
                          return_data: pd.DataFrame,
                          metrics: dict) -> dict:
        """
        Calculate the metrics for the portfolio and a benchmark if
            we are looking at optimizing for max return. This is for
            imputed data, so we make it easy to extend and plan to label
            it later.
        :param port_returns: The returns of the portfolio assets.
        :param weights: The weights of the portfolio assets.
        :param obj_func: The objective function used to optimize the
            portfolio.
        :param objective_selection: The objective selection, which we
            might need to use to find the benchmark weights.
        :param return_data: The return data that includes the benchmark
            assets.
        :param metrics: The metrics dictionary that we will append to.
        :return metrics: The metrics dictionary with the new metrics
            appended. Includes the average, volatility, and Sharpe ratio.
            As well as the same for the benchmark if the objective is
            max_return.
        """
        metrics_engine = PortfolioMetrics(port_returns, weights)
        if metrics:
            metrics['Average'] = metrics['Average'].append(
                metrics_engine.mean())
            metrics['Volatility'] = metrics['Volatility'].append(
                metrics_engine.stddev())
            metrics['Sharpe Ratio'] = metrics['Sharpe Ratio'].append(
                metrics_engine.sharpe_ratio())
        else:
            metrics = {
                'Average': [metrics_engine.mean()],
                'Volatility': [metrics_engine.stddev()],
                'Sharpe Ratio': [metrics_engine.sharpe_ratio()]
            }

        if obj_func == 'max_return':
            # if we want the max return, get the benchmark based on the
            # weights of the stocks and bonds
            bench_rets = return_data[['acwi', 'bnd']]
            bench_weights = gv.OBJECTIVE_CHOICES[objective_selection][1]
            bench_metrics_engine = PortfolioMetrics(bench_rets, bench_weights)
            # then calculate the metrics for the benchmark
            if 'Bench Average' in metrics:
                metrics['Bench Average'] = metrics['Bench Average'].append(
                    bench_metrics_engine.mean())
                metrics['Bench Volatility'] = \
                    metrics['Bench Volatility'].append(
                        bench_metrics_engine.stddev())
                metrics['Bench Sharpe Ratio'] = \
                    metrics['Bench Sharpe Ratio'].append(
                        bench_metrics_engine.sharpe_ratio())
            else:
                metrics['Bench Average'] = [bench_metrics_engine.mean()],
                metrics['Bench Volatility'] = [bench_metrics_engine.stddev()],
                metrics['Bench Sharpe Ratio'] = [
                    bench_metrics_engine.sharpe_ratio()]

        return metrics

    def average_metrics(self, imp_metrics: dict) -> dict:
        """Label the imputed metrics."""
        metrics = {
            'Average': [imp_metrics['Average'].mean()],
            'Volatility': [imp_metrics['Volatility'].mean()],
            'Sharpe Ratio': [imp_metrics['Sharpe Ratio'].mean()]
        }

        # include the benchmark metrics if they exist
        if 'Bench Average' in imp_metrics:
            metrics['Average'] = metrics['Average'].append(
                imp_metrics['Bench Average'].mean())
            metrics['Volatility'] = metrics['Volatility'].append(
                imp_metrics['Bench Volatility'].mean())
            metrics['Sharpe Ratio'] = metrics['Sharpe Ratio'].append(
                imp_metrics['Bench Sharpe Ratio'].mean())

        return metrics
