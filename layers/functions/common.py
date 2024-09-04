def normalize_list(lst):
    return [lst[i:i + 10] for i in range(0, len(lst), 10)]