#!/usr/bin/env python3

from fastai.tabular.learner import tabular_learner
from fastai.tabular.core import (
    TabularPandas,
    Categorify,
    FillMissing,
    Normalize,
    cont_cat_split,
)
import torch.nn.functional as F
import pandas as pd
import numpy as np
from .model import Model


class DeepLearningModel(Model):
    def __init__(self, df, ins, out, splits):
        int_cols = df.select_dtypes(int).columns
        str_cols = df.select_dtypes(object).columns
        df[int_cols] = df[int_cols].astype(float)
        df[str_cols] = df[str_cols].astype("category")
        for cat in str_cols:
            df[cat] = df[cat].cat.codes
        cont, cat = cont_cat_split(df, 1, dep_var=out)
        df[cat] = df[cat].astype("category")
        procs = [Categorify, FillMissing]
        tdf = TabularPandas(df, procs, cat, cont, y_names=out, splits=splits)
        dls = tdf.dataloaders(1024)
        self.learner = tabular_learner(
            dls,
            y_range=(tdf[out].min(), tdf[out].max()),
            layers=[500, 250],
            n_out=1,
            loss_func=F.mse_loss,
        )
        self.learner.fit(5, 1e-2)

    def predict(self, xs):
        return [self.learner.predict(xs.iloc[i])[1].item() for i in range(len(xs))]


if __name__ == "__main__":
    df = pd.read_csv("train.csv")
    ins = df.columns.tolist()
    ins.remove("SalePrice")
    splits = round(len(df) * 0.75)
    splits = list(range(splits)), list(range(splits, len(df)))
    dlm = DeepLearningModel(df, ins, "SalePrice", splits)
    print(dlm.predict(df.loc[:10, ins]))
