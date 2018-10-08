import os
from pathlib import Path

MODULE_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = Path(MODULE_DIR).parent.parent
DATA_DIR = os.path.join(ROOT_DIR, 'data')
DATA_RAW = os.path.join(DATA_DIR, 'raw')
DATA_INTERIM = os.path.join(DATA_DIR, 'interim')
DATA_EXTERNAL = os.path.join(DATA_DIR, 'external')
DATA_PROCESSED = os.path.join(DATA_DIR, 'processed')

SEATTLE_CALENDAR = os.path.join(DATA_RAW, 'seattle', 'calendar.csv')
SEATTLE_LISTINGS = os.path.join(DATA_RAW, 'seattle', 'listings.csv')
SEATTLE_REVIEWS = os.path.join(DATA_RAW, 'seattle', 'reviews.csv')

SEATTLE_LISTINGS_COLS = os.path.join(
    DATA_INTERIM, 'seattle', 'listings_cols_df.pkl')
