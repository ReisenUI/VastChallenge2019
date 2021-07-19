import pandas as pd
from cartopy.io.shapereader import Reader
from shapely.geometry import *

shp_path = r'../static/StHimark.shp'
raw_data_path = r'../data/Step1_Extract_To_Minute'
raw_data_path2 = r'../data/Step2_Extract_To_Minute_Static'
corrected_data_path = r'../data/StepFinal'

day, hour = 1440, 60

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


reader = Reader(shp_path)


def uniform_time(src_file_path, des_file_path, names):
    count = 0
    file = pd.read_csv(src_file_path, names=names, header=0)
    time_arr = []
    sensorId_arr = []
    # location_arr = []
    long_arr = []
    lat_arr = []
    value_arr = []
    userId_arr = []
    for i, row in file.iterrows():
        count += 1
        print('\rcurrent: ', count, end=' ')
        flag = False
        # [8: 10] - day, [11: 13] - hour, [-2:] - minute
        time_arr.append((int(row[names[0]][8:10]) - 6) * day +
                        int(row[names[0]][11:13]) * hour +
                        int(row[names[0]][-2:]))
        # lon = lon2x(row[names[2]])
        # lat = lat2y(row[names[3]])
        # for index, items in enumerate(reader.geometries()):
        #     if items.intersects(Point(lon, lat)):
        #         flag = True
        #         location_arr.append(index + 1)
        # if not flag:
        #     location_arr.append(-1)
        long_arr.append(row[names[2]])
        lat_arr.append(row[names[3]])
        sensorId_arr.append(row[names[1]])
        value_arr.append(row[names[4]])
        userId_arr.append(row[names[5]])
    output_data_frame = pd.DataFrame({'time': time_arr,
                                      'sensorId': sensorId_arr,
                                      'Long': long_arr,
                                      'Lat': lat_arr,
                                      'value': value_arr,
                                      'userId': userId_arr})
    output_data_frame.to_csv(des_file_path, index=False, sep=',')


def uniform_time_static(src_file_path, des_file_path, names):
    count = 0
    file = pd.read_csv(src_file_path, names=names, header=0)
    time_arr = []
    sensorId_arr = []
    value_arr = []
    for i, row in file.iterrows():
        count += 1
        print("\rcurrent: ", count, end="")
        # print(row[names[0]])
        time_arr.append((int(row[names[0]][8:10]) - 6) * day +
                        int(row[names[0]][11:13]) * hour +
                        int(row[names[0]][-2:]))
        sensorId_arr.append(row[names[1]])
        value_arr.append(row[names[2]])
    output_data_frame = pd.DataFrame({names[0]: time_arr,
                                      names[1]: sensorId_arr,
                                      names[2]: value_arr})
    output_data_frame.to_csv(des_file_path, index=False, sep=',')


if __name__ == '__main__':
    # uniform_time(raw_data_path + '/MobileSensorReadings.csv',
    #              corrected_data_path + '/MobileSensorReadingsLong.csv',
    #              ['time', 'sensorId', 'long', 'lat', 'value', 'userId'])
    uniform_time_static(raw_data_path2 + '/StaticSensorReadings.csv',
                 corrected_data_path + '/StaticSensorReadingsLong.csv',
                 ['time', 'sensorId', 'value'])

