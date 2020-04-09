""""
Example code on how to export panoramas stored in a pano-database,
either by aggregating at anchor XY or by panos at the same location
"""

import streetview
from svdiscover.database import StreetviewDB

# Get records
sv_db_path = 'output/sv_imgs.sqlite'
sv_db = StreetviewDB(sv_db_path)
sv_db.table = 'postcodes_ams'
all_records = [rec for rec in sv_db.get_records()]


# Download panoramas
my_google_api_key = ''

for record in all_records:
    heading = '' # By default: Gets forward-facing perspective
    
    # Panoramas are saved by their year & pano-id
    streetview.api_download(record[1], heading, 'output/images/', my_google_api_key)