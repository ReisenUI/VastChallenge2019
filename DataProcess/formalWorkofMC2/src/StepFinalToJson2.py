import pandas as pd
import json

raw_data_path = r'../data/StepFinal'
corrected_data_path = r'../data/ODfile'


def reset_sensor_template(time, sid, long, lat, value):
    template = {
        "time": time,
        "sensorId": sid,
        "long": long,
        "lat": lat,
        "value": value,
    }
    return template


def extract_to_json(src_file_path, des_file_path):
    time_line = []
    count = 0
    file = pd.read_csv(src_file_path)
    for i, row in file.iterrows():
        count += 1
        print("\rcurrent: ", count, end='')
        if row['Long'] == 0 and row['Lat'] == 0 and row['value'] == 0:
            continue
        time_line.append(reset_sensor_template(row['time'], row['sensorId'], row['Long'],
                                               row['Lat'], row['value']))
    with open(des_file_path, 'w', encoding='utf-8') as f:
        f.write(json.dumps(time_line, indent=4))


if __name__ == '__main__':
    extract_to_json(raw_data_path + '/MobileSensorReadingsLong.csv',
                    corrected_data_path + '/MC2path.json')
