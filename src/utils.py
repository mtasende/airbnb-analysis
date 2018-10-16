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


def show_data(data):
    print('The data has shape: {}\n'.format(data.shape))
    print('There is {} missing data!\n'.format(data.isnull().sum().sum()))
    print(data.head())


def common_values(series1, series2):
    """ Shows the differences, intersections and union of two sets. """
    values1 = set(series1)
    values2 = set(series2)
    intersection = set.intersection(values1, values2)
    no_values2 = values1 - values2
    no_values1 = values2 - values1
    total = set.union(values1, values2)

    print('Intersection: {}'.format(len(intersection)))
    print('Total set 1: {}'.format(len(values1)))
    print('Not in set 2: {}'.format(len(no_values2)))
    print('Total set 2: {}'.format(len(values2)))
    print('Not in set 1: {}'.format(len(no_values1)))
    print('Total: {}'.format(len(total)))
