import pandas as pd

raw_data_path = r'../data/7_Final'

corrected_data_path = r'../data/7_Final_2'


def uniform_time_five(src_file_path, des_file_path):
    time = 5
    file = pd.read_csv(src_file_path)
    time_arr = []
    location_arr = []
    account_arr = []
    cluster_arr = []
    word_arr = []
    for index, row in file.iterrows():
        if row['time'] < time:
            time_arr.append(time)
        else:
            while row['time'] > time:
                time += 5
            time_arr.append(time)
        location_arr.append(row['location'])
        account_arr.append(row['account'])
        cluster_arr.append(row['cluster'])
        word_arr.append(row['word'])
    output_data_frame = pd.DataFrame({'time': time_arr,
                                      'location': location_arr,
                                      'account': account_arr,
                                      'cluster': cluster_arr,
                                      'word': word_arr})
    output_data_frame.to_csv(des_file_path, index=False, sep=',')


def uniform_time_five_min(src_file_path, des_file_path):
    time = 5
    file = pd.read_csv(src_file_path)
    time_arr = []
    location_arr = []
    account_arr = []
    cluster_arr = []
    word_arr = []
    for index, row in file.iterrows():
        if row['time'] < time:
            time_arr.append(time)
        else:
            while row['time'] > time:
                time += 5
            time_arr.append(time)
        location_arr.append(row['location'])
        account_arr.append(row['account'])
        cluster_arr.append(row['cluster'])
        word_arr.append(row['word'])
    output_data_frame = pd.DataFrame({'time': time_arr,
                                      'location': location_arr,
                                      'cluster': cluster_arr,
                                      'word': word_arr})
    output_data_frame.to_csv(des_file_path, index=False, sep=',')


if __name__ == '__main__':
    uniform_time_five(raw_data_path + '/Cluster.csv', corrected_data_path + '/Cluster.csv')
    uniform_time_five_min(raw_data_path + '/Cluster.csv', corrected_data_path + '/ClusterMin.csv')
