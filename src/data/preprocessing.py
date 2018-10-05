""" A collection of functions to preprocess the data. """

from functools import update_wrapper
import numpy as np
import pandas as pd
from datetime import datetime

DOLLAR_SIGN = '\$'


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


@pandify
def price_to_float(price_str):
    """ Converts a price like $67.0 to a float (67.0)"""
    if price_str is np.nan:
        return np.nan
    return float(price_str[1:].replace(',', ''))


def find_str(df, string=DOLLAR_SIGN):
    """
    Finds substrings in a dataframe.
    By default it searches for the dollar sign.
    """
    return df.apply(lambda x: x.str.contains(string), axis=1)


@pandify
def string2bool(text):
    """ Convert 'boolean strings' to booleans."""
    if (text == 't') or (text == 'True'):
        return True
    elif (text == 'f') or (text == 'False'):
        return False
    else:
        return np.nan


def is_tf(df):
    """ Which values are a 'boolean string'? """
    return (df == 't') | (df == 'f') | (df == 'True') | (df == 'False')


@pandify
def string2date(text):
    """ Convert 'date strings' to dates. """
    if text is np.nan:
        return np.nan
    return datetime.strptime(text, '%Y-%m-%d')
