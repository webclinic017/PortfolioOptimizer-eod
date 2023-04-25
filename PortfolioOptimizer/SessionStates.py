"""Wrappers for variables that can be stored in SessionStates. This is
useful for storing variables that are the outputs of class functions,
which are hard to cache."""

from PortfolioOptimizer.AnalyticTools import AnalyticTools
from PortfolioOptimizer.DataTools import DataTools

import pandas as pd
import streamlit as st


def state_pull_ticker_tables() -> list:
    """Get the asset class data tables."""
    if 'tables' in st.session_state:
        tables = st.session_state.tables
    else:
        data_engine = DataTools()
        tables = data_engine.pull_ticker_tables()
        st.session_state.tables = tables
    return tables


def state_pull_return_data(tables: list) -> pd.DataFrame:
    """Get the asset class return data."""
    if 'return_data' in st.session_state and \
            st.session_state.return_tables == tables:
        return_data = st.session_state.return_data
    else:
        data_engine = DataTools()
        return_data = data_engine.pull_return_data(tables)
        st.session_state.return_data = return_data
        st.session_state.return_tables = tables
    return return_data


def state_bootstrap_optimization(user_return_data: pd.DataFrame,
                                 obj_func: str, objective_selection: str,
                                 return_data: pd.DataFrame) -> pd.DataFrame:
    """Bootstrap the return data and run the optimization based on the
        user's asset choices returns and the objective function
        selected by the user."""
    if 'bs_weights' in st.session_state and \
            st.session_state.bs_user_return_data.equals(user_return_data) and \
            st.session_state.bs_obj_func == obj_func and \
            st.session_state.bs_objective_selection == objective_selection \
            and st.session_state.bs_return_data.equals(return_data):
        weights = st.session_state.bs_weights
    else:
        analytics_engine = AnalyticTools()
        weights = analytics_engine.bootstrap_optimization(
            user_return_data, obj_func, objective_selection,
            return_data)
        st.session_state.bs_user_return_data = user_return_data
        st.session_state.bs_obj_func = obj_func
        st.session_state.bs_objective_selection = objective_selection
        st.session_state.bs_return_data = return_data
        st.session_state.bs_weights = weights
    return weights


def state_pmm(data: pd.DataFrame, d: int) -> list:
    """Impute missing data using the predictive mean matching method."""
    if 'imp_data' in st.session_state and st.session_state.pmm_data.equals(
            data) and st.session_state.pmm_d == d:
        imp_data = st.session_state.imp_data
    else:
        data_engine = DataTools()
        imp_data_gen = data_engine.pmm(data, d)
        imp_data = []
        for _ in range(d):
            imp_data.append(next(imp_data_gen))
        st.session_state.pmm_data = data
        st.session_state.pmm_d = d
        st.session_state.imp_data = imp_data
    return imp_data
