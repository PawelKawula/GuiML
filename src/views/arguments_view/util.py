def get_recursive_dict_item(d, keys, to_end=None):
    to_end = -len(keys) if to_end is None else to_end
    for key in keys[:-to_end]:
        d = d[key]
    return d


def set_recursive_dict_item(d, keys, value):
    for key in keys[:-1]:
        if key not in d:
            d[key] = {}
        d = d[key]
    d[keys[-1]] = value


def exists_recursive_dict_item(d, keys):
    for key in keys:
        if key in d:
            d = d[key]
        else:
            return False
    return True


def delete_recursive_dict(d, keys):
    for key in keys[:-1]:
        if key in d:
            d = d[key]
        else:
            return
    if keys[-1] in d:
        del d[keys[-1]]


def check_empty_dict(d):
    for key in d:
        if isinstance(d[key], dict):
            if not check_empty_dict(d[key]):
                return False
        elif d[key]:
            return False
    return True


def get_recursive_dict_item_from_toml(d, keys, to_end=None):
    keys = keys.split(".")
    return get_recursive_dict_item(d, keys, to_end)
