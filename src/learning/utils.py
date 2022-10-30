import flatdict


def flatten_args(d):
    return {k.split(":")[-1]: v for k, v in flatdict.FlatDict(d).items()}


def dict_get_recursive_arg(d, *keys):
    res = d.copy()
    for k in keys:
        v = res.get(k, False)
        if not v:
            return {}
        res = res[k]
    return res


def flatten_arg_groups(d, *args):
    res = d.copy()
    print(args[0])
    for arg in args:
        if arg in res:
            del res[arg]
            res.update(d[arg])
    return res
