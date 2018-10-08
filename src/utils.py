""" General utility functions. """

from functools import update_wrapper
import pandas as pd


def decorator(d):
    """
    Make function d a decorator: d wraps a function fn.
    (Thanks to "Desing of Computer Programs" by Peter Norvig)
    """

    def _d(fn):
        return update_wrapper(d(fn), fn)

    update_wrapper(_d, d)
    return _d


@decorator
def pandify(scalar_fun):
    """
    The decorated function applies the scalar function to all values
    and accepts Series and DataFrames.
    Args:
        scalar_fun(function): a scalar function
    Returns:
        df_fun(function): a matrix/vector function for pandas DFs and Series
    """

    def df_fun(df):
        if isinstance(df, pd.Series):
            return df.apply(scalar_fun)
        elif isinstance(df, pd.DataFrame):
            return df.apply(lambda x: x.apply(scalar_fun))
        else:
            return None

    return df_fun