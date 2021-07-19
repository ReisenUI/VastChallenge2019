import pandas as pd
import json

raw_data_path = r'../data/7_Final_3'

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


def reset_sub_template(word, value=1):
    template = {
        'name': word,
        'value': value
    }
    return template


# 判断这个数组里面是否有这个聚类，如果有，是否有这个单词
# 如果没有这个单词，则新建，否则在单词下加一个
def judge_cluster(array, cluster, word, value=-1):
    # flag1, flag2 False时表示没有这个聚类
    flag1 = False
    count = 0
    for items in array:
        if items['name'] == cluster:
            flag1 = True
            break
        count += 1

    if value == -1:
        value = 1
    # 如果没有这个聚类，则添加该聚类
    if not flag1:
        new_main = reset_main_template(cluster)
        new_sub = reset_sub_template(word, value)
        new_main['children'].append(new_sub)
        array.append(new_main)
        return

    # 如果有这个聚类，则判断是否有相应单词
    for items in array[count]['children']:
        if items['name'] == word:  # 如果有这个单词，则直接value++
            items['value'] += 1
            return

    # 否则没有该单词，将该单词加入该聚类
    new_sub = reset_sub_template(word, value)
    array[count]['children'].append(new_sub)
    return


# add data_mc1 to data_mc3
def read_to_json(src_file_path_mc1, src_file_path_mc3, des_file_path):
    time_line = []

    f = open(src_file_path_mc1)
    mc1_file = json.load(f)
    len1 = len(mc1_file)
    f.close()
    f = open(src_file_path_mc3)
    mc3_file = json.load(f)
    len3 = len(mc3_file)
    f.close()

    index1, index3 = 0, 0
    cur_time = 0
    while index1 < len1 or index3 < len3:
        time_template = reset_time_template(cur_time)
        regions = [reset_region_template() for x in range(1, 20)]
        print('\rindex1: {}, index3: {}'.format(index1, index3), end='')
        count = 0
        if index1 != len1:
            for items in mc1_file[index1]['regions']:
                if items['total'] != 0:
                    count2 = 0
                    for key in items.keys():
                        if key == 'total':
                            continue
                        judge_cluster(regions[count]['children'],
                                      key, 'APP_' + key, 0.3 * items[key] / items['total'])
                        count2 += 1
                count += 1
            index1 += 1
        # 由于MC3里面的数据不是连续的，所以需要特别判定
        if index3 != len3:
            count = 0
            if mc3_file[index3]['time'] == cur_time:
                for items in mc3_file[index3]['regions']:
                    if items['children'] != []:
                        for key in items['children']:
                            for sub_key in key['children']:
                                judge_cluster(regions[count]['children'],
                                              key['name'], sub_key['name'])
                    count += 1
                index3 += 1
            time_template['regions'] = regions
            time_line.append(time_template)
        cur_time += 5
    with open(des_file_path, 'w', encoding='utf-8') as f:
        f.write(json.dumps(time_line, indent=4))


if __name__ == '__main__':
    read_to_json(raw_data_path + '/MC1data.json',
                 raw_data_path + '/Prework.json',
                 corrected_data_path + '/MC3data.json')
