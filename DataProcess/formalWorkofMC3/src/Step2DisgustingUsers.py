import pandas as pd
import json

pd.set_option('display.max_colwidth', None)
pd.set_option('display.max_columns', None)

pd.set_option('display.max_rows', None)

raw_data_path = r'../data/1_correct_ugly_word'

corrected_data_path = r'../data/2_disgusting_users'

disgusting_words = ['sale', 'deal']


def calc_users(file_path, des_file_path):
    file = pd.read_csv(file_path)
    user_dict = {}
    for i, instance in enumerate(file['account']):
        if instance not in user_dict:
            user_dict[instance] = 1
        else:
            user_dict[instance] += 1
    dict_sorted = sorted(user_dict.items(),
                         key=lambda x: x[1], reverse=True)
    dict_sorted_new = {}
    for key, value in dict_sorted:
        dict_sorted_new[key] = value
    with open(des_file_path, 'w', encoding='utf-8') as f:
        f.write(json.dumps(dict_sorted_new, indent=4))
        f.close()


def find_disgusting_user(file_path, des_file_path):
    file = pd.read_csv(file_path)
    user_dict = {}
    for i, instance in enumerate(file['message']):
        flag = False
        if isinstance(instance, str):
            for word in instance.split():
                for key in disgusting_words:
                    if key in word:
                        if file['account'][i] not in user_dict:
                            user_dict[file['account'][i]] = 1
                        else:
                            user_dict[file['account'][i]] += 1
                        flag = True
                if flag:
                    break
    dict_sorted = sorted(user_dict.items(),
                         key=lambda x: x[1], reverse=True)
    dict_sorted_new = {}
    for key, value in dict_sorted:
        if value < 5:
            break
        dict_sorted_new[key] = value
    with open(des_file_path, 'w', encoding='utf-8') as f:
        f.write(json.dumps(dict_sorted_new, indent=4))
        f.close()


def kick_off(file_path, des_file_path, json_file_path):
    # load file
    file = pd.read_csv(file_path)
    with open(json_file_path, 'r', encoding='utf-8') as f:
        blacklist = json.load(f)
    time_arr = []
    location_arr = []
    account_arr = []
    message_arr = []
    count = 0
    for i, instance in enumerate(file['account']):
        flag = False
        count += 1
        print(count)
        for key, value in blacklist.items():
            if key == instance:
                flag = True
                break
        if flag:
            continue
        time_arr.append(file['time'][i])
        location_arr.append(file['location'][i])
        message_arr.append(file['message'][i])
        account_arr.append(instance)
    output_data_frame = pd.DataFrame({'time': time_arr,
                                      'location': location_arr,
                                      'account': account_arr,
                                      'message': message_arr})
    output_data_frame.to_csv(des_file_path, index=False, sep=',')


if __name__ == '__main__':
    # 1 - calculate the tweets frequency of each users
    calc_users(raw_data_path + '/YInt.csv',
               corrected_data_path + '/user_frequency.json')

    # 2 - find disgusting user
    find_disgusting_user(raw_data_path + '/YInt.csv',
                         corrected_data_path + '/blacklist.json')

    # 3 - kick disgusting users off !!!!!
    kick_off(raw_data_path + '/YInt.csv',
             corrected_data_path + '/YInt.csv',
             corrected_data_path + '/blacklist.json')

    # 4 - calculate the tweets frequency of each users again
    calc_users(corrected_data_path + '/YInt.csv',
               corrected_data_path + '/user_frequency_cleaner.json')
