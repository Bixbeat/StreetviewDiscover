from lib.sqlite_funcs import StreetviewDB
from lib.data_mgmt import group_by_xy, get_xy_timestats, export_to_csv

## Setup database
sv_db_path = 'output/sv_imgs.sqlite'
sv_db = StreetviewDB(sv_db_path)
sv_db.make_region_table('postcodes', set_target=True)

panos = group_by_xy([rec for rec in sv_db.get_records()], 5, 6, precision=6)
pano_stats = get_xy_timestats(panos, 5, 6)
header = ['subregion_name', 'x', 'y', 'min_time', 'max_time', 'month_timediff', 'year_timediff', 'num_timesteps']
export_to_csv("output/pano_timestats.csv", pano_stats, header)