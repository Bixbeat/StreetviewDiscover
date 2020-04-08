from time import sleep
from datetime import date
from random import shuffle
from pathlib import Path

import streetview
import geopandas as gpd
import numpy as np
import pandas as pd

from lib.streetview_funcs import sample_pts_in_poly, store_panos_from_sample_pts
from lib.sqlite_funcs import StreetviewDB

## Setup database
Path('output').mkdir(exist_ok=True)
sv_db_path = 'output/sv_imgs.sqlite'
sv_db = StreetviewDB(sv_db_path)
sv_db.make_region_table('postcodes', set_target=True)

## Load target geometries
pc4_file = 'source/pc4_2018.geojson'
pc4_polys = gpd.read_file(pc4_file)
pc4_polys = pc4_polys.sample(frac=1).reset_index(drop=True)

## Get finished geometries from database
recorded_pcs = list(set([rec[0] for rec in sv_db.get_records()]))

for _,row in pc4_polys.iterrows():
    if row['postcode'] in recorded_pcs:
        continue
    else:
        print(row['postcode'])

    sample_pts = sample_pts_in_poly(row['geometry'], in_proj='epsg:28992')
    store_panos_from_sample_pts(sample_pts, row['postcode'], sv_db)

## Saving recorded panoramas
# streetview.api_download('kPcPLJftVZ237Yz7TyB6tA', '', 'output/images/', '')