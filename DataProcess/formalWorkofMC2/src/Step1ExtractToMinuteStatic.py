import pandas as pd

raw_data_path = r'../data'

corrected_data_path = r'../data/Step2_Extract_To_Minute_Static'

names = {
    '1': 1, '2': 4, '3': 6,
    '4': 9, '5': 11, '6': 12,
    '7': 13, '8': 14, '9': 15
}

namesReverse = {
    '1': 0, '4': 1, '6': 2,
    '9': 3, '11': 4, '12': 5,
    '13': 6, '14': 7, '15': 8
}


def extract_minute(src_file_path, des_file_path):
    count = 0
    pre = 0
    file = pd.read_csv(src_file_path)
    time_arr = []
    sid_arr = []
    value_arr = []
    value_lis = [0 for x in range(0, 9)]
    counter = [0 for x in range(0, 9)]
    for i, instance in enumerate(file['Timestamp']):
        count += 1
        cur = int(instance[-5: -3])
        if pre != cur:
            pre = cur
            # Add to answer array
            for j in range(0, 9):
                if value_lis[j] == 0:
                    continue
                time_arr.append(file['Timestamp'][i-1][:-3])
                sid_arr.append(names[str(j+1)])
                value_arr.append(round(value_lis[j] / counter[j], 2))

            value_lis = [0 for x in range(0, 9)]
            counter = [0 for x in range(0, 9)]
            value_lis[namesReverse[str(file['Sensor-id'][i])]] += file['Value'][i]
            counter[namesReverse[str(file['Sensor-id'][i])]] += 1
        else:
            value_lis[namesReverse[str(file['Sensor-id'][i])]] += file['Value'][i]
            counter[namesReverse[str(file['Sensor-id'][i])]] += 1
        print('\rcurrent: ', count, end='')
    for j in range(0, 9):
        time_arr.append(file['Timestamp'][i-1][:-3])
        sid_arr.append(names[str(j+1)])
        value_arr.append(round(value_lis[j] / counter[j], 2))

    output_data_frame = pd.DataFrame({'Timestamp': time_arr,
                                      'Sensor-id': sid_arr,
                                      'Value': value_arr})
    output_data_frame.to_csv(des_file_path, index=False, sep=',')


if __name__ == '__main__':
    extract_minute(raw_data_path + '/StaticSensorReadings.csv',
                   corrected_data_path + '/StaticSensorReadings.csv')
