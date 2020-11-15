from data_preparing import clean_corpus, get_prefix_model, get_bigram_model, get_clear_prefix_model,\
    get_equal_length_model, get_fix_words_model
import pickle


def index():
    corpus = clean_corpus()

    prefix_model, terminating = get_prefix_model(corpus)
    with open("prefix_model", "wb") as f:
        pickle.dump(prefix_model, f)

    with open("terminating", "wb") as f:
        pickle.dump(terminating, f)

    bigram_model = get_bigram_model(corpus)
    with open("bigram_model", "wb") as f:
        pickle.dump(bigram_model, f)

    clear_prefix_model = get_clear_prefix_model(corpus)
    with open("clear_prefix_model", "wb") as f:
        pickle.dump(clear_prefix_model, f)

    equal_length_model = get_equal_length_model(corpus)
    with open("equal_length_model", "wb") as f:
        pickle.dump(equal_length_model, f)

    fix_words_model = get_fix_words_model(corpus)
    with open("fix_words_model", "wb") as f:
        pickle.dump(fix_words_model, f)


if __name__ == "__main__":
    index()
