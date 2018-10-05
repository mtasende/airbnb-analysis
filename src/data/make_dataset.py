# -*- coding: utf-8 -*-
import click
import logging
import os
import pandas as pd
import src.data.preprocessing as pp

ROOT_DIR = '../..'
DATA_DIR = os.path.join(ROOT_DIR, 'data')
DATA_RAW = os.path.join(DATA_DIR, 'raw')
DATA_INTERIM = os.path.join(DATA_DIR, 'interim')
DATA_EXTERNAL = os.path.join(DATA_DIR, 'external')
DATA_PROCESSED = os.path.join(DATA_DIR, 'processed')


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
    create_dataset(input_filepath, output_filepath)


def create_dataset(raw_dir=DATA_RAW, proc_dir=DATA_PROCESSED):
    """
    Does the same as main, but without 'click'. To be called from other
    functions or notebooks.
    """
    calendar, listings, reviews = load_data(raw_dir)
    calendar, listings, reviews = transform_prices(calendar, listings, reviews)



def load_data(raw_dir, city='seattle'):
    calendar = pd.read_csv(os.path.join(raw_dir, city, 'calendar.csv'))
    listings = pd.read_csv(os.path.join(raw_dir, city, 'listings.csv'))
    reviews = pd.read_csv(os.path.join(raw_dir, city, 'reviews.csv'))

    return calendar, listings, reviews


def transform_prices(calendar, listings, reviews):
    pass


if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    main()
