def get_recursive_dict_item(d, keys, to_end=None):
    to_end = -len(keys) if to_end is None else to_end
    for key in keys[:-to_end]:
        d = d[key]
    return d


def get_recursive_dict_item_from_toml(d, keys, to_end=None):
    keys = keys.split(".")
    return get_recursive_dict_item(d, keys, to_end)
