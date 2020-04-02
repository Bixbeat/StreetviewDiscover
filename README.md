# Streetview Discoverer
Simple functions for discovering current and historic Google Streetview panorama IDs in polygons of a given region.

### Why?
Because Google currently doesn't provide overviews of the availability and reach of historic data for any given region. With this repo I hope to make it easier for people to find historic data for their desired region.

### How?
By hooking up readily-existing API wrappers with geo-operations so that users can look up the availability images in their own region. Currently the framework accepts polygon datasets as input, in which points are sampled. These points are used to check for panoramas at their respective location. For best results use a dataset of street polygons.

## Installing
Install Robolyst' Streetview wrapper separately

`pip install git+https://github.com/robolyst/streetview`

Then install this repo

TODO: Prepare install files

`pip install git+https://github.com/Bixbeat/streetview-discoverer`

## Usage
### Querying pano-ids
```
## Setup database
sv_db_path = 'output/sv_imgs.sqlite'
sv_db = StreetviewDB(sv_db_path)
sv_db.make_region_table('postcodes', set_target=True)

## Load geodata
zipcode_file = 'source/zipcodes_nl_2018.geojson'
zipcode_polys = gpd.read_file(zipcode_file)

## Query & store panorama ids
for _,row in zipcode_polys.iterrows():
    sample_pts = sample_pts_in_poly(row['geometry'], n_samples=5, in_proj='epsg:28992')
    store_panos_from_sample_pts(sample_pts, row['postcode'], sv_db)
```
You don't need an API key to query the availability of panoramas. The listed example uses the 4-digit zipcode of the Netherlands. Get it from the [WFS endpoint](https://www.pdok.nl/geo-services/-/article/cbs-postcode-statistieken#d765e0742d1486171bab4b3ea46fcbdf).

For a more complete example, see `download_svs.py`.

### Viewing the SQLite database
The best way to quickly see your data is by using the excellent [SQLite browser](https://sqlitebrowser.org/dl/). If you download the zip, you don't need to install any files either.

### Downloading stored pano-ids
Get an API key from your [Google dashboard](https://console.cloud.google.com/google/maps-apis/overview), then, download them by passing the panorama id as reference to `api_download`.
```
my_google_key = '' # Get an API key from the Google dashboard
sv_db = StreetviewDB('Your path here') # Load database containing pano-ids
recorded_panos = sv_db.get_records()
For record in recorded_panos:
  streetview.api_download(panoid, heading, 'output/images/', my_google_key)
```
Files will be saved in the output directory by their year and pano-id.
