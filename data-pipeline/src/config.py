import os

_current_dir = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(_current_dir, "..", ".."))

DATA_DIR = os.path.join(PROJECT_ROOT, "data")
RAW_DATA = os.path.join(DATA_DIR, "raw")
INTERIM_DATA = os.path.join(DATA_DIR, "interim")
PROCESSED_DATA = os.path.join(DATA_DIR, "processed")

TORONTO_PBF = os.path.join(INTERIM_DATA, "toronto-exact.osm.pbf")
