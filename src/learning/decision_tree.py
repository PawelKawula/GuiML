#!/usr/bin/env python

from fastai.tabular.core import (
    TabularPandas,
    Categorify,
    FillMissing,
    cont_cat_split,
)
from sklearn.tree import DecisionTreeRegressor
import pandas as pd

from .model import Model


class DecisionTreeModel(Model):
    def __init__(self, tdf, **kwargs):
        self.tdf = tdf
        self.model = DecisionTreeRegressor(**kwargs)
        print(len(self.tdf.items.columns))
        self.model.fit(self.tdf.train.xs, self.tdf.train.y)

    def predict(self, xs):
        print(set(self.tdf.items.columns).difference(set(xs.columns)))
        return self.model.predict(xs.to_numpy())


if __name__ == "__main__":
    df = pd.read_csv("train.csv")
    cont, cat = cont_cat_split(df, 1, dep_var=out)
    procs = [Categorify, FillMissing]
    tdf = TabularPandas(df, procs, cat, cont, y_names=out, splits=splits)

    ins = df.columns.tolist()
    ins.remove("SalePrice")
    splits = round(len(df) * 0.75)
    splits = list(range(splits)), list(range(splits, len(df)))

    dlm = DecisionTreeModel(df, ins, "SalePrice", splits)
    print(dlm.predict(dlm.tdf.loc[:10].drop("SalePrice", axis=1)))
