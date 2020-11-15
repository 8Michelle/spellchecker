import re
from collections import defaultdict


def clean_corpus(filename="queries_all.txt"):
    with open(filename) as f:
        data = f.read()

    data = data.split("\n")
    data.remove(data[-1])

    corpus = []
    for item in data:
        if "\t" in item:
            corpus.append((item.split("\t")[0], item.split("\t")[1]))
        else:
            corpus.append((item, ""))

    cleaned_corpus = []
    for item in corpus:
        item0, item1 = item[0], item[1]
        item0 = re.sub(' +', ' ', (re.sub(r"[^\w\s]", "", item0)))
        item1 = re.sub(' +', ' ', (re.sub(r"[^\w\s]", "", item1)))
        cleaned_corpus.append((item0, item1))

    return cleaned_corpus


def get_prefix_model(corpus):
    corpus_line = re.sub(' +', ' ', " ".join([" ".join(item) for item in corpus]))
    prefix_list = []
    terminating = []
    for term in corpus_line.split(" "):
        result = ""
        for i, char in enumerate(term):
            result += char
            if i == len(term) - 1:
                terminating.append(result)
            prefix_list.append(result)

    prefix_model = defaultdict(int)
    for prefix in prefix_list:
        prefix_model[prefix] += 1

    sum_freq = 0
    for prefix in prefix_model:
        sum_freq += prefix_model[prefix]

    prefix_model = {prefix: prefix_model[prefix] / sum_freq for prefix in prefix_model}

    return prefix_model, terminating


def get_clear_prefix_model(corpus):
    clear_corpus = [item[1] if item[1] else item[0] for item in corpus]
    clear_corpus_line = " ".join([re.sub(' +', ' ', item) for item in clear_corpus])

    clear_prefix_list = []
    for term in clear_corpus_line.split(" "):
        result = ""
        for i, char in enumerate(term):
            result += char
            clear_prefix_list.append(result)

    clear_prefix_model = defaultdict(int)
    sum_freq = len(clear_prefix_list)
    for prefix in clear_prefix_list:
        clear_prefix_model[prefix] += 1 / sum_freq

    return clear_prefix_model


def get_bigram_model(corpus):
    clear_corpus = [item[1] if item[1] else item[0] for item in corpus]
    bigrams = []
    bigram_tuples = []
    for query in clear_corpus:
        bigram_tuples += [b for q in [query] for b in zip(q.split(" ")[:-1], q.split(" ")[1:])]
    for bigram in bigram_tuples:
        bigrams.append(bigram[0] + " " + bigram[1])

    bigram_model = defaultdict(int)
    sum_freq = len(bigrams)

    for bigram in bigrams:
        bigram_model[bigram] += 1 / sum_freq

    return bigram_model


def get_equal_length_model(corpus):
    words = defaultdict(int)
    for item in corpus:
        if not item[1]:
            for word in item[0].split():
                words[word] += 1

        elif len(item[0].split()) == len(item[1].split()):
            for word in item[0].split() + item[1].split():
                words[word] += 1

    sum_freq = 0
    for word, freq in words.items():
        sum_freq += freq

    for word in words:
        words[word] /= sum_freq

    return words, sum_freq


def get_fix_words_model(corpus):
    words = defaultdict(int)
    for item in corpus:
        if not item[1]:
            for word in item[0].split():
                words[word] += 1

        else:
            for word in item[0].split() + item[1].split():
                words[word] += 1

    sum_freq = 0
    for word, freq in words.items():
        sum_freq += freq

    for word in words:
        words[word] /= sum_freq

    return words
