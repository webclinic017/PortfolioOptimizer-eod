"""
Runs the portfolio optimizer.
"""

from PortfolioOptimizer import GlobalVariables as gv
from PortfolioOptimizer.AnalyticTools import AnalyticTools
from PortfolioOptimizer.DataTools import DataTools
from PortfolioOptimizer.StreamlitTools import StreamlitTools

import pandas as pd
import streamlit as st


def main():
    ####################################################################
    # Basic Setup
    ####################################################################

    # set up the page
    st.set_page_config(page_title="Portfolio Optimizer", layout="wide")

    # first, give the user basic info about the tool
    # formatting done with css/html
    col1_title, col2_title, col3_title = st.columns(3)
    with col2_title:
        title_writing = "Portfolio Optimizer"
        title_format = f'<p style="text-align: center; ' \
                       f'font-family:Garamond; color:blue; ' \
                       f'font-size: 40px; font-weight: bold;">' \
                       f'{title_writing}</p>'
        st.markdown(title_format, unsafe_allow_html=True)
    # and set up the sidebar too
    sidebar_title_format = f'<p style="text-align: center; ' \
                           f'font-family:Garamond; color:blue; ' \
                           f'font-size: 30px; font-weight: bold;">' \
                           f'{title_writing}</p>'
    st.sidebar.markdown(sidebar_title_format, unsafe_allow_html=True)

    # define tools for use throughout
    data_engine = DataTools()
    analytics_engine = AnalyticTools()
    format_engine = StreamlitTools()

    ####################################################################
    # User Options
    ####################################################################

    # define what the tool does for the user
    st.write("This tool will help you optimize your portfolio by finding the "
             "optimal weights based on the investments you have available "
             "and your desired risk.")
    st.write("First, choose those investments you would like to include. We "
             "suggest using a set of investments that are as exhaustive and "
             "non-overlapping as possible. By having an exhaustive set of "
             "investments, the worst case scenario is that investments that "
             "don't add anything aren't included in the portfolio. By having "
             "a non-overlapping set of investments, you can be sure that the "
             "portfolio is not double counting any investments and, "
             "since the optimizer is using the data provided, it won't be "
             "confused by investments that look similar and not know which "
             "to allocate to. For example, including global stocks, global "
             "bonds and commodities might be considered pretty exhaustive "
             "and non-overlapping. Including only US stocks, comparatively, "
             "would be less exhaustive, and if you included both US stocks as "
             "a whole and US large cap stocks, that would be overlapping.")
    st.write("Next, choose the metric/risk you would like to target. This is "
             "customizable since each investor might have a different goal "
             "and risk tolerance, which can depend on things like liquidity "
             "needs, general comfort with risk, time horizon, whether this "
             "represents your entire portfolio or just a portion, etc. You "
             "can either target the optimal Sharpe Ratio (returns/risk) or "
             "choose a risk level comparable to standard mixes of stocks and "
             "bonds (e.g. 60/40, 70/30, etc.).")
    st.write("Finally, choose the type of optimization method features you "
             "would like. We recommend bootstrapping as we believe it is "
             "more ideal for creating a stable portfolio through time, "
             "especially given uncertainty in future market returns. "
             "Descriptions of this method can be seen below.")

    # let the user choose their options
    investment_selection = st.sidebar.multiselect(
        "Which investments would you like to include?",
        gv.SECURITY_MAPPING.keys(), default=gv.DEFAULT_INVESTMENTS)
    objective_selection = st.sidebar.selectbox(
        "What would you like to optimize for?",
        gv.OBJECTIVE_CHOICES.keys())
    optimizer_option_selection = st.sidebar.multiselect(
        "Which optimization methods would you like to use?",
        gv.OPTIMIZER_CHOICES, default=gv.DEFAULT_OPTIMIZER_OPTIONS)

    ####################################################################
    # Pull Data
    ####################################################################

    # pull the data
    tables = data_engine.pull_ticker_tables()
    return_data = data_engine.pull_return_data(tables)

    # get data for the selected investments
    user_return_data, any_missing = data_engine.get_user_data(
        investment_selection, return_data)

    ####################################################################
    # Run Analysis
    ####################################################################

    # if we don't have missing data, we can just run the analysis
    if not any_missing:
        # run the optimization
        weights = analytics_engine.run_optimization(
            user_return_data, objective_selection, return_data)
        metrics = analytics_engine.portfolio_metrics(user_return_data, weights)
    else:
        # if we have missing data, we need to impute it and run the
        # analysis for each set of imputed data
        imp_data = data_engine.pmm(return_data, gv.DEFAULT_IMPUTE_COUNT)
        imp_weights = []
        imp_metrics = []
        for _ in range(gv.DEFAULT_IMPUTE_COUNT):
            user_return_data, _ = data_engine.get_user_data(
                investment_selection, next(imp_data))
            # run the optimization and record the weights and metrics
            curr_weights = analytics_engine.run_optimization(
                user_return_data, objective_selection, return_data)
            imp_weights.append(curr_weights)
            curr_metrics = analytics_engine.portfolio_metrics(
                user_return_data, curr_weights)
            imp_metrics.append([v[0] for v in curr_metrics.values()])
        # average the weights and metrics
        weights = pd.DataFrame(imp_weights).mean()
        avg_metrics = pd.DataFrame(imp_metrics).mean()
        metrics = analytics_engine.label_imp_metrics(avg_metrics)

    ####################################################################
    # Display Holdings
    ####################################################################

    st.write('')
    hld_title_cols = st.columns(3)
    with hld_title_cols[1]:
        hld_writing = "Recommended Holdings"
        hld_format = f'<p style="text-align: center; ' \
                     f'font-size: 26px; font-weight: bold;">' \
                     f'{hld_writing}</p>'
        st.markdown(hld_format, unsafe_allow_html=True)

    # create a table of the recommended holdings
    # use HTML / CSS styling to create a table
    st.markdown(gv.CSS_TABLE_STYLE, unsafe_allow_html=True)
    # create the table
    hdl_table_index_width = 50
    hld_table_title = 'Asset Classes'
    hld_table_headers = ['Weight (%)']
    hld_table_line_items = {a: [w] for a, w in zip(investment_selection,
                                                   weights)}
    hld_table_format_type = 'percent'
    hld_table_decimal_places = 0
    hld_table = format_engine.create_html_table(
        hdl_table_index_width, hld_table_title, hld_table_headers,
        hld_table_line_items, hld_table_format_type,
        decimals=hld_table_decimal_places)
    # display the table
    format_engine.display_table(hld_table, hld_table_headers, 10)

    ####################################################################
    # Display Metrics
    ####################################################################

    st.write('')
    metric_title_cols = st.columns(3)
    with metric_title_cols[1]:
        metric_writing = "Holdings Historical Metrics"
        metric_format = f'<p style="text-align: center; ' \
                        f'font-size: 26px; font-weight: bold;">' \
                        f'{metric_writing}</p>'
        st.markdown(metric_format, unsafe_allow_html=True)

    # create a table of the recommended holdings
    # use HTML / CSS styling to create a table
    st.markdown(gv.CSS_TABLE_STYLE, unsafe_allow_html=True)
    # create the table
    metric_table_index_width = 50
    metric_table_title = 'Metric'
    metric_table_headers = ['']
    metric_table_line_items = metrics
    metric_table_format_type = 'percent'
    metric_table_decimal_places = 1
    metric_table = format_engine.create_html_table(
        metric_table_index_width, metric_table_title, metric_table_headers,
        metric_table_line_items, metric_table_format_type,
        decimals=metric_table_decimal_places)
    # display the table
    format_engine.display_table(metric_table, metric_table_headers, 10)

    ##############################################################
    # ALLOW USER TO RUN BACKTEST, BOOTSTRAPPING



    ####################################################################
    # General Notes
    ####################################################################

    st.write('')
    st.write('---')

    st.markdown("#### General Notes")

    st.markdown("##### Investment Choices")
    # use HTML / CSS styling to create a table
    st.markdown(gv.CSS_TABLE_STYLE, unsafe_allow_html=True)
    # create the table
    inv_table_index_width = 25
    inv_table_title = 'Asset Classes'
    inv_table_headers = ['ETF Tickers', 'ETF Names', 'ETF Fees*']
    inv_table_line_items = gv.SECURITY_MAPPING
    inv_table_format_type = 'percent'
    inv_table_decimal_places = 1
    inv_table = format_engine.create_html_table(
        inv_table_index_width, inv_table_title, inv_table_headers,
        inv_table_line_items, inv_table_format_type,
        decimals=inv_table_decimal_places)
    st.markdown(inv_table, unsafe_allow_html=True)
    # add a note about the ETFs
    st.write('*Fees are based on fund websites as of 2022-09-30.')
    st.write("We currently include Bitcoin and Ethereum through ETFs since "
             "we wanted to stay consistent and include only ETFs. That being "
             "said, we would recommend investing directly into Bitcoin and "
             "Ethereum if possible, since the ETFs have management fees of "
             "0.95% and 2.50%, respectively, as of Sept. 30, 2022.")

    st.markdown("##### Optimization Methods")
    st.write('**Bootstrapping**')
    st.write("Bootstrapping is a method of using historical data, taking "
             "random sub-samples of that data and using each sub-sample to "
             "create an estimate of some metric.")
    st.write("Since the sub-samples are random and semi-uncorrelated, the "
             "estimates are also semi-uncorrelated. The metrics from each "
             "sub-sample are then averaged to create a single estimate, "
             "which better deals with uncertainty in the data and is not "
             "as impacted by outliers that would skew a metric taken from all "
             "the data.")
    st.write("In this case, we take subsamples of the historical returns for "
             "each investment. Those subsamples also maintain some semblance "
             "of the ordering of the original data to be more robust to "
             "maintaining the correlation of the data through time. Each "
             "subsample is then used to optimize a portfolio of the given "
             "investments and the weights from each subsample are averaged "
             "to create a single set of weights.")


if __name__ == '__main__':
    main()

