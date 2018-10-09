""" A collection of functions to preprocess the data. """

import numpy as np
import pandas as pd
from datetime import datetime
import os
from src.data import DATA_RAW, SEATTLE_CALENDAR_TEMP, SEATTLE_LISTINGS_TEMP,\
    SEATTLE_REVIEWS_TEMP
from src.utils import pandify

DOLLAR_SIGN = '\$'


def transform_all(calendar, listings, reviews, save_results=False):
    """ Transforms all the columns. """
    calendar, listings, reviews = transform_prices(calendar, listings, reviews)
    calendar, listings, reviews = transform_booleans(calendar, listings,
                                                     reviews)
    calendar, listings, reviews = transform_dates(calendar, listings,
                                                  reviews)
    calendar, listings, reviews = transform_percent(calendar, listings,
                                                    reviews)

    if save_results:
        save_data(calendar, listings, reviews)

    return calendar, listings, reviews


def transform_prices(calendar, listings, reviews):
    """ Transforms all the prices in '$x' format to float. """
    calendar.price = price_to_float(calendar.price)

    # Find features that have dollar signs in all non-null entries
    obj_listings = listings.select_dtypes(include='object')
    has_dsign = find_str(obj_listings)
    all_dsign = obj_listings[obj_listings.columns[has_dsign.all()]]
    price_cols = all_dsign.columns.tolist()

    listings[price_cols] = price_to_float(listings[price_cols])

    return calendar, listings, reviews


def transform_booleans(calendar, listings, reviews):
    """ Transforms all the 'boolean string' values (t/f) to booleans. """
    # Calendar
    calendar.available = string2bool(calendar.available)

    # Listings
    tf_any = is_tf(listings).sum() > 0
    positive_tfs = is_tf(listings).mean()[tf_any]
    tf_cols = positive_tfs.index.tolist()
    listings[tf_cols] = string2bool(listings[tf_cols])

    return calendar, listings, reviews


def transform_dates(calendar, listings, reviews):
    """ Transforms all the 'date strings' to date format. """
    # Calendar
    calendar.date = string2date(calendar.date)

    # Listings
    is_date = listings.iloc[0].str.contains('\d{4}-\d{2}-\d{2}').fillna(False)
    date_cols = listings.columns[is_date].tolist()
    listings[date_cols] = string2date(listings[date_cols])

    # Reviews
    reviews.date = string2date(reviews.date)

    return calendar, listings, reviews


def transform_percent(calendar, listings, reviews):
    """ Transforms all the 'percent strings' to floats. """
    percent_cols = ['host_response_rate', 'host_acceptance_rate']
    listings[percent_cols] = percent2num(listings[percent_cols])

    return calendar, listings, reviews


def load_data(raw_dir=DATA_RAW, city='seattle'):
    """ Loads the raw data. """
    calendar = pd.read_csv(os.path.join(raw_dir, city, 'calendar.csv'))
    listings = pd.read_csv(os.path.join(raw_dir, city, 'listings.csv'))
    reviews = pd.read_csv(os.path.join(raw_dir, city, 'reviews.csv'))

    return calendar, listings, reviews


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


def get_column_by_kind(listing_cols_df, kind):
    return listing_cols_df.index[
        listing_cols_df.kind == kind].tolist()


@pandify
def percent2num(text):
    """ Convert 'percent strings' to floats. """
    if text is np.nan:
        return np.nan
    return float(text[:-1])


def save_data(calendar, listings, reviews):
    """ Save the usual variables to pickles in the interim folder. """
    calendar.to_pickle(SEATTLE_CALENDAR_TEMP)
    listings.to_pickle(SEATTLE_LISTINGS_TEMP)
    reviews.to_pickle(SEATTLE_REVIEWS_TEMP)
