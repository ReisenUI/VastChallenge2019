import pandas as pd

pd.set_option('display.max_colwidth', None)
pd.set_option('display.max_columns', None)

pd.set_option('display.max_rows', None)

raw_data_path = r'../data/4_correct_misspell'

static_rule_path = r'../static'

corrected_data_path = '../data/6_cluster'

cluster_dic = {}


def get_cluster_dict(src_file_path):
    dic = {}
    with open(src_file_path, 'r', encoding='utf-8') as f:
        for lines in f:
            dict_line = lines.strip().split(':')
            dic[dict_line[0]] = dict_line[1].split()
    return dic


def cluster_extract(src_file_path, des_file_path):
    count = 0
    file = pd.read_csv(src_file_path)
    time_arr = []
    location_arr = []
    account_arr = []
    cluster_arr = []
    word_arr = []
    for i, instance in enumerate(file['message']):
        count += 1
        print('\rcurrent: ', count, end='')
        if isinstance(instance, str):
            for word in instance.split():
                for key, value in cluster_dic.items():
                    if word in value:
                        time_arr.append(file['time'][i])
                        location_arr.append(file['location'][i])
                        account_arr.append(file['account'][i])
                        cluster_arr.append(key)
                        word_arr.append(word)
    output_data_frame = pd.DataFrame({'time': time_arr,
                                      'location': location_arr,
                                      'account': account_arr,
                                      'cluster': cluster_arr,
                                      'word': word_arr})
    output_data_frame.to_csv(des_file_path, index=False, sep=',')


if __name__ == '__main__':
    # 1 - get cluster dictionary
    cluster_dic = get_cluster_dict(static_rule_path + '/cluster.txt')

    # 2 - try to cluster different topic
    cluster_extract(raw_data_path + '/YInt.csv',
                    corrected_data_path + '/Cluster.csv')
