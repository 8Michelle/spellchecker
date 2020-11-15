import os
import struct
import pickle
from collections import defaultdict
import math


def expand_mask(mask, length):
    return '0' * (length - len(mask)) + mask


def join_by_mask(tokens, mask):
    if len(mask) + 1 != len(tokens):
        raise Exception("Mask and query are of unequal length")

    result = tokens[0]
    for index, marker in enumerate(mask):
        if int(marker):
            result += (tokens[index + 1])
        else:
            result += (' ' + tokens[index + 1])

    return result


def get_weight(word, prefix_model):
    if word in prefix_model:
        return prefix_model[word]
    else:
        return 0.0


def get_query_weight(query, prefix_model):
    weight = 1.0
    for token in query.split(" "):
        weight *= get_weight(token, prefix_model)
    return weight


def get_join(query, prefix_model):
    tokens = query.split(' ')
    if len(tokens) > 10:
        return query

    join_mask_length = len(tokens) - 1
    join_num = 2 ** join_mask_length
    result = [(get_query_weight(query, prefix_model), query)]

    for i in range(1, join_num):
        join_mask = expand_mask(bin(i)[2:], join_mask_length)
        joined = join_by_mask(tokens, join_mask)
        result.append((get_query_weight(joined, prefix_model), joined))

    return max(result, key=lambda x: x[0])[1]


def get_split(query, prefix_model, threshold):
    fix_query = []
    for token in query.split(" "):
        if get_weight(token, prefix_model) <= threshold:
            splits = [(0, token)]
            for i in range(1, len(token)):
                token_first, token_second = token[:i], token[i:]
                splits.append((get_weight(token_first, prefix_model) * get_weight(token_second, prefix_model),
                               token_first + ' ' + token_second))

            fix_query.append(max(splits, key=lambda x: x[0])[1])

        else:
            fix_query.append(token)

    return " ".join(fix_query)


def switch_layout(query, cyr2lat, lat2cyr):
    if set(query) & set(cyr2lat.keys()) == set(query):
        layout = cyr2lat
    elif set(query) & set(lat2cyr.keys()) == set(query):
        layout = lat2cyr
    else:
        return

    result = ""
    for char in query:
        if char in layout:
            result += layout[char]
        else:
            result += char

    return result
