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
from .ml_model import MlModel


class DeepLearningModel(MlModel):
    display_name = "Deep Learning"

    def __init__(self, tdf):
        train_len, tdf_len = len(tdf.train), len(tdf.items)
        splits = list(range(train_len)), list(range(train_len, tdf_len))
        # new_tdf.setup()
        dls = tdf.dataloaders(1024)
        self.learner = tabular_learner(
            dls,
            layers=[500, 250],
            n_out=1,
            loss_func=F.mse_loss,
        )
        self.learner.fit(5, 1e-2)

    def predict(self, xs):
        return self.learner.predict(xs)

    @staticmethod
    def setup_view(view):
        return {}

if __name__ == "__main__":
    df = pd.read_csv("train.csv")
    splits = round(len(df) * 0.75)
    splits = list(range(splits)), list(range(splits, len(df)))
    dep_var = "SalePrice"
    procs = [Categorify, FillMissing, Normalize]
    cont, cat = cont_cat_split(df, 1, dep_var=dep_var)
    tdf = TabularPandas(df, procs, cat, cont, y_names=dep_var, splits=splits)
    dlm = DeepLearningModel(tdf)
