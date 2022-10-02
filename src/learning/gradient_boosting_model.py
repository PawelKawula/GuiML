#!/usr/bin/env python

import xgboost as xgb
from gi.repository import Gtk

from .ml_model import MlModel


class GradientBoostingModel(MlModel):
    def __init__(self, tdf, **kwargs):
        dtrain = xgb.DMatrix(tdf.train.xs, label=tdf.train.y)
        param = {"max_depth": 2, "eta": 1, "objective": "binary:logistic"}
        num_round = kwargs["num_round"] if "num_round" in kwargs else 2
        self.bst = xgb.train(kwargs, dtrain, num_round)

    def predict(self, xs):
        xs = xgb.DMatrix(xs)
        return self.bst.predict(xs)

    @staticmethod
    def setup_view():
        return {
            "verbose": (Gtk.Switch, {}),
        }
