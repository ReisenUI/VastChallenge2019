import pandas as pd

raw_data_path = r'../data/6_cluster'
raw_data_path2 = r'../data/2_disgusting_users'
corrected_data_path = r'../data/7_Final'

day, hour = 1440, 60

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
    if len(names) == 5:
        time_arr, location_arr, account_arr, cluster_arr, word_arr = [], [], [], [], []
    elif len(names) == 4:
        time_arr, location_arr, account_arr, message_arr = [], [], [], []
    for index, row in file.iterrows():
        count += 1
        print('\rcurrent: ', count, end='')
        # [8: 11] - day, [-8: -6] - hour, [-5: -3] - minute
        if len(names) == 5:
            time_arr.append((int(row[names[0]][8:11])-6) * day +
                            int(row[names[0]][-8: -6]) * hour +
                            int(row[names[0]][-5: -3]))
            location_arr.append(projection[row[names[1]]])
            account_arr.append(row[names[2]])
            cluster_arr.append(row[names[3]])
            word_arr.append(row[names[4]])
        elif len(names) == 4:
            time_arr.append((int(row[names[0]][8:11])-6) * day +
                            int(row[names[0]][-8: -6]) * hour +
                            int(row[names[0]][-5: -3]))
            location_arr.append(projection[row[names[1]]])
            account_arr.append(row[names[2]])
            message_arr.append(row[names[3]])
    if len(names) == 5:
        output_data_frame = pd.DataFrame({names[0]: time_arr,
                                         names[1]: location_arr,
                                         names[2]: account_arr,
                                         names[3]: cluster_arr,
                                         names[4]: word_arr})
    elif len(names) == 4:
        output_data_frame = pd.DataFrame({names[0]: time_arr,
                                         names[1]: location_arr,
                                         names[2]: account_arr,
                                         names[3]: message_arr})
    output_data_frame.to_csv(des_file_path, index=False, sep=',')


if __name__ == '__main__':
    uniform_time(raw_data_path + '/Cluster.csv',
                 corrected_data_path + '/Cluster.csv',
                 ['time', 'location', 'account', 'cluster', 'word'])

    uniform_time(raw_data_path2 + '/YInt.csv',
                 corrected_data_path + '/YInt.csv',
                 ['time', 'location', 'account', 'message'])
