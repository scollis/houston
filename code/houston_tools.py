"""
Tools for working on the Houston climatology project
"""
import pyart
from netCDF4 import num2date
import pytz
import cartopy
from matplotlib import pyplot as plt

# and finally we can make it into a function
def radar_plot(radar, radar_title=None, bb=None,
                   sweep=0, timezone='US/Central',
                   field='reflectivity', vmax=64,
                   vmin=-8, cmap = None):
    if radar_title is None:
        radar_title = 'Area '

    # Lets get some geographical context
    if bb is None:
        lats = radar.gate_latitude
        lons = radar.gate_longitude

        min_lon = lons['data'].min()
        min_lat = lats['data'].min()
        max_lat = lats['data'].max()
        max_lon = lons['data'].max()
        bb = {'north' : max_lat,
              'south' : min_lat,
              'east' : max_lon,
              'west' : min_lon}
    else:
        min_lon = bb['west']
        min_lat = bb['south']
        max_lon = bb['east']
        max_lat = bb['north']

    print('min_lat:', min_lat, ' min_lon:', min_lon,
          ' max_lat:', max_lat, ' max_lon:', max_lon)

    index_at_start = radar.sweep_start_ray_index['data'][sweep]
    time_at_start_of_radar = num2date(radar.time['data'][index_at_start],
                                      radar.time['units'])

    tzobj = pytz.timezone(timezone)
    local_time = tzobj.fromutc(time_at_start_of_radar)
    fancy_date_string = local_time.strftime('%A %B %d at %I:%M %p %Z')
    print(fancy_date_string)
    # Convert wind to components
    fig = plt.figure(figsize=(10, 8))
    display = pyart.graph.RadarMapDisplayCartopy(radar)
    lat_0 = display.loc[0]
    lon_0 = display.loc[1]

    # Set our Projection
    projection = cartopy.crs.Mercator(central_longitude=lon_0,
                                      min_latitude=min_lat, max_latitude=max_lat)

    # Call our function to reduce data
    display.plot_ppi_map(
        field, sweep, colorbar_flag=True,
        title=radar_title +' area ' + field + ' \n' + fancy_date_string,
        projection=projection,
        min_lon=min_lon, max_lon=max_lon, min_lat=min_lat, max_lat=max_lat,
        vmin=vmin, vmax=vmax, cmap=cmap)

    # Mark the radar
    display.plot_point(lon_0, lat_0, label_text='Radar')

    # Get the current axes and plot some lat and lon lines
    gl = display.ax.gridlines(draw_labels=True,
                              linewidth=2, color='gray', alpha=0.5, linestyle='--')
    gl.xlabels_top = False
    gl.ylabels_right = False

    return display

