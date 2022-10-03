"""
Runs the portfolio optimizer.
"""

import PortfolioOptimizer as portopt

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
        title_format = f'<p style="text-align: center; font-family:Garamond; color:blue; ' \
                       f'font-size: 40px; font-weight: bold;">{title_writing}</p>'
        st.markdown(title_format, unsafe_allow_html=True)
        # and set up the sidebar too
        sidebar_title_format = f'<p style="text-align: center; font-family:Garamond; color:blue; ' \
                               f'font-size: 30px; font-weight: bold;">{title_writing}</p>'
        st.sidebar.markdown(sidebar_title_format, unsafe_allow_html=True)

    ####################################################################
    # User Options
    ####################################################################

    # define what the tool does for the user
    st.write("This tool will help you optimize your portfolio by finding the optimal weights "
             "based on the investments you have available and your desired risk.")
    st.write("First, choose those investments you would like to include. We suggest using "
             "a set of investments that are as exhaustive and non-overlapping as possible. "
             "By having an exhaustive set of investments, the worst case scenario is that "
             "investments that don't add anything aren't included in the portfolio. By having "
             "a non-overlapping set of investments, you can be sure that the portfolio is "
             "not double counting any investments and, since the optimizer is using the data "
             "provided, it won't be confused by investments that look similar and not know which "
             "to allocate to. For example, including global stocks, global bonds and commodities "
             "might be considered pretty exhaustive and non-overlapping. Including only US stocks, "
             "comparatively, would be less exhaustive, and if you included both US stocks as a "
             "whole and US large cap stocks, that would be overlapping.")
    st.write("Next, choose the metric/risk you would like to target. This is customizable "
             "since each investor might have a different goal and risk tolerance, which can "
             "depend on things like liquidity needs, general comfort with risk, time horizon, "
             "whether this represents your entire portfolio or just a portion, etc. You can either "
             "target the optimal Sharpe Ratio (returns/risk) or choose a risk level comparable "
             "to standard mixes of stocks and bonds (e.g. 60/40, 70/30, etc.).")
    st.write("Finally, choose the type of optimization method features you would like. We "
             "recommend bootstrapping as we believe it is more ideal for creating a stable "
             "portfolio through time, especially given uncertainty in future market returns. "
             "Descriptions of this method can be seen below.")

    # let the user choose their options
    investment_selection = st.sidebar.multiselect("Which investments would you like to include?",
                                                  portopt.GlobalVariables.SECURITY_MAPPING.keys(),
                                                  default=portopt.GlobalVariables.DEFAULT_INVESTMENTS)
    objective_selection = st.sidebar.selectbox("What would you like to optimize for?",
                                               portopt.GlobalVariables.OBJECTIVE_CHOICES,
                                               index=portopt.GlobalVariables.OBJECTIVE_CHOICES.index(
                                                   portopt.GlobalVariables.DEFAULT_OBJECTIVE))
    optimizer_option_selection = st.sidebar.multiselect("Which optimization methods would you like to use?",
                                                        portopt.GlobalVariables.OPTIMIZER_CHOICES,
                                                        default=portopt.GlobalVariables.DEFAULT_OPTIMIZER_OPTIONS)

    ####################################################################
    # Data Pull
    ####################################################################

    # pull the data
    api_key = portopt.Credentials.eodhd_api_key
    eodhd_engine = portopt.EodhdDataGathering(api_key)
    eodhd_data = eodhd_engine.get_data('MCD.US', '2019-01-01', '2020-01-01')
    st.write(eodhd_data)





    ####################################################################
    # General Notes
    ####################################################################

    st.markdown("#### General Notes")

    st.markdown("##### Investment Choices")
    # use HTML / CSS styling to create a table
    format_engine = portopt.FormatEngine()
    html_table_style = format_engine.create_html_table_style()
    st.markdown(html_table_style, unsafe_allow_html=True)
    # create the table
    inv_table_title = 'Asset Classes'
    inv_table_headers = ['ETF Tickers', 'ETF Names', 'ETF Fees']
    inv_table_line_items = portopt.GlobalVariables.SECURITY_MAPPING
    inv_table_indent = []
    inv_table_underline = []
    inv_table_format_type = 'percent'
    inv_table_decimal_places = 1
    inv_table = format_engine.create_html_table(
        inv_table_title, inv_table_headers, inv_table_line_items,
        inv_table_indent, inv_table_underline, inv_table_format_type,
        decimals=inv_table_decimal_places)
    st.markdown(inv_table, unsafe_allow_html=True)

    '''
    col1_inv_choices, col2_inv_choices, col3_inv_choices, col4_inv_choices, col5_inv_choices = \
        st.columns(5)
    with col2_inv_choices:
        st.markdown('**Asset Classes**')
        for investment in portopt.GlobalVariables.SECURITY_MAPPING.keys():
            st.write(investment)
    with col3_inv_choices:
        st.markdown('**ETF Tickers**')
        for etf in portopt.GlobalVariables.SECURITY_MAPPING.values():
            st.write(etf[0])
    with col4_inv_choices:
        st.markdown('**ETF Names**')
        for etf in portopt.GlobalVariables.SECURITY_MAPPING.values():
            st.write(etf[1])
    with col5_inv_choices:
        st.markdown('**ETF Fees***')
        for etf in portopt.GlobalVariables.SECURITY_MAPPING.values():
            st.write(etf[2])
    st.write('* Fees are based on fund websites as of 2022-09-30.')
    st.write("We currently include Bitcoin and Ethereum through ETFs since "
             "we wanted to stay consistent and include only ETFs. That being said, "
             "we would recommend investing directly into Bitcoin and Ethereum if possible, "
             "since the ETFs have management fees of 0.95% and 2.50%, respectively, "
             "as of Sept. 30, 2022.")
    '''

    st.markdown("##### Optimization Methods")
    st.write('Bootstrapping:')
    st.write('Bootstrapping is a method of using historical data, taking random sub-samples '
             'of that data and using each sub-sample to create an estimate of some metric. ')
    st.write('Since the sub-samples are random and semi-uncorrelated, the estimates are also '
             'semi-uncorrelated. The metrics from each sub-sample are then averaged to create a '
             'single estimate, which better deals with uncertainty in the data and is not '
             'as impacted by outliers that would skew a metric taken from all the data.')
    st.write('In this case, we take subsamples of the historical returns for each investment. '
             'Those subsamples also maintain some semblance of the ordering of the original data '
             'to be more robust to maintaining the correlation of the data through time. '
             'Each subsample is then used to optimize a portfolio of the given investments '
             'and the weights from each subsample are averaged to create a single set of weights.')


if __name__ == '__main__':
    main()

