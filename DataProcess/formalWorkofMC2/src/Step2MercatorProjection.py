import numpy as np
import pandas as pd
import cartopy.crs as ccrs
import cartopy.feature as cfeat
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
from cartopy.io.shapereader import Reader
from shapely.geometry import *
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

shp_path = r'../static/StHimark.shp'

raw_data_path = r'../data/Step1_Extract_To_Minute'

corrected_data_path = r'../data'

pt_lr_min = -13356433.40021311
pt_lr_max = -13326281.92702737
pt_lr_l_min = -119.981857
pt_lr_l_max = -119.712517
pt_ud_min = 949.7406152039766
pt_ud_max = 25330.81290255487
pt_ud_l_min = 0.009261
pt_ud_l_max = 0.228801

lr_k = (pt_lr_max - pt_lr_min) / (pt_lr_l_max - pt_lr_l_min)
ud_k = (pt_ud_max - pt_ud_min) / (pt_ud_l_max - pt_ud_l_min)


def lon2x(longitude):
    return pt_lr_min + lr_k * (longitude - pt_lr_l_min)


def lat2y(latitude):
    return pt_ud_min + ud_k * (latitude - pt_ud_l_min)


proj = ccrs.Mercator()
fig = plt.figure(figsize=(4, 4), dpi=400)
ax = fig.subplots(1, 1, subplot_kw={'projection': proj})

# extent = [-13359550, -13322000, 0, 26000]
extent = [-13356433.40021311, -13326281.92702737, 949.7406152039766, 25330.81290255487]
reader = Reader(shp_path)

city = cfeat.ShapelyFeature(reader.geometries(), proj, edgecolor='k', facecolor='none')
ax.add_feature(city, linewidth=0.7)
ax.set_extent(extent, crs=proj)

file = pd.read_csv(raw_data_path + '/MobileSensorReadings.csv')
count = 0

for items in reader.geometries():
    print(items)
start, end = 0, 50


with open(corrected_data_path + '/Debug.txt', 'w', encoding='utf-8') as f:
    for i, instance in enumerate(file['Long']):
        count += 1
        if count < start:
            continue
        if count == end:
            break
        print('\rcurrent: ', count, end=' ')
        long = lon2x(file['Long'][i])
        lat = lat2y(file['Lat'][i])
        print(long, lat)
        # for index, items in enumerate(reader.geometries()):
            # print(index, items.intersects(Point(long, lat)))
        writeStr = "" + str(i) + " " + str(file['Long'][i]) + " " + str(file['Lat'][i]) + "\n"
        f.write(writeStr)
        ax.scatter(long, lat, marker='.', s=1, color='chocolate')

plt.show()


# from shapely.geometry import *
#
# p1 = Point(.5, -0.5)
# p2 = Point(.5,1)
# p3 = Point(1,1)
#
# poly = Polygon([(0,0), (0,2), (2,2), (2,0)])
#
# for p in [p1, p2, p3]:
#     print(poly.intersects(p))
