import json

raw_data_path = r'../data/7_Final_3'

corrected_data_path = r'../data/7_Final_4'


region_name = ['Palace Hills', 'Northwest', 'Old Town', 'Safe Town',
               'Southwest', 'Downtown', 'Wilson Forest', 'Scenic Vista',
               'Broadview', 'Chapparal', 'Terrapin Springs', 'Pepper Mill',
               'Cheddarford', 'Easton', 'Weston', 'Southton', 'Oak Willow',
               'East Parton', 'West Parton']


def reset_time_template(time):
    template = {
        'time': time,
        'total': {
            'name': 'total',
            'children': []
        },
        'regions': []
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
            items['value'] += value
            return

    # 否则没有该单词，将该单词加入该聚类
    new_sub = reset_sub_template(word, value)
    array[count]['children'].append(new_sub)
    return


def merge_all(src_file_path, des_file_path):
    time_line = []
    f = open(src_file_path, 'r', encoding='utf-8')
    mc3_file = json.load(f)
    len3 = len(mc3_file)
    f.close()

    index = 0
    while index < len3:
        time_template = reset_time_template(mc3_file[index]['time'])
        time_template['regions'] = mc3_file[index]['regions']
        count = 0
        for items in mc3_file[index]['regions']:
            time_template['regions'][count]['name'] = region_name[count]
            if items['children'] != []:
                for main_key in items['children']:
                    for sub_key in main_key['children']:
                        judge_cluster(time_template['total']['children'],
                                      main_key['name'], sub_key['name'], sub_key['value'])
            count += 1
        index += 1
        time_line.append(time_template)
    with open(des_file_path, 'w', encoding='utf-8') as f:
        f.write(json.dumps(time_line, indent=4))


if __name__ == '__main__':
    merge_all(raw_data_path + '/MC3data.json',
              corrected_data_path + '/MC3data.json')
