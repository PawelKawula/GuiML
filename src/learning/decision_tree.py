from fastai.tabular.core import (
    TabularPandas,
    Categorify,
    FillMissing,
    cont_cat_split,
)
from sklearn.tree import DecisionTreeRegressor
import pandas as pd

from .ml_model import MlModel


class DecisionTreeModel(MlModel):
    display_name = "Decision Tree"

    def __init__(self, tdf, **kwargs):
        self.tdf = tdf
        self.model = DecisionTreeRegressor(**kwargs)
        self.model.fit(self.tdf.train.xs, self.tdf.train.y)

    def predict(self, xs):
        return self.model.predict(xs)

    @staticmethod
    def setup_view():
        return {}


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

    dlm = DecisionTreeModel(tdf)
    print(dlm.predict(tdf.valid.xs))
