"""
Tools to help with the web apps.

Classes:
    StreamlitTools: Creates visuals for the web apps.
"""

import numpy as np
import streamlit as st

from typing import Any, Literal, Union


class StreamlitTools(object):
    """
    Tools to help with the web apps.

    Methods:

    """

    def __init__(self):
        """
        Args:
        """
        pass

    def _check_expand_input(self, input_val: Union[list, str, bool, None],
                            desired_len: int, input_type: str,
                            type_constraint: Any) -> list:
        """
        Checks if the input is a list and, if not, makes it into
            a list of the correct length. If it is a list, checks that
            it is the correct length and values.
        :param input_val: The value we want to make into a list of the
            correct length.
        :param desired_len: The length of the list that we want.
        :param input_type: The type of input, which we use to display any
            errors, such as 'format_type' or 'decimals'.
        :param type_constraint: The type that we want the input to be. We
            use this to let the user know of any errors.
        :return output: The list of correct length/allowable values.
        """
        # we need to deal with np.int64 since that can cause issues as it
        # doesn't match to int
        if isinstance(input_val, list) and isinstance(input_val[0], np.int64):
            input_val = [int(x) for x in input_val]
        # check that the type matches
        if isinstance(type_constraint, list):
            if isinstance(input_val, list):
                type_match = all(type(x) in type_constraint for x in input_val)
            else:
                type_match = type(input_val) in type_constraint
        else:
            if isinstance(input_val, list):
                type_match = all(isinstance(x, type_constraint) for x in
                                 input_val)
            else:
                type_match = isinstance(input_val, type_constraint)

        # if it's just a single value, make it a list
        if (not isinstance(input_val, list) and type_match) or \
                input_val is None:
            output = [input_val] * desired_len
        # if it's a list, check that it's the right length
        elif len(input_val) != desired_len:
            log_str = (f"*******************Error*******************\n"
                       f"{input_type} must either be a single value, applied "
                       "to all rows, or a list of length equal to the number "
                       "of rows.")
            st.write(log_str)
        # if it's a list, check that it's the right values
        elif not type_match:
            log_str = (f"*******************Error*******************\n"
                       f"Only {type_constraint} is supported for "
                       f"{input_type}.")
            st.write(log_str)
        else:
            output = input_val

        return output

    def format_numbers(self, format_type: Literal['percent', 'float', ''],
                       numbers: list, decimals: int = 1,
                       highlights: Union[list, None] = None,
                       neg_red: bool = True) -> list:
        """
        Formats numbers from int/float type to percentages. Will ignore
            strings.
        :param format_type: The type of formatting to do.
        :param numbers: The numbers to format.
        :param decimals: The number of decimals to include.
        :param highlights: The numbers to highlight in yellow (as 0 or 1).
        :param neg_red: Whether to color negative numbers red.
        :return formatted_numbers: The same numbers formatted.
        """

        if format_type == 'percent':
            handle = '%'
        elif format_type == 'float':
            handle = 'f'
        elif format_type != '':
            log_str = ("*******************Error*******************\n"
                       "Only 'percent', 'float' and '' are supported for "
                       "format_type ('' should only be used when this "
                       "function will be accessed with a string or some "
                       "other variable that will not actually be formatted.")
            st.write(log_str)

        formatted_numbers = []

        for i, curr_num in enumerate(numbers):
            # if a string was passed, we keep it the same, otherwise we
            # format it as a number
            if not (isinstance(curr_num, str)):
                # set to percentage type with decimals
                formatted_curr_num = f"{curr_num:.{decimals}{handle}}"
                # make string
                formatted_curr_num = str(formatted_curr_num)
            else:
                formatted_curr_num = curr_num

            # add color if negative
            neg_check = (isinstance(curr_num, (int, float)) and curr_num < 0
                         and neg_red)
            if neg_check:
                html_style = 'color: red;'
            # add color if highlight
            highlight_check = highlights is not None and highlights[i]
            if highlight_check:
                if neg_check:
                    html_style += 'background-color: gold;'
                else:
                    html_style = 'background-color: gold;'
            # add any html style
            if neg_check or highlight_check:
                formatted_curr_num = f'<span style="{html_style}">' \
                                     f'{formatted_curr_num}</span>'

            formatted_numbers.append(formatted_curr_num)

        return formatted_numbers

    def _format_number_list(self,
                            format_type: Union[Literal['percent', 'float'],
                                               list],
                            numbers: list,
                            decimals: Union[int, list] = 1,
                            highlights: Union[int, list, None] = None,
                            neg_red: [bool, list] = True) -> list:
        """
        This allows for formatting of numbers with different formatting
            types, decimals, highlights, and/or neg_reds. This should only
            be used instead of format_numbers if you want to format each
            value differently in some way.
        :param format_type: The type of formatting to do.
        :param numbers: The numbers to format.
        :param decimals: The number of decimals to include.
        :param highlights: The numbers to highlight in yellow (as 0 or 1).
        :param neg_red: Whether to color negative numbers red.
        :return formatted_numbers: The same numbers formatted.
        """
        # expand format_type, decimals, highlights, and neg_red to equal
        # the length of numbers
        format_type = self._check_expand_input(
            format_type, len(numbers), 'format_type', str)
        decimals = self._check_expand_input(
            decimals, len(numbers), 'decimals', int)
        highlights = self._check_expand_input(
            highlights, len(numbers), 'highlights', [int, None])
        neg_red = self._check_expand_input(
            neg_red, len(numbers), 'neg_red', bool)

        formatted_numbers = []
        for i in range(len(numbers)):
            formatted_numbers.append(self.format_numbers(
                format_type[i], [numbers[i]], decimals[i], [highlights[i]],
                neg_red[i])[0])

        return formatted_numbers

    def create_html_table(self, index_width: int, title: str,
                          col_headers: list, row_items: dict,
                          format_type: Union[list, str],
                          indent_items: list = [], underline_items: list = [],
                          blank_after: list = [], neg_red: bool = True,
                          **kwargs) -> str:
        """
        Creates a string to be used to create a table with HTML. This is
            what is used in the <table> ... </table> section of html.
        :param index_width: The width of the index column out of 100.
        :param title: The title of the table to be displayed in the top
            left corner.
        :param col_headers: A list of the headers for the columns.
        :param row_items: The row items with the key as the
             row name - displayed in the left-most column -
             and the value as a list with values for each
             column (values can be number or string types).
        :param format_type: The format to use for the numbers in the
            table. Can either be one string and we apply that same
            type to all rows or a list that corresponds to each row.
            Currently only supports 'percent' and 'float'.
        :param indent_items: List of keys from the row_items dict that
            should be indented.
        :param underline_items: List of keys for which the associated
            values should be underlined.
        :param blank_after: The items after which a blank line will
            be inserted.
        :param neg_red: Whether to color negative numbers red.
        :param kwargs: The keyword arguments to be used for the
            format_type. Currently supports:
            1. 'decimals' - which should either be one integer, for all
            rows, or a list corresponding to each row
            2. 'highlights' - which should be a dictionary
            corresponding to the row_items dict based on key, with the
            values as indicators (0 or 1) for which values to highlight
            (such as {'Jan': [0, 0, 1], 'Feb': [1, 0, 0], ...} for a table
            with months as rows and three columns)
            3. 'align' - which should be list corresponding to each column
            with the alignment of the column ('left', 'center', or
            'right')
        :return html_table: The string with the HTML table.
        """
        # check and create format_type
        format_type = self._check_expand_input(
            format_type, len(row_items), 'format_type', [str, list])
        # determine the number of decimals per row
        if 'decimals' in kwargs:
            decimals = self._check_expand_input(
                kwargs['decimals'], len(row_items), 'decimals', [int, list])
        else:
            decimals = [1] * len(row_items)
        if 'align' in kwargs:
            align = self._check_expand_input(
                kwargs['align'], len(col_headers), 'align', str)
        else:
            align = ['right'] * len(col_headers)

        # we set the non-index columns to be equally spaced
        col_count = len(col_headers)
        col_width = str((100 - index_width) / col_count)

        # create the beginning of the string with column widths and the
        # title
        html_table = f'''
            <table width="100%">
                <colgroup>
                    <col width="{str(index_width)}%">
                    <col span="{col_count}" width="{col_width}%">
                </colgroup>
                <tr>
                    <th>{title}</th>'''

        # add the column headers
        for i, curr_header in enumerate(col_headers):
            html_table += f'<th align="{align[i]}"><b>{curr_header}</b></th>'
        # close the header row
        html_table += "</tr>"

        # add each row item with data
        for i, (key, values) in enumerate(row_items.items()):
            # indent if necessary
            if key in indent_items:
                formatted_key = "&emsp;" + key
            else:
                formatted_key = key
            # add the row item first and underline if necessary
            if key in underline_items:
                html_table += f'<tr class="border_bottom" ' \
                              f'style="white-space:nowrap"><th>' \
                              f'{formatted_key}</th>'
            else:
                html_table += f'<tr style="white-space:nowrap">'\
                              f'<th>{formatted_key}</th>'
            # determine if we want to highlight
            if 'highlights' in kwargs and key in kwargs['highlights']:
                highlights = kwargs['highlights'][key]
            else:
                highlights = None
            # create the values in the correct format, allowing for
            # different formats for different values
            if isinstance(format_type[i], list) or \
                    isinstance(decimals[i], list) or \
                    isinstance(highlights, list):
                formatted_values = self._format_number_list(
                    format_type[i], values, decimals[i], highlights, neg_red)
            # this is the case of just one type of formatting for an
            # entire row
            else:
                formatted_values = self.format_numbers(
                    format_type[i], values, decimals[i], highlights, neg_red)
            # add the values and align right
            for j, curr_value in enumerate(formatted_values):
                html_table += f'<td align="{align[j]}">{curr_value}</td>'
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

    def display_table(self, table: str, col_headers: list,
                      cols_for_center: int) -> Union[None, list]:
        """
        Displays the table in the app.
        :param table: The HTML table as a string.
        :param col_headers: The column headers for the table, which we
            need as a way to determine the length of the table.
        :param cols_for_center: If we have less than this number of
            columns, we center the table on the page, otherwise we use the
            full width of the page.
        :return col_list: The list of the column widths, so we can use it
            for other displays if necessary.
        """
        # determine the width of the table, we want it to be 100% of the
        # width of the page if the number of years is at least 19, but
        # smaller if not (we choose 19 since we also have the month names to
        # get 20 total and make the math easier)
        # we also use 98 as the highest number since we need to have at least
        # 1 for each margin
        if len(col_headers) >= cols_for_center:
            st.markdown(table, unsafe_allow_html=True)
        else:
            table_width = 100 - (cols_for_center - len(col_headers)) * (100 / (
                    cols_for_center + 1))
            margin_width = int(100 - table_width) / 2
            col_widths = [margin_width, table_width, margin_width]

            # display the table
            table_col1, table_col2, table_col3 = st.columns(col_widths)
            with table_col2:
                st.markdown(table, unsafe_allow_html=True)

            return col_widths


    def get_metric_headers(self, obj_func: str) -> list:
        """Gets the headers for the metrics table depending on whether we
            have a benchmark or not."""
        if obj_func == 'max_return':
            headers = ['Portfolio', 'Benchmark']
        else:
            headers = ['Portfolio']

        return headers
