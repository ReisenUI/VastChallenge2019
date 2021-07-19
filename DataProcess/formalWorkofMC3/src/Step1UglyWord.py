import pandas as pd

pd.set_option('display.max_colwidth', None)
pd.set_option('display.max_columns', None)

pd.set_option('display.max_rows', None)

raw_data_path = r'../data/raw_data'

static_rules_path = r'../static'

corrected_data_path = r'../data/1_correct_ugly_word'

replace_lib = {}


def get_replace_lib(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        for lines in f:
            key, value = lines.strip().split(" ")
            replace_lib[key] = value


def correct(src_file_path, des_file_path):
    file = pd.read_csv(src_file_path)
    time_arr = []
    location_arr = []
    account_arr = []
    message_arr = []
    count = 0
    for i, instance in enumerate(file['message']):
        count += 1
        print("current: ", count)
        time_arr.append(file['time'][i])
        location_arr.append(file['location'][i])
        account_arr.append(file['account'][i])
        current_text = ""
        if isinstance(instance, str):
            for word in instance.split():
                for key, value in replace_lib.items():
                    if key in word:
                        word = word.replace(key, value)
                if current_text == "":
                    current_text = current_text + word
                else:
                    current_text = current_text + " " + word
        else:
            current_text = file['message'][i]
        message_arr.append(current_text)
    output_data_frame = pd.DataFrame({'time': time_arr, 'location': location_arr,
                                     'account': account_arr, 'message': message_arr})
    output_data_frame.to_csv(des_file_path, index=False, sep=',')


if __name__ == '__main__':
    # 1 - get replace library
    get_replace_lib(static_rules_path + '/replace.txt')

    # 2 - correct misspell
    correct(raw_data_path + '/YInt.csv', corrected_data_path + '/YInt.csv')
