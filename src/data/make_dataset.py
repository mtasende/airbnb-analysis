# -*- coding: utf-8 -*-
import click
import logging
import pandas as pd
import src.data.preprocessing as pp
import src.data.missing_data as md
from src.data import DATA_RAW, DATA_PROCESSED, SEATTLE_CALENDAR_FINAL,\
    SEATTLE_LISTINGS_FINAL, SEATTLE_REVIEWS_FINAL


@click.command()
@click.argument('input_filepath', type=click.Path(exists=True), required=False)
@click.argument('output_filepath', type=click.Path(), required=False)
def main(input_filepath, output_filepath):
    """ Runs data processing scripts to turn raw data from (../raw) into
        cleaned data ready to be analyzed (saved in ../processed).
    """
    if input_filepath is None:
        input_filepath = DATA_RAW
    if output_filepath is None:
        output_filepath = DATA_PROCESSED
    logger = logging.getLogger(__name__)
    logger.info('\nConverting from: {}\nConverting to: {}'.format(
        input_filepath, output_filepath
    ))
    logger.info('making final data set from raw data')
    create_dataset(input_filepath)


def create_dataset(raw_dir=DATA_RAW):
    """
    Does the same as main, but without 'click'. To be called from other
    functions or notebooks.
    """
    calendar, listings, reviews = pp.load_data(raw_dir)
    calendar, listings, reviews = pp.transform_all(calendar,
                                                   listings,
                                                   reviews,
                                                   save_results=True)
    calendar, listings, reviews = md.fill_missing(calendar,
                                                  listings,
                                                  reviews,
                                                  save_results=True)
    save_to_processed(calendar, listings, reviews)


def save_to_processed(calendar, listings, reviews):
    """ Saves the data to the 'processed' folder. """
    calendar.to_pickle(SEATTLE_CALENDAR_FINAL)
    listings.to_pickle(SEATTLE_LISTINGS_FINAL)
    reviews.to_pickle(SEATTLE_REVIEWS_FINAL)


def load_processed():
    """ Saves the data to the 'processed' folder. """
    calendar = pd.read_pickle(SEATTLE_CALENDAR_FINAL)
    listings = pd.read_pickle(SEATTLE_LISTINGS_FINAL)
    reviews = pd.read_pickle(SEATTLE_REVIEWS_FINAL)
    return calendar, listings, reviews


if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    main()
