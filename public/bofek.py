import geopandas as gpd
import matplotlib
import matplotlib.pyplot as plt
import shapely
import fiona

matplotlib.use('Agg')

def polygon_plotter(pol,axis,lw=5,color = None):
    if pol.geom_type != 'Polygon':
        for geom in pol.geoms:
            axis.plot(*geom.exterior.xy,lw = lw,color = color)
    elif pol.geom_type == 'Polygon':
        axis.plot(*pol.exterior.xy,lw=lw,color = color)

class bofek2020:
    """
    This class has as attribute the bofek2020 dataset (I have merged 2020 data with 2012 to get everything in one).
    It should be noted that there are some discrepancies between the two datasets, but here I ignore this because they are minor.
    Maybe you just want to use the feather file, this script can be used as example material ;)
    """
    def __init__(self,crs = 'EPSG:28992',bofek2020_main_dir = "BOFEK2020"):
        self.bofek2020 = gpd.read_feather('bofek2020_gdf.feather').to_crs(crs)
        print("Creating spatial index")
        self.bofek2020_index = self.bofek2020.sindex

    def clip_to_polygon(self,polygon):
        clipped_gdf = self.bofek2020[self.bofek2020.geometry.intersects(polygon)]
        return clipped_gdf

    def plot_bofek(self,polygon,fig,ax,plot_pol = True,bufsize = 10):
        clipped_gdf = self.clip_to_polygon(polygon)
        axbox = ax.get_position()
        clipped_gdf.plot(ax=ax,column= 'Omschrijving cluster',legend=True,legend_kwds={'loc': 'upper center','bbox_to_anchor':(axbox.x0 + 0.5*axbox.width,axbox.y0),'bbox_transform': fig.transFigure})
        if plot_pol:
            polygon_plotter(polygon,ax,color = 'black')
        ax.axis('off')
        leg = ax.get_legend()
        ax.set_title("Bodem-BOFEK2020")
        ax.set_xlim(polygon.buffer(bufsize).bounds[0],polygon.buffer(bufsize).bounds[2])
        ax.set_ylim(polygon.buffer(bufsize).bounds[1],polygon.buffer(bufsize).bounds[3])
        return ax

def main(coordinates, type=None):
    str_polygon = ''
    index = 0
    for item in coordinates:
        index += 1
        str_polygon += str(item['x']) + ' ' + str(item['y'])
        if (index != len(coordinates)):
            str_polygon += ', '
    if type == 'file':
        fiona.drvsupport.supported_drivers['KML'] = 'rw'
        my_gdf = gpd.read_file('static/uploads/starch_potato.kml')
        my_gdf = my_gdf.to_crs(epsg=28992)
        polygon = my_gdf.geometry.iloc[0]
        my_bofek = bofek2020()
        my_bofek.plot_bofek(polygon, *plt.subplots())
        plt.savefig('static/image/plot.png', bbox_inches="tight")
        limit = 30
        line = my_bofek.bofek2020[my_bofek.bofek2020.intersects(polygon)].transpose().tail(limit)
    else:
        polygon = shapely.wkt.loads('POLYGON (('+str_polygon+'))')
        my_bofek = bofek2020()
        my_bofek.plot_bofek(polygon,*plt.subplots())
        plt.savefig('static/image/plot.png', bbox_inches="tight")
        # COMMAND ----------
        limit = 30
        line = my_bofek.bofek2020[my_bofek.bofek2020.intersects(polygon)].transpose().tail(limit)

    rows = []
    header = line.T.columns.tolist()
    row_values = line.values.tolist()
    for i in range(0, limit):
        values = []
        values.append(header[i])
        for item in row_values[i]:
            values.append(item)
        rows.append(values)

    return ('plot.png', line.columns.values, rows)

