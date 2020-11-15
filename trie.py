import math
from collections import defaultdict
import Levenshtein
from heapq import heappop, heappush


def levenshtein_distance(first, second):
    return Levenshtein.distance(first, second)


def spell_model(orig, fix, alpha=math.e):
    return alpha ** (-Levenshtein.distance(orig, fix))


def get_model_subset(prefix, model):
    subset = {}
    for item in model:
        if item.startswith(prefix):
            subset[item] = model[item]
    return subset


def terminate_subset(prefix, terminate):
    subset = set()
    for item in terminate:
        if item.startswith(prefix):
            subset.add(item)
    return subset


def calculate_weight(orig, node, alpha, beta):
    lang_model = beta * math.log2(node.weight)
    typo_model = math.log2(spell_model(node.prefix, orig, alpha))
    return lang_model + typo_model


class NodeItem:
    def __init__(self, weight, node, index):
        self.weight = weight
        self.node = node
        self.index = index

    def __lt__(self, other):
        return self.weight < other.weight

    def __le__(self, other):
        return self.weight <= other.weight


class Node:
    def __init__(self, prefix, prefix_model, terminate):
        self.prefix = prefix
        self.weight = prefix_model[prefix] if prefix in prefix_model else 0
        self.nodes = []
        self.terminate = prefix in terminate

        for next_prefix in prefix_model:
            if 100 > len(next_prefix) == len(prefix) + 1 and next_prefix.startswith(prefix):
                subset_prefix_model = get_model_subset(next_prefix, prefix_model)
                subset_terminate = terminate_subset(next_prefix, terminate)

                self.nodes.append(Node(next_prefix, subset_prefix_model, subset_terminate))

    def move(self, queue, orig, index, alpha, beta):
        for node in self.nodes:
            weight = calculate_weight(orig[:index], node, alpha=alpha, beta=beta)
            heappush(queue, NodeItem(-weight, node, index))


class Trie:
    def __init__(self, prefix_model, terminate):
        self.master_node = Node("", prefix_model, terminate)

    def get_fix(self, orig, alpha=2, beta=0.1, k=100):
        result_set = set()
        # result = []
        queue = []
        self.master_node.move(queue, orig, 1, alpha, beta)

        while len(result_set) < k:
            item = heappop(queue)
            node, index = item.node, item.index

            if node.terminate and node.prefix not in result_set and len(node.prefix) > len(orig) / 2:
                # result.append((node.prefix, weight))
                result_set.add(node.prefix)

            node.move(queue, orig, index + 1, alpha=alpha, beta=beta)
            #             if len(orig) > index + 1:
            #                 weight = beta * math.log2(node.weight) + math.log2(spell_model(node.prefix, orig[:index + 1], alpha))
            #                 heappush(queue, NodeItem(-weight, node, index + 1, label=orig[index + 1]))
            #             node.move(queue, orig, index, alpha=alpha, beta=beta, label=orig[:index])

        return result_set
