#!/usr/bin/env python3

import csv

import pandas as pd
import numpy as np
from gi.repository import Gtk
from fastai.tabular.core import (
    TabularPandas,
    Categorify,
    FillMissing,
    cont_cat_split,
)


def get_store(values, **kwargs):
    tree_store = Gtk.ListStore(*([str] * len(values[0])))

    for row in values:
        tree_store.append(row)

    return tree_store


def get_values(df, **split_kwargs):
    in_values = df[split_kwargs["ins"]].to_numpy()
    out_values = (
        kwargs["model"].predict(df[split_kwargs["ins"]])
        if "model" in split_kwargs
        else df[split_kwargs["out"]]
    )
    out_values = out_values.to_numpy()
    print(in_values)
    values = np.concatenate((in_values, out_values[:, None]), axis=1).tolist()
    return values


def get_tabular_pandas(filename, ins, out, pct=75, model=None, **kwargs):
    df = pd.read_csv(filename)
    df = sort_data(df, **kwargs) if model else df
    df = df.astype(str)
    split = round(pct / 100 * len(df))
    splits = list(range(split)), list(range(split, len(df)))
    if len(df) == 0:
        return None, None
    procs = [Categorify, FillMissing]
    cont, cat = cont_cat_split(df, 1, dep_var=out)
    return df, TabularPandas(df, procs, cat, cont, y_names=out, splits=splits)


def sort_data(df, **kwargs):
    print("sort_data")
    if "validation_split_method" in kwargs:
        if kwargs["validation_split_method"] == "time-based":
            dt_col = df.select_dtypes(include=["datetime64"]).columns
            if len(dt_col) != 0:
                df = df.sort_values(by=dt_col)
            else:
                for c in df.columns[df.dtypes == "object"]:
                    try:
                        df[c] = pd.to_datetime(df[c])
                    except:
                        pass
        elif kwargs["validation_split_method"] == "random":
            df = df.sample(frac=1).reset_index(drop=True)
    else:
        df = df.sample(frac=1).reset_index(drop=True)
    return df

def get_columns_from_csv(filename):
    with open(filename) as f:
        reader = csv.reader(f)
        for row in reader:
            return row
