import pandas as pd

raw_data_path = r'../data'

maxx = 0


def confirm(src_file_path, jud):
    count = 0
    file = pd.read_csv(src_file_path)
    for i, instance in enumerate(file['Value']):
        count += 1
        if count < 2000000:
            continue
        print('\rcurrent: ', count, end='')
        jud = max(maxx, instance)
    return jud


if __name__ == '__main__':
    maxx = confirm(raw_data_path + '/MobileSensorReadings.csv', maxx)
    print('')
    print(maxx)
