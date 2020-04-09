from lib.sqlite_funcs import StreetviewDB
from lib.data_mgmt import group_by_anchors, get_anchor_timestats, export_to_csv

## Setup database
sv_db_path = 'output/sv_imgs.sqlite'
sv_db = StreetviewDB(sv_db_path)
sv_db.make_region_table('postcodes', set_target=True)

anchors = group_by_anchors([rec for rec in sv_db.get_records()])    
anchors = get_anchor_timestats(anchors)
header = ['subregion_name', 'anchor_x', 'anchor_y', 'min_time', 'max_time', 'month_timediff', 'year_timediff', 'num_timesteps']
export_to_csv("output/anchor_timestats.csv", anchors, header)