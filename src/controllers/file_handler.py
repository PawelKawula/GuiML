#!/usr/bin/env python3


import pandas as pd
from gi.repository import Gtk


def populate(filename, ins, out, **kwargs):
    csv = pd.read_csv(filename)
    csv = csv[ins + [out]][:50].astype(str)
    kwargs["split_method"] = "time-based"
    if "split_method" in kwargs:
        if kwargs["split_method"] == "time-based":
            dt_col = csv.select_dtypes(include=['datetime64']).columns
            print(dt_col)
            if len(dt_col) != 0:
                csv = csv.sort_values(by=dt_col)
            else:
                csv = csv.sample(frac=1).reset_index(drop=True)
    else:
        csv = csv.sample(frac=1).reset_index(drop=True)
    if len(csv) == 0:
        return None, None
    in_values = csv[ins].to_numpy().tolist()
    out_values = csv[out].to_numpy().tolist()
    ins_tree_store = Gtk.ListStore(*([str] * len(ins)))
    out_tree_store = Gtk.ListStore(str)
    for row in in_values:
        ins_tree_store.append(row)
    for row in out_values:
        out_tree_store.append([row])
    return ins_tree_store, out_tree_store
