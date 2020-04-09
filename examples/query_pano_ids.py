""""
Example code on how to query panorama ids

Sample data used are 4-digit post codes around the city center of Amsterdam,
Derived from the Dutch Statistics Office (CBS, 2017)
https://www.pdok.nl/introductie/-/article/cbs-postcode-statistieken
"""
from random import shuffle
from pathlib import Path

import streetview
import geopandas as gpd

from svdiscover.sampling import sample_pts_in_poly, store_panos_from_sample_pts
from svdiscover.database import StreetviewDB

## Setup database & table
Path('output').mkdir(exist_ok=True)
sv_db_path = 'output/sv_imgs.sqlite'

sv_db = StreetviewDB(sv_db_path)
sv_db.make_region_table('postcodes_ams', set_target=True)

## Load target geometries
pc4_file = 'examples/geodata/postcodes_ams.geojson'
pc4_polys = gpd.read_file(pc4_file)
pc4_polys = pc4_polys.sample(frac=1).reset_index(drop=True) # Randomly sample polygons

## Get previously-queried regions from database
recorded_pcs = list(set([rec[0] for rec in sv_db.get_records()]))

for _,row in pc4_polys.iterrows():
    if row['postcode'] in recorded_pcs:
        continue
    else:
        print(row['postcode'])

    sample_pts = sample_pts_in_poly(row['geometry'], in_proj='epsg:28992')
    store_panos_from_sample_pts(sample_pts, row['postcode'], sv_db)