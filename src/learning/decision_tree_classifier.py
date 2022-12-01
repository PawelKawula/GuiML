from sklearn.tree import DecisionTreeClassifier

from .decision_tree_abstract import DecisionTreeAbstractModel
from .ml_model import MlModel


class DecisionTreeClassifierModel(DecisionTreeAbstractModel):
    _current_params = {}
    _default_params = {}

    def __init__(self, tdf, **parameters_dict):
        super().__init__(tdf, **parameters_dict)
        self.model = DecisionTreeClassifier(**self.init)
        self.model.fit(self.tdf.train.xs, self.tdf.train.y, **self.fit)

    def predict(self, xs):
        return self.model.predict(xs)

    @staticmethod
    def parse_options(option):
        return MlModel.parse_options(
            "learning/decision_tree_classifier.toml", option
        )

    @staticmethod
    def save_current(conf):
        print(conf)
        DecisionTreeClassifierModel._current_params.update(conf["general"])

    @classmethod
    def load_default(cls):
        cls.default_params = MlModel.load_default(
            "learning/decision_tree_classifier.toml"
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

    dlm = DecisionTreeClassifierModel(tdf)
    print(dlm.predict(tdf.valid.xs))
