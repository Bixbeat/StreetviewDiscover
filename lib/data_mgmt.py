import csv
from datetime import datetime

def group_by_anchors(records):
    """Groups panoramas by their anchor location.
    Records must be sorted by anchor XY!
    
    Arguments:
        records {List of lists} -- Contains records extracted from a Streetview database 
    
    Returns:
        dict -- Contains records grouped by their anchor location as dict key
    """    
    groups = {}
    records_at_anchor = []
    records = iter(records)

    # Initialize t-1
    prev_record = next(records)
    records_at_anchor.append(prev_record)

    for record in records:
        # Check if using same anchor point
        if record[3:5] != prev_record[3:5]:
            groups[f'{prev_record[3]}-{prev_record[4]}'] = records_at_anchor
            records_at_anchor = []     
        records_at_anchor.append(record)
        prev_record = record
    return groups

def get_anchor_timestats(anchor_records):
    """Calculates biggest timedif, min pano date, max pano date, and num. of distinct pano dates per anchor XY
    
    Arguments:
        anchor_records {dict} -- Dictionary with anchor xy as keys and records at anchor xy as entries
    
    Returns:
        list -- List containing the anchor xy and its biggest time difference
    """    
    anchors = []

    for a in anchor_records:
        timestamps = [datetime.strptime(entry[2], '%Y-%m') for entry in anchor_records[a]]
        min_time = min(timestamps)
        max_time = max(timestamps)
        num_timesteps = len(set(timestamps))

        month_timediff = 12 * (max_time.year - min_time.year) + (max_time.month - min_time.month)
        year_timediff = month_timediff/12

        anchors.append([anchor_records[a][0][0],
                        anchor_records[a][0][3],
                        anchor_records[a][0][4],
                        min_time,
                        max_time,
                        month_timediff,
                        year_timediff,
                        num_timesteps])
    return anchors

def export_to_csv(out_filepath, record_list, header=None):
    """Simple utility to export SQLite records to a CSV
    
    Arguments:
        out_filepath {str} -- Filepath+name of output file
        record_list {list} -- List of lists containing SQLite database records
    """    
    with open(out_filepath, "w") as f:
        writer = csv.writer(f)
        if header:
            writer.writerow(header)
        writer.writerows(record_list)

# def plot_anchor_timediff(records, centerpoint, zoom=5):
#     map_obj = folium.Map(
#         location=centerpoint,
#         zoom_start=zoom
#     )

#     for r in records:
#         if r[-1] <= 2:
#             color = 'red'
#         elif r[-1] >= 3 and r[-1] < 6:
#             color = 'orange'
#         else:
#             color = 'green'

#         folium.Marker(
#             location=[r[1], r[0]],
#             #popup=f"{records[r][0][0]}",
#             icon=folium.Icon(color=color)
#         ).add_to(map_obj)
#     return map_obj
