# streetview-discoverer
Simple functions for finding current and historic Streetview panorama IDs in polygons of a given region.

### Why?
Because Google currently doesn't provide overviews of the availability and reach of historic data for any given region. With this repo I hope to make it easier for people to find historic data for their desired region.

### How?
By hooking up readily-existing API wrappers with geo-operations so that users can look up the availability images in their own region. Currently the framework accepts polygon datasets as input, in which points are sampled. These points are used to check for panoramas at their respective location. For best results use a polygons streets dataset.

Currently the framework only supports area size-based sampling for polygons supplied in projected coordinate systems (e.g. RD New), which will be updated later.

It stores each panorama with their listed date as well as the sample location from which they came in a SQLite database. From there they can be exported to a CSV to load in a geo-application.

Listed example uses the 4-digit zipcode of the Netherlands. The WFS endpoint is found here:
https://www.pdok.nl/geo-services/-/article/cbs-postcode-statistieken#d765e0742d1486171bab4b3ea46fcbdf
