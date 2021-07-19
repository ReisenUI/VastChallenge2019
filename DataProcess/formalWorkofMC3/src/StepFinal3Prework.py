import pandas as pd
import json

raw_data_path = r'../data/7_Final_2'
corrected_data_path = r'../data/7_Final_3'


def reset_time_template(time):
    template = {
        'time': time,
        'regions': []
    }
    return template


def reset_region_template():
    template = {
        'children': []
    }
    return template


def reset_main_template(cluster):
    template = {
        'name': cluster,
        'children': []
    }
    return template


def reset_sub_template(word):
    template = {
        'name': word,
        'value': 1
    }
    return template


# 判断这个数组里面是否有这个聚类，如果有，是否有这个单词
# 如果没有这个单词，则新建，否则在单词下加一个
def judge_cluster(array, cluster, word):
    # flag1, flag2 False时表示没有这个聚类
    flag1 = False
    count = 0
    for items in array:
        if items['name'] == cluster:
            flag1 = True
            break
        count += 1

    # 如果没有这个聚类，则添加该聚类
    if not flag1:
        new_main = reset_main_template(cluster)
        new_sub = reset_sub_template(word)
        new_main['children'].append(new_sub)
        array.append(new_main)
        return

    # 如果有这个聚类，则判断是否有相应单词
    for items in array[count]['children']:
        if items['name'] == word:  # 如果有这个单词，则直接value++
            items['value'] += 1
            return

    # 否则没有该单词，将该单词加入该聚类
    new_sub = reset_sub_template(word)
    array[count]['children'].append(new_sub)
    return


def read_to_json(src_file_path, des_file_path):
    time_line = []
    count = 0
    cur_time = 0
    time_template = reset_time_template(cur_time)
    regions = [reset_region_template() for x in range(1, 20)]
    file = pd.read_csv(src_file_path)
    for index, row in file.iterrows():
        count += 1
        print("\rcurrent: ", count, end='')
        if row['time'] != cur_time:
            time_template['regions'] = regions
            time_line.append(time_template)
            cur_time = int(row['time'])
            time_template = reset_time_template(cur_time)
            regions = [reset_region_template() for x in range(1, 20)]

            judge_cluster(regions[int(row['location']) - 1]['children'], row['cluster'], row['word'])
        else:
            cur_cluster = row['cluster']
            cur_word = row['word']
            cur_location = int(row['location'])

            # 判断children里面是否有这个聚类
            judge_cluster(regions[cur_location - 1]['children'], cur_cluster, cur_word)
    time_template['regions'] = regions
    time_line.append(time_template)
    with open(des_file_path, 'w', encoding='utf-8') as f:
        f.write(json.dumps(time_line, indent=4))


if __name__ == '__main__':
    read_to_json(raw_data_path + '/ClusterMin.csv',
                 corrected_data_path + '/Prework.json')
