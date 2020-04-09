from datetime import date
from time import sleep

import streetview
import numpy as np
from pyproj import Proj, transform
from shapely.geometry import Point

def sample_pts_in_poly(poly_geom, n_samples=None, in_proj=None):
    """Samples n points that fall within a polygon's extent, optionally
    after reprojecting points to WGS84.

    TODO: Get coordinate system from poly object
    Arguments:
        poly_geom {shapely.geometry.polygon.Polygon} -- Target polygon in which points must fall
    
    Keyword Arguments:
        n_samples {int} -- Number of points to sample. Default will sample based on polygon area (default: {None})
        in_proj {str} -- EPSG string for the projection of the original polygon (default: {None})
    
    Returns:
        {list} -- List of coordinate pairs containing n sampled points in the polygon
    """    
    # Pre-define projections if needed
    if in_proj:
        in_proj = Proj(in_proj)
        out_proj = Proj('epsg:4326')    

    if n_samples == None:
        area_in_km = poly_geom.area / 100000
        n_samples = round(area_in_km) * 2
    xmin_orig, ymin_orig, xmax_orig, ymax_orig = poly_geom.bounds

    sample_pts = []
    while len(sample_pts) < n_samples:
        anchor_x = np.random.uniform(xmin_orig, xmax_orig, 1)
        anchor_y = np.random.uniform(ymin_orig, ymax_orig, 1)

        sample_pt = Point(anchor_x, anchor_y)
        if poly_geom.contains(sample_pt):
            # Reproject if defined
            if in_proj:
                reproj_pt = transform(in_proj, out_proj, anchor_x, anchor_y)
                sample_pt = [reproj_pt[0][0], reproj_pt[1][0]]
            sample_pts.append(sample_pt)
    return sample_pts

def store_panos_from_sample_pts(sample_pts, subregion_name, sv_db):
    """Retrieves panoramas and stores them in a SQLite database
    
    Arguments:
        sample_pts {list} -- List of coordinate pairs
        subregion_name {str} -- Subregion name to fill in the region table
        sv_db {StreetviewDB} -- SQLite database for panorama IDs
    """    
    for sample_pt in sample_pts:
        entries = panos_from_coord_pair(sample_pt, subregion_name)
        if len(entries) > 0:
            for entry in entries:
                sv_db.add_entry(entry, manual_commit=True)
                sv_db.db.commit()
        sleep(0.05)


def panos_from_coord_pair(sample_pt, subregion_name=''):
    """Get all panoramas with a date from a coordinate pair
    
    Arguments:
        sample_pt {list} -- List containing an X and Y coordinate in WGS84 coordinates
    
    Keyword Arguments:
        subregion_name {str} -- Optional subregion name for keeping track of aggregations (default: {''})
    
    Returns:
        {list} -- List containing dictionaries of all panoramas at the coordinate pairs
    """    
    anchor_pano = streetview.panoids(lat=sample_pt[1], lon=sample_pt[0])
    entries = []
    if len(anchor_pano) > 0:
        for pano in anchor_pano:
            if 'year' in pano:
                entry = {'subregion_name': subregion_name,
                            'pano_id': pano['panoid'],
                            'capture_date': f'{pano["year"]}-{pano["month"]}',
                            'anchor_x': sample_pt[0],
                            'anchor_y': sample_pt[1],
                            'pano_x': pano['lon'],
                            'pano_y': pano['lat'],
                            'lookup_date': str(date.today()),
                            'download_date': '',
                            'saved_path': ''}
                entries.append(entry)
    return entries        