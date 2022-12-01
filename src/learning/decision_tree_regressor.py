from sklearn.tree import DecisionTreeRegressor

from .decision_tree_abstract import DecisionTreeAbstractModel
from .ml_model import MlModel


class DecisionTreeRegressorModel(DecisionTreeAbstractModel):
    _current_params = {}
    _default_params = {}

    def __init__(self, tdf, **parameters_dict):
        super().__init__(tdf, **parameters_dict)
        params = {}
        params.update(
            DecisionTreeRegressorModel._default_params["general"]["init"]
        )
        params.update(
            DecisionTreeRegressorModel._current_params["init"]
            if "init" in DecisionTreeRegressorModel._current_params
            else {}
        )
        print(self.fit)
        self.model = DecisionTreeRegressor(**params)
        self.model.fit(self.tdf.train.xs, self.tdf.train.y, **self.fit)

    def predict(self, xs):
        return self.model.predict(xs)

    @staticmethod
    def parse_options(option):
        return MlModel.parse_options(
            "learning/decision_tree_regressor.toml", option
        )

    @staticmethod
    def save_current(conf):
        DecisionTreeRegressorModel._current_params.update(conf["general"])

    @classmethod
    def load_default(cls):
        cls._default_params = MlModel.load_default(
            "learning/decision_tree_regressor.toml"
        )


if __name__ == "__main__":
    import pandas as pd
    from fastai.tabular.core import (
        TabularPandas,
        Categorify,
        FillMissing,
        cont_cat_split,
    )

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
