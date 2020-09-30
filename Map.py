"""In order to get geopoints, use the NearbyCities API call !!!"""

from bokeh.plotting import gmap, ColumnDataSource
from bokeh.models import GMapOptions 
from bokeh.embed import file_html
from bokeh.resources import CDN

key = open('googlekey.txt').read()
def generate_map(geopoints, city):
    """Generates a Google map based on GEOPOINTS and a central CITY.

    *Note: GEOPOINTS is a 1D list, which must be reformatted before proper use.*
    """

    # Basic formatting
    gp_pairs = []
    while geopoints:
        lat, long = geopoints.pop(0), geopoints.pop(0)
        gp_pairs.append([lat, long])
    lats, lons = [lat for lat, long in gp_pairs][1:], [lon for lat, lon in gp_pairs][1:]

    # Host city geopoint
    lat, lng = gp_pairs[0]
    google_map_options = GMapOptions(lat=lat, 
                                    lng=lng, 
                                    map_type='roadmap', 
                                    zoom=10) 

    # Google map generation
    google_map = gmap(
        key, 
        google_map_options
    ) 
    
    source = ColumnDataSource(
        data=dict(lat=lats,
                  lon=lons)
    )

    google_map.circle(x="lon", y="lat", size=15, fill_color="blue", fill_alpha=0.8, source=source)

    html = file_html(google_map, CDN)

    return html