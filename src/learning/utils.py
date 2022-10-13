import flatdict


def flatten_args(d):
    return {k.split(":")[-1]: v for k, v in flatdict.FlatDict(d).items()}
