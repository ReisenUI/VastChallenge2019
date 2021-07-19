import pandas as pd
import json

raw_data_path = r'../data/StepFinal'
corrected_data_path = r'../data/StepFinal_2'


def reset_time_template():
    template = {
        'time': 0,
        'water': 0,
        'power': 0,
        'transport': 0,
        'medical': 0,
        'building': 0,
        'shake': 0,
        'total': 0,
        'regions': []
    }
    return template


def reset_region_template():
    template = {
        'water': 0,
        'power': 0,
        'transport': 0,
        'medical': 0,
        'building': 0,
        'shake': 0,
        'total': 0
    }
    return template


def update_regions(region, rows):
    region['water'] = int(rows['water'])
    region['power'] = int(rows['power'])
    region['transport'] = int(rows['transport'])
    region['medical'] = int(rows['medical'])
    region['building'] = int(rows['building'])
    region['shake'] = int(rows['shake'])
    region['total'] += 1


def calc_total(region, word):
    t_sum = 0
    for reg in region:
        t_sum += reg[word]
    return t_sum


def update_time(timeline, region):
    word = ['water', 'power', 'transport', 'medical', 'building', 'shake', 'total']
    for items in word:
        timeline[items] = calc_total(region, items)
    timeline['regions'] = region


def read_to_json(src_file_path, des_file_path):
    time_line = []
    count = 0
    cur_time = 0
    time_template = reset_time_template()
    regions = [reset_region_template() for x in range(1, 20)]
    file = pd.read_csv(src_file_path)
    for index, row in file.iterrows():
        count += 1
        print("\rcurrent: ", count, end="")
        if row['time'] != cur_time:
            # update timeLine's value
            update_time(time_template, regions)
            time_template['time'] = cur_time
            cur_time = int(row['time'])
            time_line.append(time_template)
            time_template = reset_time_template()
            regions = [reset_region_template() for x in range(1, 20)]
            update_regions(regions[int(row['location']) - 1], row)
        else:
            update_regions(regions[int(row['location']) - 1], row)
    update_time(time_template, regions)
    if time_template['total'] != 0:
        time_template['time'] = cur_time
        time_line.append(time_template)
    with open(des_file_path, 'w', encoding='utf-8') as f:
        f.write(json.dumps(time_line, indent=4))


if __name__ == '__main__':
    read_to_json(raw_data_path + '/reports-data.csv',
                 corrected_data_path + '/MC1data.json')
