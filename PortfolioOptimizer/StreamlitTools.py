"""
Tools to help with the web apps.

Classes:
    StreamlitTools: Creates visuals for the web apps.
"""

import streamlit as st


class StreamlitTools(object):
    """
    Tools to help with the web apps.

    Methods:

    """

    def __init__(self):
        """
        Args:
        """

    def create_html_table_style(self):
        """
        Creates a string to be used to style a financial statement with
        CSS. This is what is used in the <style> ... </style> section
        of html/css.

        Args:
            N/A

        Returns:
            financial_statement_style(string): The string with the
                styling.
        """

        financial_statement_style = '''
            <style>
                td:hover {
                    background-color: palegreen;
                }
                tr:hover {
                    background-color: aliceblue;
                }
                table, th, tr, td
                {
                    border: 0;
                }
                tr.border_bottom td {
                    border-bottom: 1px solid black;
                }
            </style>
            '''

        # for no borders
        '''
            table, th, tr, td
            {
                border: 0 !important;
            }
        '''

        return financial_statement_style

    def format_int(self, numbers):
        """
        Formats numbers from int/float type to string with commas, no
        zeros and '-' instead of '0'. Will ignore strings.

        Args:
            numbers(int/float list): A list of the numbers to format.

        Returns:
            formatted_numbers: The same numbers formatted.
        """

        formatted_numbers = []

        for curr_num in numbers:
            if not (isinstance(curr_num, str)):
                # set to int
                if isinstance(curr_num, float):
                    curr_num = int(round(curr_num, 0))
                    # set to number type with commas and no decimal
                    curr_num = "{:,d}".format(curr_num)
                # make string
                curr_num = str(curr_num)
            # turn 0 or Null into -
            if curr_num == '0' or curr_num == "None":
                curr_num = '-'

            formatted_numbers.append(curr_num)

        # deal with a single value or none
        if len(formatted_numbers) == 1:
            formatted_numbers = formatted_numbers[0]
        if len(formatted_numbers) == 0:
            formatted_numbers = ""

        return formatted_numbers

    def format_float(self, numbers, decimals):
        """
        Formats numbers from int/float type to string with decmials
        commas, no zeros and '-' instead of '0'. Will ignore strings.

        Args:
            numbers(int/float list): A list of the numbers to format.
            decimals(int): The number of decimals to use.

        Returns:
            formatted_numbers: The same numbers formatted.
        """

        formatted_numbers = []

        for curr_num in numbers:
            if not (isinstance(curr_num, str)):
                # set to float
                if isinstance(curr_num, float):
                    # set to number type with commas and decimals
                    curr_num = '{:,.{decimals}f}'.format(curr_num,
                                                         decimals=decimals)
                # make string
                curr_num = str(curr_num)
            # turn 0 or Null into -
            if curr_num == '0.0' or curr_num == "None":
                curr_num = '-'

            formatted_numbers.append(curr_num)

        # deal with a single value or none
        if len(formatted_numbers) == 1:
            formatted_numbers = formatted_numbers[0]
        if len(formatted_numbers) == 0:
            formatted_numbers = ""

        return formatted_numbers

    def format_percentages(self, numbers, decimals):
        """
        Formats numbers from int/float type to percentages, no
        zeros and '-' instead of '0'. Will ignore strings.

        Args:
            numbers(int/float list): A list of the numbers to format.
            decimals(int): The number of decimals to use.

        Returns:
            formatted_numbers: The same numbers formatted.
        """

        formatted_numbers = []

        for curr_num in numbers:
            if not (isinstance(curr_num, str)):
                # set to percentage type with decimals
                curr_num = '{0:.{decimals}%}'.format(curr_num,
                                                     decimals=decimals)
                # make string
                curr_num = str(curr_num)[:-1]
            # turn 0 or Null into -
            if curr_num == '0.0':
                curr_num = '-'

            formatted_numbers.append(curr_num)

        return formatted_numbers

    def create_html_table(self, title, col_headers, line_items, indent_items,
                          underline_items, format_type, blank_after=[],
                          **kwargs):
        """
        Creates a string to be used to create a
        table with HTML. This is what is used in the <table> ...
        </table> section of html.

        Args:
            title(string): The title of the table.
            col_headers(string list): A set of the headers for the data
                columns.
            line_items(string dict): The line items with the key as the
                 line item name and the value as a list with values for
                 each column (values can be number or string types).
            indent_items(string list): List of keys from the line_items
                dict that should be indented.
            underline_items(string list): List of keys for which the
                associated values should be underlined.
            format_type(string): How to format the line item values.
                Currently supports 'int', 'float' and 'percent'.
            blank_after(int): The items after which a blank line will
                be inserted.
            **kwargs: Arbitrary keyword arguments for format types.

        Returns:
            html_table(string): The string with the HTML table.
        """

        # determine the width of the table
        table_width = len(col_headers)
        # we set the line items to be 25% of the table width and the
        # rest of the columns to be equally spaced
        col_width = str(75 / table_width)

        # create the beginning of the string
        html_table = f'''
            <table width="100%">
                <colgroup>
                    <col width="25%">
                    <col span="{table_width}" width="{col_width}%">
                </colgroup>
                <tr>
                    <th>{title}</th>'''

        # add the column headers
        for curr_header in col_headers:
            html_table += f'<th align="right"><b>{curr_header}</b></th>'

        # close the header row
        html_table += "</tr>"

        # add each line item with data
        for key, values in line_items.items():
            # indent if necessary
            if key in indent_items:
                formatted_key = "&emsp;" + key
            else:
                formatted_key = key
            # add the line item first
            if key in underline_items:
                html_table += f'<tr class="border_bottom"><th>' \
                              f'{formatted_key}</th>'
            else:
                html_table += f'<tr><th>{formatted_key}</th>'
            # create the values in the correct format
            if format_type == 'int':
                formatted_values = self.format_int(values)
            elif format_type == 'float':
                formatted_values = self.format_float(values, **kwargs)
            else:
                formatted_values = self.format_percentages(values,
                                                           **kwargs)
            for curr_value in formatted_values:
                html_table += f'<td align="right">{curr_value}</td>'
            # close the line
            html_table += "</tr>"
            # add a blank row if necessary
            if key in blank_after:
                html_table += "<tr><th></th>"
                for _ in range(len(col_headers)):
                    html_table += "<td></td>"
                html_table += "</tr>"

        # finish the table
        html_table += "</table>"

        return html_table
