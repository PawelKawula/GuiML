import flatdict


def flatten_args(d):
    return {k.split(":")[-1]: v for k, v in flatdict.FlatDict(d).items()}


def dict_get_recursive_arg(d, *keys):
    for k in keys:
        v = d.get(k, False)
        if not v:
            return {}
        d = d[k]
    return d
