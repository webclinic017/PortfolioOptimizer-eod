"""Wrappers for variables that can be stored in SessionStates. This is
useful for storing variables that are the outputs of class functions,
which are hard to cache."""

from PortfolioOptimizer.DataTools import DataTools

import streamlit as st


def state_pull_ticker_tables():
    """Get the asset class data tables."""
    if 'tables' in st.session_state:
        tables = st.session_state.tables
    else:
        data_engine = DataTools()
        tables = data_engine.pull_ticker_tables()
        st.session_state.tables = tables
    return tables

def state_pull_return_data(tables):
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
