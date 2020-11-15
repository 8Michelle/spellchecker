from trie import Trie
import pickle
from split_join_layout import get_split, switch_layout, get_join


def create_trie(test_mode):
    with open("prefix_model", "rb") as f:
        prefix_model = pickle.load(f)

    with open("terminating", "rb") as f:
        terminating = pickle.load(f)

    if test_mode:
        prefix_model = {prefix: weight for prefix, weight in prefix_model.items() if prefix.startswith('а')}

    return Trie(prefix_model, terminating)


def get_pairs(words, bigram_model):
    pairs = []
    for first in words[0]:
        for second in words[1]:
            pair = first + " " + second
            weight = bigram_model[pair] if pair in bigram_model else 0
            pairs.append((weight, pair))

    return pairs


def find_pairs_by_word(word, pairs):
    result = []
    for pair in pairs:
        if word in pair[1].split()[0]:
            result.append(pair)
    return result


class Spellchecker:
    def __init__(self, test_mode=False):
        self.trie = create_trie(test_mode)

        with open("bigram_model", "rb") as f:
            self.bigram_model = pickle.load(f)

        with open("equal_length_model", "rb") as f:
            self.equal_length_model, self.split_threshold = pickle.load(f)

        with open("keyboard_switches", "rb") as f:
            self.keyboard_switches = pickle.load(f)

        with open("fix_words_model", "rb") as f:
            self.fix_words_model = pickle.load(f)

    def generate_by_letters(self, query):
        tokens = query.split()
        if len(tokens) < 2:
            return max([(self.fix_words_model[token], token) for token in self.trie.get_fix(query)])[1]

        results = []
        for token in tokens:
            results.append(self.trie.get_fix(token, 2, 0.1, 100))

        pairs_blocks = []
        for index, _ in enumerate(tokens[:-1]):
            pairs_blocks.append(get_pairs((results[index], results[index + 1]), self.bigram_model))

        pair_first = max(pairs_blocks[0])
        new_query = pair_first[1]
        word = pair_first[1].split()[1]
        for block in pairs_blocks[1:]:
            pairs = find_pairs_by_word(word, block)
            pair = max(pairs)
            word = pair[1].split()[1]
            new_query += " " + word

        return new_query

    def generate_join(self, query):
        return get_join(query, self.equal_length_model)

    def generate_split(self, query):
        return get_split(query, self.equal_length_model, self.split_threshold)

    def generate_switch(self, query):
        return switch_layout(query, *self.keyboard_switches)

    def classify(self, queries):
        results = []
        for query in queries:
            query_weight = 1
            tokens = query.split()
            for token in tokens:
                query_weight *= self.fix_words_model[token] if token in self.fix_words_model else 0
            results.append((query_weight, query))
        return max(results)[1]

    def check(self, query):
        results = []
        results.append(self.generate_by_letters(query))
        results.append(self.generate_join(query))
        results.append(self.generate_split(query))
        results.append(self.generate_switch(query))
        return self.classify(results)


if __name__ == "__main__":
    spellchecker = Spellchecker()
    while True:
        query = input("query: ")
        if query:
            print(spellchecker.check(query))
        else:
            break
