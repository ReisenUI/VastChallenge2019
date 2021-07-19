import json
import pandas as pd

pd.set_option('display.max_colwidth', None)
pd.set_option('display.max_columns', None)

pd.set_option('display.max_rows', None)

raw_data_path = r'../data/2_disgusting_users'

static_rule_path = r'../static'

corrected_data_path = r'../data/3_extract_hashtag_cue'


def get_lib(src_file_path):
    return_info = []
    with open(src_file_path, 'r', encoding='utf-8') as f:
        for line in f:
            return_info.append(line.strip())
        f.close()
    return return_info


def most_cued(src_file_path, des_file_path):
    count = 0
    file = pd.read_csv(src_file_path)
    cued_user = {}
    user_arr = []
    message_arr = []
    for i, instance in enumerate(file['message']):
        count += 1
        print('\r3-current: ', count, end='')
        if isinstance(instance, str):
            if 're:' not in instance:
                user_arr.append(file['account'][i])
                message_arr.append(instance.strip())
            else:
                for index, items in enumerate(message_arr):
                    test = instance.replace('re:', '')
                    test = test.strip()
                    if test == items:
                        if user_arr[index] not in cued_user:
                            cued_user[user_arr[index]] = 1
                        else:
                            cued_user[user_arr[index]] += 1
                        break
        else:
            continue
    print('')
    cued_user_sorted = sorted(cued_user.items(), key=lambda x: x[1], reverse=True)
    cued_user_sorted_new = {}
    for key, value in cued_user_sorted:
        cued_user_sorted_new[key] = value
    with open(des_file_path, 'w', encoding='utf-8') as f:
        f.write(json.dumps(cued_user_sorted_new, indent=4))
        f.close()


def extract(src_file_path, des_file_path, hash_file_path, cue_file_path, loc_lib_path, gov_lib_path):
    count = 0
    dict_hash = {}
    dict_cue = {}
    time_arr = []
    location_arr = []
    account_arr = []
    message_arr = []
    loc_lib = get_lib(loc_lib_path)
    gov_lib = get_lib(gov_lib_path)
    file = pd.read_csv(src_file_path)
    for i, instance in enumerate(file['message']):
        count += 1
        print("\r1-current: ", count, end='')
        current_text = ""
        # if file['location'][i] in loc_lib or file['account'][i] in gov_lib:
        #     continue
        time_arr.append(file['time'][i])
        location_arr.append(file['location'][i])
        account_arr.append(file['account'][i])
        if isinstance(instance, str):
            for word in instance.split():
                if word[0] == '#' and len(word) > 2:
                    if word not in dict_hash:
                        dict_hash[word] = 1
                    else:
                        dict_hash[word] += 1
                elif word[0] == '@' and len(word) > 2:
                    if word not in dict_hash:
                        dict_cue[word] = 1
                    else:
                        dict_cue[word] += 1
                else:
                    if current_text == "":
                        current_text = word
                    else:
                        current_text = current_text + " " + word
        else:
            current_text = file['message'][i]
        message_arr.append(current_text)
    print('')
    output_data_frame = pd.DataFrame({'time': time_arr, 'location': location_arr,
                                     'account': account_arr, 'message': message_arr})
    output_data_frame.to_csv(des_file_path, index=False, sep=',')
    dict_hash_sorted = sorted(dict_hash.items(), key=lambda x: x[1], reverse=True)
    dict_cue_sorted = sorted(dict_cue.items(), key=lambda x: x[1], reverse=True)
    dict_hash_sorted_new = {}
    dict_cue_sorted_new = {}
    for key, value in dict_hash_sorted:
        dict_hash_sorted_new[key] = value
    for key, value in dict_cue_sorted:
        dict_cue_sorted_new[key] = value
    with open(hash_file_path, 'w', encoding='utf-8') as f:
        f.write(json.dumps(dict_hash_sorted_new, indent=4))
        f.close()
    with open(cue_file_path, 'w', encoding='utf-8') as f:
        f.write(json.dumps(dict_cue_sorted_new, indent=4))
        f.close()


def extract_to_new(src_file_path, hash_file_path, cue_file_path):
    file = pd.read_csv(src_file_path)
    count = 0
    hash_time = []
    hash_location = []
    hash_account = []
    hash_message = []
    cue_time = []
    cue_location = []
    cue_account = []
    cue_message = []
    for i, instance in enumerate(file['message']):
        count += 1
        print("\r2-current: ", count, end='')
        current_hash = []
        current_cue = []
        if isinstance(instance, str):
            for word in instance.split():
                if word[0] == '#' and len(word) > 2:  # add hash_tag array
                    current_hash.append(word)
                elif word[0] == '@' and len(word) > 2:
                    current_cue.append(word)
            if len(current_hash) != 0:
                hash_time.append(file['time'][i])
                hash_location.append(file['location'][i])
                hash_account.append(file['account'][i])
                hash_message.append(current_hash)
            if len(current_cue) != 0:
                cue_time.append(file['time'][i])
                cue_location.append(file['location'][i])
                cue_account.append(file['account'][i])
                cue_message.append(current_cue)
    print('')
    output_data_frame_hash = pd.DataFrame({'time': hash_time,
                                           'location': hash_location,
                                           'account': hash_account,
                                           'hashtag': hash_message})
    output_data_frame_hash.to_csv(hash_file_path, index=False, sep=',')
    output_data_frame_cue = pd.DataFrame({'time': cue_time,
                                          'location': cue_location,
                                          'account': cue_account,
                                          'cue': cue_message})
    output_data_frame_cue.to_csv(cue_file_path, index=False, sep=',')


def get_essential_user(src_file_path, loc_file_path, gov_file_path, loc_lib_path, gov_lib_path):
    count = 0
    file = pd.read_csv(src_file_path)
    loc_lib = get_lib(loc_lib_path)
    loc_time = []
    loc_location = []
    loc_account = []
    loc_message = []
    gov_lib = get_lib(gov_lib_path)
    gov_time = []
    gov_location = []
    gov_account = []
    gov_message = []
    for i in range(0, len(file['location'])):
        count += 1
        print('\r4-current: ', count, end='')
        if file['location'][i] in loc_lib:
            loc_time.append(file['time'][i])
            loc_location.append(file['location'][i])
            loc_account.append(file['account'][i])
            loc_message.append(file['message'][i])
        elif file['account'][i] in gov_lib:
            gov_time.append(file['time'][i])
            gov_location.append(file['location'][i])
            gov_account.append(file['account'][i])
            gov_message.append(file['message'][i])
    output_data_frame_loc = pd.DataFrame({'time': loc_time,
                                          'location': loc_location,
                                          'account': loc_account,
                                          'message': loc_message})
    output_data_frame_loc.to_csv(loc_file_path, index=False, sep=',')
    output_data_frame_gov = pd.DataFrame({'time': gov_time,
                                          'location': gov_location,
                                          'account': gov_account,
                                          'message': gov_message})
    output_data_frame_gov.to_csv(gov_file_path, index=False, sep=',')


if __name__ == '__main__':
    # 1 - extract hash tag and cue information
    extract(raw_data_path + '/YInt.csv', corrected_data_path + '/YInt.csv',
            corrected_data_path + '/hashtag.json', corrected_data_path + '/cueinfo.json',
            static_rule_path + '/essential_location.txt', static_rule_path + '/essential_account.txt')

    # 2 - extract hash tag and cue information to a new message file
    extract_to_new(raw_data_path + '/YInt.csv',
                   corrected_data_path + '/YIntWithHashTag.csv', corrected_data_path + '/YIntWithCueInfo.csv')

    # 3 - calculate who was cued the most frequent
    most_cued(raw_data_path + '/YInt.csv', corrected_data_path + '/MostCuedAccount.json')

    # 4 - extract the government
    get_essential_user(raw_data_path + '/YInt.csv',
                       corrected_data_path + '/YIntLocation.csv', corrected_data_path + '/YIntGovernment.csv',
                       static_rule_path + '/essential_location.txt', static_rule_path + '/essential_account.txt')
