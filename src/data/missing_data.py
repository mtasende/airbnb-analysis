""" Functions to help filling the missing data. """
import pandas as pd
from src.data import preprocessing as pp
from src.data import SEATTLE_LISTINGS_COLS, SEATTLE_CALENDAR_TEMP, \
    SEATTLE_LISTINGS_TEMP, SEATTLE_REVIEWS_TEMP


def fill_missing(calendar, listings, reviews, save_results=False):
    """
    Fills all the missing data that is filledbefore the feature generation.
    There may be some missing data that is filled after the feature generation.
    """
    calendar = fill_calendar_na(calendar, listings)
    reviews = fill_reviews_na(reviews)
    listings = fill_listings_na(listings)

    if save_results:
        pp.save_data(calendar, listings, reviews)

    return calendar, listings, reviews


def fill_listings_na(listings, save_listings_cols=True):
    """ A specific function to fill the listings missing values."""
    listings_cols_df = pd.read_pickle(SEATTLE_LISTINGS_COLS)
    listings, listings_cols_df = fill_num_cols(listings, listings_cols_df)
    listings, listings_cols_df = fill_price_cols(listings, listings_cols_df)
    listings, listings_cols_df = fill_tf_cols(listings, listings_cols_df)
    listings, listings_cols_df = fill_free_text_cols(listings,
                                                     listings_cols_df)
    listings, listings_cols_df = fill_url_cols(listings, listings_cols_df)
    listings, listings_cols_df = fill_location_cols(listings, listings_cols_df)
    listings, listings_cols_df = fill_date_cols(listings, listings_cols_df)
    listings, listings_cols_df = fill_percent_cols(listings, listings_cols_df)
    listings, listings_cols_df = fill_time_cols(listings, listings_cols_df)
    listings, listings_cols_df = fill_cat_cols(listings, listings_cols_df)

    if save_listings_cols:
        listings_cols_df.to_pickle(SEATTLE_LISTINGS_COLS)

    return listings


def fill_reviews_na(reviews):
    """ A specific function to fill the reviews missing values."""
    return reviews.dropna()


def fill_calendar_na(calendar, listings):
    """
    A specific function to fill the calendar missing values.

    Args:
        calendar (pandas.DataFrame): Contains prices and availabilities in
            time for the listings.
        listings (pandas.DataFrame): Contains the static features of each
            listing.
    Returns:
        pandas.DataFrame: The filled calendar.
    """
    new_cal = calendar.copy()
    new_cal = fill_df_in_time(new_cal)
    return fill_with_listings(new_cal, listings)


def fill_in_time(ts):
    """ Fills a time series by forward filling and then backfilling"""
    return ts.fillna(method='ffill').fillna(method='bfill')


def get_ts(df, values_col='price'):
    """
    Extracts one time series per listing.
    Args:
        df(pd.DataFrame): a dataframe with listing_id, date, and a value that
        changes in time (price, as default).
        values_col(str): the column to take as dependent variable.
    Returns:
        pd.DataFrame: A time series, indexed in dates, has one column per
        listing.
    """
    return pd.pivot_table(data=df,
                          index='date',
                          columns='listing_id',
                          values=values_col)


def fill_df_in_time(df, idx_col='listing_id', value_col='price'):
    """
    Fills an entire dataframe in time, by forward filling and then backfilling.
    It first groups the dataframe by idx_col.
    The df must have a 'date' column with timestamps.
    Args:
        df (pandas.DataFrame): The dataframe to fill
        idx_col (str): A column name to group by.
        value_col (str): The name of the column that has the values to fill.
    """
    tmp_df = df.copy()
    ts = get_ts(tmp_df, values_col=value_col)
    ts = ts.apply(fill_in_time)
    tmp_df = tmp_df.set_index([idx_col, 'date'])
    tmp_df.price = tmp_df.price.fillna(ts.unstack())
    return tmp_df.reset_index()


def fill_with_listings(calendar, listings):
    """
    Fills the missing prices in the calendar dataframe,
    with the prices available in the listings dataframe.

    Args:
        calendar (pandas.DataFrame): Contains prices and availabilities in
            time for the listings.
        listings (pandas.DataFrame): Contains the static features of each
            listing.
    Returns:
        pandas.DataFrame: The filled calendar.
    """
    listings_price = listings[['id', 'price']].rename(columns={
        'id': 'listing_id'}).set_index('listing_id').price

    new_cal = calendar.copy()
    new_cal = new_cal.set_index('listing_id')
    new_cal.price = new_cal.price.fillna(listings_price)

    return new_cal.reset_index()


def create_is_missing(df, cols):
    """
    Creates a new column with 1 in the places where the 'cols' have missing
    values.

    Args:
        df (pandas.DataFrame): Any dataframe with missing data.
        cols (list(str)): The names of the columns to use.
    Returns:
        pandas.DataFrame: The same as df but with the added columns.
    """
    missing_df = df[cols].isnull().astype(int).rename(columns={
        c: c + '_missing' for c in cols})
    return df.join(missing_df)


def fill_num_cols(listings, listings_cols_df):
    """
    Fills the missing data in the numeric features of the listings dataframe.

    Args:
        listings (pandas.DataFrame): Contains the static features of each
            listing.
        num_cols (list(str)): The list of numeric column names to fill.
    Returns:
        pandas.DataFrame: The filled 'listings' dataframe.
        pandas.DataFrame: A dataframe with the 'kind' of
            columns that each column is.
    """
    num_cols = pp.get_column_by_kind(listings_cols_df, 'num_cols')
    num_listings = listings[num_cols]
    has_missing = num_listings.columns[
        num_listings.isnull().sum() > 0].tolist()
    drop = [
        'license',
        'square_feet'
    ]
    most_frequent = [
        'bathrooms',
        'bedrooms',
        'beds',
        'host_listings_count',
        'host_total_listings_count'
    ]
    # Others: mean
    mean = list(
        set(listings[has_missing].columns) - set(drop) - set(most_frequent))

    # Create the "is_missing" feature for features with medium missing data
    feat_cols = num_listings.columns[
        (num_listings.isnull().mean() > 0.1) &
        (num_listings.isnull().mean() < 0.9)].tolist()
    listings = create_is_missing(listings, feat_cols)

    # Drop the features that have too little data
    drop = list(set(listings.columns).intersection(set(drop)))
    listings = listings.drop(drop, axis=1)
    drop = list(set(listings_cols_df.index).intersection(set(drop)))
    listings_cols_df = listings_cols_df.drop(drop)

    # Fill with the most frequent or the mean
    listings[most_frequent] = listings[most_frequent].fillna(
        listings[most_frequent].median())
    listings[mean] = listings[mean].fillna(listings[mean].mean())

    return listings, listings_cols_df


def fill_price_cols(listings, listings_cols_df):
    """
    Fill the missing data in the listings dataframe, for the 'price' columns.

    Args:
        listings (pandas.DataFrame): Contains the static features of each
            listing.
        listings_cols_df (pandas.DataFrame): A dataframe with the 'kind' of
            columns that each column is.
    Returns:
        The same arguments, with listings filled.
    """
    # Fill the long-term prices with the daily price
    week_factor = (listings.weekly_price / listings.price).mean()
    listings.weekly_price = listings.weekly_price.fillna(
        listings.price * week_factor)

    month_factor = (listings.monthly_price / listings.price).mean()
    listings.monthly_price = listings.monthly_price.fillna(
        listings.price * month_factor)

    # Fill the cleaning fee proportionally to the price
    cleaning_coef = (listings.cleaning_fee / listings.price).mean()
    listings.cleaning_fee = listings.cleaning_fee.fillna(
        cleaning_coef * listings.price)

    # Fill the security deposit with the mean
    listings.security_deposit = listings.security_deposit.fillna(
        listings.security_deposit.mean())

    return listings, listings_cols_df


def fill_tf_cols(listings, listings_cols_df):
    """
    Fill the missing data for the 'tf' columns.

    Args:
        listings (pandas.DataFrame): Contains the static features of each
            listing.
        listings_cols_df (pandas.DataFrame): A dataframe with the 'kind' of
            columns that each column is.
    Returns:
        The same arguments, with listings filled.
    """
    tf_cols = pp.get_column_by_kind(listings_cols_df, 'tf_cols')
    listings[tf_cols] = listings[tf_cols].fillna(listings[tf_cols].median())

    return listings, listings_cols_df


def fill_free_text_cols(listings, listings_cols_df):
    """
    Fill the missing data for the 'free text' columns.

    Args:
        listings (pandas.DataFrame): Contains the static features of each
            listing.
        listings_cols_df (pandas.DataFrame): A dataframe with the 'kind' of
            columns that each column is.
    Returns:
        The same arguments, with listings filled.
    """
    free_text_cols = pp.get_column_by_kind(listings_cols_df, 'free_text_cols')
    listings[free_text_cols] = listings[free_text_cols].fillna('')
    return listings, listings_cols_df


def fill_url_cols(listings, listings_cols_df):
    """
    Fill the missing data for the 'url' columns.

    Args:
        listings (pandas.DataFrame): Contains the static features of each
            listing.
        listings_cols_df (pandas.DataFrame): A dataframe with the 'kind' of
            columns that each column is.
    Returns:
        The same arguments, with listings filled.
    """
    url_cols = pp.get_column_by_kind(listings_cols_df, 'url_cols')
    listings[url_cols] = listings[url_cols].fillna('')
    return listings, listings_cols_df


def fill_location_cols(listings, listings_cols_df):
    """
    Fill the missing data for the 'location' columns.

    Args:
        listings (pandas.DataFrame): Contains the static features of each
            listing.
        listings_cols_df (pandas.DataFrame): A dataframe with the 'kind' of
            columns that each column is.
    Returns:
        The same arguments, with listings filled.
    """
    listings.neighbourhood = listings.neighbourhood.fillna(
        listings.neighbourhood_cleansed)
    listings.host_neighbourhood = listings.host_neighbourhood.fillna(
        listings.neighbourhood)
    listings.host_location = listings.host_location.fillna(
        listings.host_location.value_counts().index[0])
    listings.zipcode = listings.zipcode.fillna('')

    # Fix a mistake
    listings.loc[listings.zipcode == '99\n98122', 'zipcode'] = '98122'

    return listings, listings_cols_df


def fill_date_cols(listings, listings_cols_df):
    """
    Fill the missing data for the 'date' columns.

    Args:
        listings (pandas.DataFrame): Contains the static features of each
            listing.
        listings_cols_df (pandas.DataFrame): A dataframe with the 'kind' of
            columns that each column is.
    Returns:
        The same arguments, with listings filled.
    """
    listings[['first_review', 'last_review']] = listings[
        ['first_review', 'last_review']].fillna(listings.last_scraped.max())
    listings = listings[~listings.host_since.isnull()]
    return listings, listings_cols_df


def fill_percent_cols(listings, listings_cols_df):
    """
    Fill the missing data for the 'percent' columns.

    Args:
        listings (pandas.DataFrame): Contains the static features of each
            listing.
        listings_cols_df (pandas.DataFrame): A dataframe with the 'kind' of
            columns that each column is.
    Returns:
        The same arguments, with listings filled.
    """
    percent_cols = pp.get_column_by_kind(listings_cols_df, 'percent_cols')
    listings[percent_cols] = listings[percent_cols].fillna(
        listings[percent_cols].mean())
    return listings, listings_cols_df


def fill_time_cols(listings, listings_cols_df):
    """
    Fill the missing data for the 'time' columns.

    Args:
        listings (pandas.DataFrame): Contains the static features of each
            listing.
        listings_cols_df (pandas.DataFrame): A dataframe with the 'kind' of
            columns that each column is.
    Returns:
        The same arguments, with listings filled.
    """
    listings.host_response_time = listings.host_response_time.fillna('no data')
    return listings, listings_cols_df


def fill_cat_cols(listings, listings_cols_df):
    """
    Fill the missing data for the 'categorical simple' columns.

    Args:
        listings (pandas.DataFrame): Contains the static features of each
            listing.
        listings_cols_df (pandas.DataFrame): A dataframe with the 'kind' of
            columns that each column is.
    Returns:
        The same arguments, with listings filled.
    """
    listings.property_type = listings.property_type.fillna(
        listings.property_type.value_counts().index[0])
    return listings, listings_cols_df
