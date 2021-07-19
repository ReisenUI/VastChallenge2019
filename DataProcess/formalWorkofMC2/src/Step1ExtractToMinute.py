import pandas as pd
import json

raw_data_path = r'../data'

corrected_data_path = r'../data/Step1_Extract_To_Minute'

name_pro = ['MySensor', 'TestUnit', 'CitizenScientist', 'ASWillhiem',
            'CitizenScientist', 'MySensor', 'MySensor', 'MySensor', 'MySensor',
            'HSS', 'RichardFox', 'CitizenScientist', 'HSS', 'AS-3', 'CitizenScientist',
            'CitizenScientist', 'HiMarkHS', 'HiMarkHS', 'CitizenScientist',
            'CitizenScientist', 'CitizenScientist', 'HSS', 'XrayLady',
            'CitizenScientist', 'CitizenScientist', 'CitizenScientist',
            'CitizenScientist', 'AS-1', 'AS-2', 'PeterLovesCrystals54',
            'RadCurieous', 'GermanWrinkler43', 'CitizenScientist',
            'CitizenScientist', 'HiMarkHS', 'CitizenScientist', 'Bob',
            'ProfessorSievert', 'CitizenScientist', 'MutantX',
            'CitizenScientist', 'AlwaysGlowing', 'CitizenScientist',
            'TaxiDriver', 'CitizenScientist', 'Ckimball',
            'UncleG', 'NeutronsAreFreeOfCharge', 'MySensor', 'MySensor']

corrected = []


def extract_minute(src_file_path, des_file_path):
    count = 0
    pre = 0
    file = pd.read_csv(src_file_path)
    time_arr = []
    sid_arr = []
    long_arr = []
    lat_arr = []
    value_arr = []
    uid_arr = []
    value_lis = [0 for x in range(0, 50)]
    counter = [0 for x in range(0, 50)]
    long_lis = [0 for x in range(0, 50)]
    lat_lis = [0 for x in range(0, 50)]
    for i, instance in enumerate(file['Timestamp']):
        count += 1
        cur = int(instance[-5: -3])
        if pre != cur:
            # print('\rcurrent-time: ', file['Timestamp'][i-1][:-3])
            pre = cur
            # Add to answer array
            for j in range(0, 50):
                if long_lis[j] == 0 and lat_lis[j] == 0 and value_lis[j] == 0:
                    continue
                time_arr.append(file['Timestamp'][i-1][:-3])
                sid_arr.append(j+1)
                long_arr.append(long_lis[j])
                lat_arr.append(lat_lis[j])
                value_arr.append(round(value_lis[j] / counter[j], 2))
                uid_arr.append(name_pro[j])

            value_lis = [0 for x in range(0, 50)]
            long_lis = [0 for x in range(0, 50)]
            lat_lis = [0 for x in range(0, 50)]
            counter = [0 for x in range(0, 50)]
            if file['Long'][i] == 0 and file['Lat'][i] == 0:
                continue
            if file['Value'][i] > 1000:
                corrected.append({'Timestamp': str(file['Timestamp'][i]),
                                  'Sensor-id': str(file['Sensor-id'][i]),
                                  'Value': str(file['Value'][i])})
            value_lis[file['Sensor-id'][i] - 1] += file['Value'][i]
            long_lis[file['Sensor-id'][i] - 1] = file['Long'][i]
            lat_lis[file['Sensor-id'][i] - 1] = file['Lat'][i]
            counter[file['Sensor-id'][i] - 1] += 1
        else:
            if file['Long'][i] == 0 and file['Lat'][i] == 0:
                continue
            if file['Value'][i] > 1000:
                corrected.append({'Timestamp': str(file['Timestamp'][i]),
                                  'Sensor-id': str(file['Sensor-id'][i]),
                                  'Value': str(file['Value'][i])})
            value_lis[file['Sensor-id'][i] - 1] += file['Value'][i]
            long_lis[file['Sensor-id'][i]-1] = file['Long'][i]
            lat_lis[file['Sensor-id'][i]-1] = file['Lat'][i]
            counter[file['Sensor-id'][i] - 1] += 1

        print('\rcurrent: ', count, end='')

    for j in range(0, 50):
        if long_lis[j] == 0 and lat_lis[j] == 0 and value_lis[j] == 0:
            continue
        time_arr.append(file['Timestamp'][i - 1][:-3])
        sid_arr.append(j + 1)
        long_arr.append(long_lis[j])
        lat_arr.append(lat_lis[j])
        value_arr.append(round(value_lis[j] / counter[j], 2))
        uid_arr.append(name_pro[j])

    output_data_frame = pd.DataFrame({'Timestamp': time_arr,
                                      'Sensor-id': sid_arr,
                                      'Long': long_arr,
                                      'Lat': lat_arr,
                                      'Value': value_arr,
                                      'User-id': uid_arr})
    output_data_frame.to_csv(des_file_path, index=False, sep=',')
    with open(corrected_data_path + '/errorDetector.txt', 'w', encoding='utf-8') as f:
        f.write(json.dumps(corrected, indent=4))


if __name__ == '__main__':
    extract_minute(raw_data_path + '/MobileSensorReadings.csv',
                   corrected_data_path + '/MobileSensorReadingsMin.csv')
