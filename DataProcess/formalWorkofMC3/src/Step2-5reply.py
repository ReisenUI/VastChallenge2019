import pandas as pd

pd.set_option('display.max_colwidth', None)
pd.set_option('display.max_columns', None)

pd.set_option('display.max_rows', None)

raw_data_path = r'../data/2_disgusting_users'

corrected_data_path = r'../data/2_5_kick_away_reply'


def delete_reply(src_file_path, des_file_path):
    file = pd.read_csv(src_file_path)
    time_arr = []
    location_arr = []
    account_arr = []
    message_arr = []
    count = 0
    for i, instance in enumerate(file['message']):
        count += 1
        print('current: ', count)
        if isinstance(instance, str):
            if 're:' not in instance:
                time_arr.append(file['time'][i])
                location_arr.append(file['location'][i])
                account_arr.append(file['account'][i])
                message_arr.append(instance)
        else:
            time_arr.append(file['time'][i])
            location_arr.append(file['location'][i])
            account_arr.append(file['account'][i])
            message_arr.append(instance)

    output_data_frame = pd.DataFrame({'time': time_arr, 'location': location_arr,
                                      'account': account_arr, 'message': message_arr})
    output_data_frame.to_csv(des_file_path, index=False, sep=',')


if __name__ == '__main__':
    # 1 - kick off all reply message
    delete_reply(raw_data_path + '/YInt.csv', corrected_data_path + '/YInt.csv')
