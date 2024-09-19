import random


def normalize_list(lst):
    return [lst[i:i + 10] for i in range(0, len(lst), 10)]


def shuffle_words(words, definitions):
    random.seed(41)
    combined = list(zip(words, definitions))
    random.shuffle(combined)

    words, definitions = zip(*combined)
    return list(words), list(definitions)
