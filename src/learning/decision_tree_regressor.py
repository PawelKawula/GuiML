from fastai.tabular.core import (
    TabularPandas,
    Categorify,
    FillMissing,
    cont_cat_split,
)
from sklearn.tree import DecisionTreeRegressor
import pandas as pd

try:
    import tomllib as tomli
except ModuleNotFoundError:
    import tomli

from .ml_model import MlModel
from .utils import dict_get_recursive_arg


class DecisionTreeRegressorModel(MlModel):
    model_params = {}

    def __init__(self, tdf, **parameters_dict):
        self.tdf = tdf
        init = dict_get_recursive_arg(parameters_dict, "learning", "init")
        fit = dict_get_recursive_arg(parameters_dict, "learning", "fit")
        self.model = DecisionTreeRegressor(**init)
        self.model.fit(self.tdf.train.xs, self.tdf.train.y, **fit)

    def predict(self, xs):
        return self.model.predict(xs)

    @staticmethod
    def parse_options(option):
        with open("learning/decision_tree_regressor.toml", "rb") as f:
            conf = tomli.load(f)
            return conf[option] if option in conf else {}

    @staticmethod
    def save_config(conf):
        DecisionTreeRegressorModel.model_params.update(conf["general"])


if __name__ == "__main__":
    df = pd.read_csv("train.csv")
    dep_var = "SalePrice"
    ins = df.columns.tolist()
    ins.remove("SalePrice")
    splits = round(len(df) * 0.75)
    splits = list(range(splits)), list(range(splits, len(df)))
    cont, cat = cont_cat_split(df, 1, dep_var=dep_var)
    procs = [Categorify, FillMissing]
    tdf = TabularPandas(df, procs, cat, cont, y_names=dep_var, splits=splits)

    dlm = DecisionTreeRegressorModel(tdf)
    print(dlm.predict(tdf.valid.xs))
