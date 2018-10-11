import os
from pathlib import Path
import src

MODULE_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = str(Path(MODULE_DIR).parent.parent)
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

SEATTLE_CALENDAR_TEMP = os.path.join(DATA_INTERIM, 'seattle', 'calendar.pkl')
SEATTLE_LISTINGS_TEMP = os.path.join(DATA_INTERIM, 'seattle', 'listings.pkl')
SEATTLE_REVIEWS_TEMP = os.path.join(DATA_INTERIM, 'seattle', 'reviews.pkl')

SEATTLE_CALENDAR_FINAL = os.path.join(DATA_PROCESSED, 'seattle', 'calendar.pkl')
SEATTLE_LISTINGS_FINAL = os.path.join(DATA_PROCESSED, 'seattle', 'listings.pkl')
SEATTLE_REVIEWS_FINAL = os.path.join(DATA_PROCESSED, 'seattle', 'reviews.pkl')
