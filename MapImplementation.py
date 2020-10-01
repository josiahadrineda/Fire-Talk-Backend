from bokeh.io import output_notebook, show, output_file
from bokeh.plotting import figure, ColumnDataSource
from bokeh.tile_providers import get_provider, Vendors
from bokeh.palettes import PRGn, RdYlGn
from bokeh.transform import linear_cmap,factor_cmap
from bokeh.layouts import row, column
from bokeh.models import GeoJSONDataSource, LinearColorMapper, ColorBar, NumeralTickFormatter
import numpy as np
import pandas as pd


# bokeh uses mercator coordinates: need to convert long/lat into mercator

# Define function to switch from lat/long to mercator coordinates





# importing the required modules 
from bokeh.plotting import gmap 
from bokeh.models import GMapOptions 
from bokeh.io import output_file, show 
  
# file to save the model 
output_file("gfg.html") 
  
# configuring the Google map 
lat = 34.1706    # host city latitude
lng = -118.837593 #host city longitude
map_type = "roadmap"
zoom = 10
google_map_options = GMapOptions(lat = lat, 
                                 lng = lng, 
                                 map_type = map_type, 
                                 zoom = zoom) 
  
# generating the Google map 
google_api_key = 'AIzaSyB4V1PQLYtuwe57Mrhj3bNIrd9pzwdMhrE' 
title = "Thousand Oaks"
google_map = gmap(google_api_key, 
                  google_map_options, 
                  title = title) 
  
# displaying the model 
source = ColumnDataSource(
    data=dict(lat=[ 34.1706, 34.1367],
              lon=[-118.837593, -118.6615])
)


google_map.circle(x="lon", y="lat", size=15, fill_color="blue", fill_alpha=0.8, source=source)

show(google_map)
