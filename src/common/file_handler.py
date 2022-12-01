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
from models.dataset_tree_store import DatasetTreeStore


def get_store(tdf, valid=False):
    columns = [str] * len(tdf.items.iloc[0])
    tree_store = DatasetTreeStore(valid, *columns)

    if not valid:
        tree_store.append_training(
            tdf.train.decode().items.astype(str).to_numpy().tolist()
        )
        tree_store.append_validation(
            tdf.valid.decode().items.astype(str).to_numpy().tolist()
        )
    else:
        tree_store.append_results(
            tdf.decode().items.astype(str).to_numpy().tolist()
        )

    return tree_store


def get_values(df, valid=False, **split_kwargs):
    new_df = df.valid.copy() if valid else df.copy()
    if "ml_model" in split_kwargs:
        new_df.items[split_kwargs["out"]] = split_kwargs["ml_model"].predict(
            new_df.train.xs
        )
    return new_df


def get_tabular_pandas(filename, ins, out, pct=75, model=None, **kwargs):
    df = pd.read_csv(filename)
    df = sort_data(df, **kwargs) if model else df
    split = round(pct / 100 * len(df))
    splits = list(range(split)), list(range(split, len(df)))
    if len(df) == 0:
        return None, None
    procs = [Categorify, FillMissing]
    cont, cat = cont_cat_split(df, 1, dep_var=out)
    tdf = TabularPandas(df, procs, cat, cont, y_names=out, splits=splits)
    return tdf


def sort_data(df, **kwargs):
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
