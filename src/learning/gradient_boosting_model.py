import xgboost as xgb
from gi.repository import Gtk

from .ml_model import MlModel
from views.learn_dialog.learn_dialog_entry import LearnDialogEntry
from views.learn_dialog.learn_dialog_combo import LearnDialogCombo


class GradientBoostingModel(MlModel):
    def __init__(self, tdf, **kwargs):
        dtrain = xgb.DMatrix(tdf.train.xs, label=tdf.train.y)
        param = {"max_depth": 2, "eta": 1, "objective": "reg:squarederror"}
        param.update(kwargs)
        num_round = param["num_round"] if "num_round" in param else 2
        print(param)
        self.bst = xgb.train(param, dtrain, num_round)

    def predict(self, xs):
        xs = xgb.DMatrix(xs)
        return self.bst.predict(xs)

    @staticmethod
    def setup_view():
        return {
            "verbose": (Gtk.Switch, {}),
            "max_depth": (LearnDialogEntry, {"text": "1", "entry_type": int}),
            "eta": (LearnDialogCombo, {"values": list(range(2)), "entry_type": int}),
            "objective": (LearnDialogCombo, {"values": ["binary:logistic", "reg:squarederror"] }),
        }
