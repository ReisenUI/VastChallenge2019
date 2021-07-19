import pandas as pd
import json

raw_data_path = r'../data/StepFinal'
corrected_data_path = r'../data/StepFinal'


def reset_time_template(time):
    template = {
        'time': time,
        'regions': []
    }
    return template


def reset_region_template():
    template = {
        'value': 0,
        'total': 0,
    }
    return template


def update_regions(region, row):
    region['value'] += float(row['value'])
    region['total'] += 1


def to_json(src_file_path, des_file_path):
    count = 0
    cur_time = 0
    time_line = []
    time_template = reset_time_template(cur_time)
    regions = [reset_region_template() for x in range(1, 20)]
    file = pd.read_csv(src_file_path)
    for index, row in file.iterrows():
        count += 1
        print('\rcurrent: ', count, end='')
        if row['time'] != cur_time:
            time_template['regions'] = regions
            time_line.append(time_template)
            cur_time = int(row['time'])
            time_template = reset_time_template(cur_time)
            regions = [reset_region_template() for x in range(1, 20)]
            if row['location'] != -1:
                update_regions(regions[int(row['location']) - 1], row)
        else:
            if row['location'] != -1:
                update_regions(regions[int(row['location']) - 1], row)
    time_template['regions'] = regions
    time_line.append(time_template)
    with open(des_file_path, 'w', encoding='utf-8') as f:
        f.write(json.dumps(time_line, indent=4))


if __name__ == '__main__':
    to_json(raw_data_path + '/MobileSensorReadings.csv',
            corrected_data_path + '/MC2dataMinute.json')
