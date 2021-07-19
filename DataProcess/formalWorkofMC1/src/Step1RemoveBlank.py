import pandas as pd
import math

raw_data_path = r'../data'

corrected_data_path = r'../data/Step1_Remove_Blank'


def remove_blank(src_file_path, des_file_path):
    count = 0
    file = pd.read_csv(src_file_path)
    time_arr = []
    water_arr = []
    power_arr = []
    roads_arr = []
    medical_arr = []
    build_arr = []
    shake_arr = []
    location_arr = []
    for i, instance in enumerate(file['time']):
        count += 1
        print('\rcurrent: ', count, end='')

        time_arr.append(instance)

        if math.isnan(file['sewer_and_water'][i]):
            water_arr.append(0)
        else:
            water_arr.append(file['sewer_and_water'][i])

        if math.isnan(file['power'][i]):
            power_arr.append(0)
        else:
            power_arr.append(file['power'][i])

        if math.isnan(file['roads_and_bridges'][i]):
            roads_arr.append(0)
        else:
            roads_arr.append(file['roads_and_bridges'][i])

        if math.isnan(file['medical'][i]):
            medical_arr.append(0)
        else:
            medical_arr.append(file['medical'][i])

        if math.isnan(file['buildings'][i]):
            build_arr.append(0)
        else:
            build_arr.append(file['buildings'][i])

        if math.isnan(file['shake_intensity'][i]):
            shake_arr.append(0)
        else:
            shake_arr.append(file['shake_intensity'][i])

        location_arr.append(file['location'][i])
    output_data_frame = pd.DataFrame({'time': time_arr,
                                      'sewer_and_water': water_arr,
                                      'power': power_arr,
                                      'roads_and_bridges': roads_arr,
                                      'medical': medical_arr,
                                      'buildings': build_arr,
                                      'shake_intensity': shake_arr,
                                      'location': location_arr})
    output_data_frame.to_csv(des_file_path, index=False, sep=',')


if __name__ == '__main__':
    remove_blank(raw_data_path + '/mc1-reports-data.csv',
                 corrected_data_path + '/reports-data-test.csv')
