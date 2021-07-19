import pandas as pd
import json

raw_data_path = r'../data/7_Final'
corrected_data_path = r'../data/7_Final_4'


def reset_time_template(time):
    template = {
        'time': time,
        'value': 0
    }
    return template


def calc_total_post(src_file_path, des_file_path):
    time_line = []
    cur_time = 0
    file = pd.read_csv(src_file_path)
    time_template = reset_time_template(cur_time)
    for index, row in file.iterrows():
        if row['time'] <= cur_time:
            time_template['value'] += 1
        else:
            time_line.append(time_template)
            cur_time += 5
            time_template = reset_time_template(cur_time)
    time_line.append(time_template)
    while cur_time <= 7200:
        time_line.append(reset_time_template(cur_time))
        cur_time += 5
    with open(des_file_path, 'w', encoding='utf-8') as f:
        f.write(json.dumps(time_line, indent=4))


if __name__ == '__main__':
    calc_total_post(raw_data_path + '/YIntMin.csv',
                    corrected_data_path + '/Timeline.json')
