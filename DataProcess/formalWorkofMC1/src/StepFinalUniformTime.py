import pandas as pd

day, hour = 1440, 60

raw_data_path = r'../data/Step1_Remove_Blank'
correct_data_path = r'../data/StepFinal'


projection = {
    "Palace Hills": 1, "Northwest": 2, "Old Town": 3, "Safe Town": 4,
    "Southwest": 5, "Downtown": 6, "Wilson Forest": 7, "Scenic Vista": 8,
    "Broadview": 9, "Chapparal": 10, "Terrapin Springs": 11, "Pepper Mill": 12,
    "Cheddarford": 13, "Easton": 14, "Weston": 15, "Southton": 16,
    "Oak Willow": 17, "East Parton": 18, "West Parton": 19, "<Location with-held due to contract>": 0, "UNKNOWN": -1
}


def uniform_time(src_file_path, des_file_path, names):
    count = 0
    file = pd.read_csv(src_file_path, names=names, header=0)
    time_arr, water_arr, power_arr, transport_arr, medical_arr, building_arr, shake_arr, location_arr = \
        [], [], [], [], [], [], [], []
    for index, row in file.iterrows():
        count += 1
        print('\rcurrent: ', count, end=' ')
        # [-2: ] - minute, [-5: -3] - hour, [7: 9].strip() - day
        time_arr.append((int(row[names[0]][7:9].strip())-6) * day +
                        int(row[names[0]][-5:-3]) * hour +
                        int(row[names[0]][-2:]))
        water_arr.append(row[names[1]])
        power_arr.append(row[names[2]])
        transport_arr.append(row[names[3]])
        medical_arr.append(row[names[4]])
        building_arr.append(row[names[5]])
        shake_arr.append(row[names[6]])
        location_arr.append(row[names[7]])
    output_data_frame = pd.DataFrame({names[0]: time_arr,
                                      names[1]: water_arr,
                                      names[2]: power_arr,
                                      names[3]: transport_arr,
                                      names[4]: medical_arr,
                                      names[5]: building_arr,
                                      names[6]: shake_arr,
                                      names[7]: location_arr})
    output_data_frame.to_csv(des_file_path, index=False, sep=',')


if __name__ == '__main__':
    uniform_time(raw_data_path + '/reports-data.csv',
                 correct_data_path + '/reports-data.csv',
                 ['time', 'water', 'power', 'transport', 'medical', 'building', 'shake', 'location'])
