"""
Runs the portfolio optimizer.
"""

import PortfolioOptimizer as portopt

import streamlit as st


def main():
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
    st.write("Next, choose the metric/risk you would like to target. This is not given for you "
             "since each investor might have a different goal and risk tolerance, which can "
             "depend on things like liquidity needs, general comfort with risk, time horizon, "
             "whether this represents your entire portfolio or just a portion, etc. You can either "
             "target the optimal Sharpe Ratio (returns/risk) or choose a risk level comparable "
             "to standard mixes of stocks and bonds (e.g. 60/40, 70/30, etc.).")
    st.write("Finally, choose the type of optimization you would like. We recommend using both "
             "bootstrapping and PCA as we believe those are more ideal for creating a stable "
             "portfolio through time, especially given uncertainty in future market returns. "
             "Descriptions of these methods can be seen below.")

    # let the user choose their options
    investment_selection = st.sidebar.multiselect("Which investments would you like to include?",
                                                  portopt.GlobalVariables.INVESTMENT_CHOICES,
                                                  default=portopt.GlobalVariables.DEFAULT_INVESTMENTS)
    objective_selection = st.sidebar.radio("What would you like to optimize for?",
                                           portopt.GlobalVariables.OBJECTIVE_CHOICES,
                                           index=portopt.GlobalVariables.OBJECTIVE_CHOICES.index(portopt.GlobalVariables.DEFAULT_OBJECTIVE)
    optimizer_option_selection = st.sidebar.multiselect("Which optimization methods would you like to use?",
                                                        portopt.GlobalVariables.OPTIMIZER_CHOICES,
                                                        default=portopt.GlobalVariables.DEFAULT_OPTIMIZER_OPTIONS)

if __name__ == '__main__':
    main()

