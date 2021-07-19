import re
import pandas as pd

from enchant.checker import SpellChecker
from nltk import word_tokenize, pos_tag
from nltk.corpus import stopwords, wordnet
from nltk.stem import WordNetLemmatizer

pd.set_option('display.max_colwidth', None)
pd.set_option('display.max_columns', None)

pd.set_option('display.max_rows', None)

raw_data_path = r'../data/3_extract_hashtag_cue'

corrected_data_path = r'../data/4_correct_misspell'

dic = SpellChecker('en_US')
lemmatizer = WordNetLemmatizer()

punctuation = r"[,.?!=*':/\d]"
stop_words = stopwords.words('English')


def get_wordnet_pos(tag):
    if tag.startswith('J'):
        return wordnet.ADJ
    elif tag.startswith('V'):
        return wordnet.VERB
    elif tag.startswith('N'):
        return wordnet.NOUN
    elif tag.startswith('R'):
        return wordnet.ADV
    else:
        return wordnet.NOUN


def word_tokenization(src_file_path, des_file_path):
    count = 0
    file = pd.read_csv(src_file_path)
    time_arr = []
    location_arr = []
    account_arr = []
    message_arr = []
    for i, instance in enumerate(file['message']):
        count += 1
        print("\rcurrent: ", count, end='')
        current_text = ""
        time_arr.append(file['time'][i])
        location_arr.append(file['location'][i])
        account_arr.append(file['account'][i])
        if isinstance(instance, str):
            tokens = word_tokenize(instance.strip())
            for items in tokens:
                if current_text == "":
                    current_text = items
                else:
                    current_text = current_text + " " + items
        else:
            current_text = instance
        message_arr.append(current_text)
    print('')
    output_data_frame = pd.DataFrame({'time': time_arr,
                                      'location': location_arr,
                                      'account': account_arr,
                                      'message': message_arr})
    output_data_frame.to_csv(des_file_path, index=False, sep=',')


def spell_checker(src_file_path, des_file_path):
    count = 0
    file = pd.read_csv(src_file_path)
    time_arr = []
    location_arr = []
    account_arr = []
    message_arr = []
    for i, instance in enumerate(file['message']):
        count += 1
        print("\rcurrent: ", count, end='')
        new_text = ""
        time_arr.append(file['time'][i])
        location_arr.append(file['location'][i])
        account_arr.append(file['account'][i])
        if isinstance(instance, str):
            current_text = re.sub(punctuation, "", str(instance).lower())
            for word in current_text.split():
                if word == "re" or word == "" or len(word) < 3:
                    continue
                else:
                    if word not in stop_words:
                        if dic.check(word) is True:
                            if new_text == "":
                                new_text = word
                            else:
                                new_text = new_text + " " + word
                        else:
                            candidate_list = dic.suggest(word)
                            if len(candidate_list) == 0:
                                new_word = word
                            else:
                                new_word = candidate_list[0]
                            if new_text == "":
                                new_text = new_word
                            else:
                                new_text = new_text + " " + new_word
        else:
            new_text = re.sub(punctuation, "", str(instance).lower())
        message_arr.append(new_text)
    print('')
    out_put_frame = pd.DataFrame({'time': time_arr,
                                  'location': location_arr,
                                  'account': account_arr,
                                  'message': message_arr})
    out_put_frame.to_csv(des_file_path, index=False, sep=',')


def word_stem(src_file_path, des_file_path):
    count = 0
    file = pd.read_csv(src_file_path)
    time_arr = []
    location_arr = []
    account_arr = []
    message_arr = []
    for i, instance in enumerate(file['message']):
        count += 1
        print("\rcurrent: ", count, end='')
        time_arr.append(file['time'][i])
        location_arr.append(file['location'][i])
        account_arr.append(file['account'][i])
        if isinstance(instance, str):
            current_text = word_tokenize(instance.strip())
            tagged_sent = pos_tag(current_text)
            new_text = ""
            for j in range(0, len(current_text)):
                if len(current_text[j]) < 3:
                    continue
                wordnet_pos = get_wordnet_pos(tagged_sent[j][1])
                if new_text == "":
                    new_text = lemmatizer.lemmatize(tagged_sent[j][0], wordnet_pos)
                else:
                    new_text = new_text + " " +\
                               lemmatizer.lemmatize(tagged_sent[j][0], wordnet_pos)
        else:
            new_text = instance
        message_arr.append(new_text)
    print('')
    output_data_frame = pd.DataFrame({'time': time_arr,
                                      'location': location_arr,
                                      'account': account_arr,
                                      'message': message_arr})
    output_data_frame.to_csv(des_file_path, index=False, sep=',')


if __name__ == '__main__':
    # 1 - tokenize text
    word_tokenization(raw_data_path + '/YInt.csv',
                      corrected_data_path + '/1_YIntTokenize.csv')

    # 2 - detect misspell
    spell_checker(corrected_data_path + '/1_YIntTokenize.csv',
                  corrected_data_path + '/2_YIntMisspell.csv')

    # 3 - word lemmatize
    word_stem(corrected_data_path + '/2_YIntMisspell.csv',
              corrected_data_path + '/YInt.csv')
