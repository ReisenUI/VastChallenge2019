import pandas as pd


raw_data_path = r'../data/Step1_Extract_To_Minute'
corrected_data_path = r'../data/StepFinal'

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


def extract_to_five(src_file_path, des_file_path):
    count = 0
    cur_line = 0
    file = pd.read_csv(src_file_path)
    cur_time = 5
    time_arr = []
    sensor_arr = []
    location_arr = []
    value_arr = []
    user_arr = []
    location = [-1 for x in range(0, 50)]
    sensor = [x+1 for x in range(0, 50)]
    counter = [0 for x in range(0, 50)]
    value = [0 for x in range(0, 50)]
    for index, row in file.iterrows():
        if row['time'] == 0:
            continue
        count += 1
        # if row['time'] == 6:
        #     break
        print('\rcurrent: ', count, end='')
        if cur_time == row['time']:
            for i in range(0, 50):
                time_arr.append(cur_time)
                sensor_arr.append(sensor[i])
                location_arr.append(location[i])
                if counter[i] == 0:
                    value_arr.append(0)
                else:
                    value_arr.append(value[i] / counter[i])
                user_arr.append(name_pro[i])
            location = [0 for x in range(0, 50)]
            sensor = [x+1 for x in range(0, 50)]
            counter = [0 for x in range(0, 50)]
            value = [0 for x in range(0, 50)]
            if location[int(row['sensorId']) - 1] != -1:
                location[int(row['sensorId']) - 1] = row['location']
                counter[int(row['sensorId']) - 1] += 1
                value[int(row['sensorId']) - 1] += float(row['value'])
            cur_time += 5
        else:
            sensor_id = int(row['sensorId']) - 1
            if row['location'] != -1:
                location[sensor_id] = row['location']
                counter[sensor_id] += 1
                value[sensor_id] += float(row['value'])
        cur_line += 1
    for i in range(0, 50):
        time_arr.append(cur_time)
        sensor_arr.append(sensor[i])
        location_arr.append(location[i])
        if counter[i] == 0:
            value_arr.append(0)
        else:
            value_arr.append(value[i] / counter[i])
        user_arr.append(name_pro[i])
    output_data_frame = pd.DataFrame({'time': time_arr,
                                      'sensorId': sensor_arr,
                                      'location': location_arr,
                                      'value': value_arr,
                                      'userId': user_arr})
    output_data_frame.to_csv(des_file_path, index=False, sep=',')


if __name__ == '__main__':
    extract_to_five(raw_data_path + '/MobileSensorReadingsMinMin.csv',
                    corrected_data_path + '/MobileSensorReadingsFive.csv')
