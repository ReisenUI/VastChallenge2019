import os
import warnings
warnings.filterwarnings('ignore')

import numpy as np
import pandas as pd

# Gensim
import gensim
import gensim.corpora as corpora

# spacy for lemmatization
import spacy

# Plotting tools
import pyLDAvis
import pyLDAvis.gensim_models
import matplotlib.pyplot as plt

# NLTK Stop words
from nltk.corpus import stopwords
stop_words = stopwords.words('english')
stop_words.extend(['from', 'subject', 're', 'edu', 'use'])

from pprint import pprint
from gensim.utils import simple_preprocess
from gensim.models import CoherenceModel

raw_data_path = r'../data/4_correct_misspell'

static_rule_path = r'../static'

correct_data_path = r'../data/5_topic_modeling'

os.environ.update({'MALLET_HOME': r'C:\\Users\\96202\\Desktop\\DataVis\\TopicModeling\\mallet-2.0.8\\'})
mallet_path = r"C:\\Users\\96202\\Desktop\\DataVis\\TopicModeling\\mallet-2.0.8\\bin\\mallet"


def pre_process(src_file_path):
    temp_text = ""
    upper = 1
    line_count = 0
    count = 0
    text_arr = []
    file = pd.read_csv(src_file_path)
    for i, instance in enumerate(file['message']):
        count += 1
        line_count += 1
        print('\rcurrent: ', count, end='')
        if temp_text == "":
            temp_text = instance
        else:
            temp_text = temp_text + " " + instance
        if line_count == upper:
            text_arr.append(temp_text)
            line_count = 0
            temp_text = ""
    print('')
    if temp_text != "":
        text_arr.append(temp_text)
    return text_arr


def pre_stop_words(src_file_path):
    with open(src_file_path, 'r', encoding='utf-8') as f:
        for lines in f:
            stop_words.extend([lines.strip()])


def remove_stopwords(raw_texts):
    return [[word for word in simple_preprocess(str(doc)) if word not in stop_words]
            for doc in raw_texts]


def make_bigrams(raw_texts):
    return [bigram_mod[doc] for doc in raw_texts]


def make_trigrams(raw_texts):
    return [trigram_mod[bigram_mod[doc]] for doc in raw_texts]


def lemmatization(raw_texts, allowed_postags=['NOUN', 'ADJ', 'VERB', 'ADV']):
    count = 0
    texts_out = []
    for sent in raw_texts:
        count += 1
        print("\rlemmatization current: ", count, end='')
        doc = nlp(" ".join(sent))
        texts_out.append([token.lemma_ for token in doc if token.pos_ in allowed_postags])
    print('')
    return texts_out


def compute_coherence_values(coherence_dictionary, coherence_corpus, texts, limit, start=2, step=3):
    in_coherence_values = []
    in_model_list = []
    for num_topics in range(start, limit, step):
        model = gensim.models.wrappers.LdaMallet(mallet_path, corpus=coherence_corpus,
                                                 num_topics=num_topics, id2word=id2word)
        in_model_list.append(model)
        coherence_model = CoherenceModel(model=model, texts=texts,
                                         dictionary=coherence_dictionary,
                                         coherence='c_v')
        in_coherence_values.append(coherence_model.get_coherence())
    return in_model_list, in_coherence_values


def sent_to_words(raw_sentences):
    for sentence in raw_sentences:
        yield (gensim.utils.simple_preprocess(str(sentence), deacc=True))
        # deacc????????????????????????


if __name__ == '__main__':
    # ???????????????????????????????????????????????????
    raw_data = pre_process(raw_data_path + '/YInt.csv')
    raw_data_word = list(sent_to_words(raw_data))
    pre_stop_words(static_rule_path + '/stopwords.txt')
    # print(raw_data_word[:1])

    # ???????????????????????????
    bigram = gensim.models.Phrases(raw_data_word, min_count=5, threshold=100)
    trigram = gensim.models.Phrases(bigram[raw_data_word], threshold=100)

    # ???????????????????????????????????????????????????/ ??????
    bigram_mod = gensim.models.phrases.Phraser(bigram)
    trigram_mod = gensim.models.phrases.Phraser(trigram)

    # ????????????????????????
    # print(trigram_mod[bigram_mod[raw_data_word[0]]])

    # ???????????????
    data_word_nostops = remove_stopwords(raw_data_word)

    # ??????????????????
    data_word_bigrams = make_bigrams(data_word_nostops)

    # ?????????spacy 'en' ??????
    nlp = spacy.load('en_core_web_sm', disable=['parser', 'ner'])

    # ?????????????????????????????????????????????????????????????????????
    data_lemmatized = lemmatization(data_word_bigrams, ['NOUN'])

    # ????????????
    id2word = corpora.Dictionary(data_lemmatized)

    # ???????????????
    corpus_texts = data_lemmatized

    # ???????????????????????????
    corpus = [id2word.doc2bow(text) for text in corpus_texts]

    # ???????????????
    # print(corpus)

    # # ???????????????LDA??????
    lda_malled = gensim.models.wrappers.LdaMallet(mallet_path, corpus=corpus,
                                                  num_topics=14, id2word=id2word)

    # ????????????
    pprint(lda_malled.show_topics(formatted=False))

    # ?????????????????????
    coherence_model_lda_mallet = CoherenceModel(model=lda_malled, texts=data_lemmatized,
                                                dictionary=id2word, coherence='c_v')
    coherence_lda_mallet = coherence_model_lda_mallet.get_coherence()
    print('\nCoherence Score: ', coherence_lda_mallet)

    # ????????????????????????topic???????????????????????????????????????????????????
    # model_list, coherence_values = compute_coherence_values(coherence_dictionary=id2word,
    #                                                         coherence_corpus=corpus,
    #                                                         texts=data_lemmatized,
    #                                                         start=2, limit=40, step=6)
    # limits = 40
    # starts = 2
    # steps = 6
    # x = range(starts, limits, steps)
    # plt.plot(x, coherence_values)
    # plt.xlabel("Num Topics")
    # plt.ylabel("Coherence Score")
    # plt.legend("coherence_values", loc="best")
    # plt.show()
    #
    # # ???????????????topic?????????????????????
    # for m, cv in zip(x, coherence_values):
    #     print("Num Topics =", m, " has Coherence Value of", round(cv, 4))
