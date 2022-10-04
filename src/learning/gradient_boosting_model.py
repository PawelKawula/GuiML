import xgboost as xgb
from gi.repository import Gtk
import tomli

from .ml_model import MlModel
from views.learn_dialog.learn_dialog_entry import LearnDialogEntry
from views.learn_dialog.learn_dialog_combo import LearnDialogCombo


class GradientBoostingModel(MlModel):
    def __init__(self, tdf, **methods_dict):
        print(methods_dict)
        dtrain = xgb.DMatrix(tdf.train.xs, label=tdf.train.y)
        param = {"max_depth": 2, "eta": 1, "objective": "reg:squarederror"}
        param.update(methods_dict["train"])
        print(f"GRADIENT PARAM:{param}")
        del methods_dict["train"]
        num_round = param["num_round"] if "num_round" in param else 2
        self.model = xgb.train(param, dtrain, num_round)
        for method, kwargs in methods_dict.items():
            getattr(self.model, method)(**kwargs)

    def predict(self, xs):
        xs = xgb.DMatrix(xs)
        return self.model.predict(xs)

    @staticmethod
    def parse_options(option):
        with open("learning/gradient_boosting.toml", "rb") as f:
            return tomli.load(f)[option]
