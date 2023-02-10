import xgboost as xgb
from gi.repository import Gtk

from .ml_model import MlModel
from .utils import flatten_args, flatten_arg_groups
from .decision_tree_regressor import DecisionTreeRegressorModel


class GradientBoostingModel(MlModel):
    _current_params = {}
    _default_params = {}

    def __init__(self, tdf, **methods_dict):
        dtrain = xgb.DMatrix(tdf.train.xs, label=tdf.train.y)
        param = {}
        groups = ["col_samples", "dart"]
        default_params = flatten_arg_groups(
            GradientBoostingModel._default_params["general"]["parameters"],
            *groups
        )
        current_params = flatten_arg_groups(
            GradientBoostingModel._current_params, *groups
        )
        param.update(default_params)
        param.update(current_params)
        param.update(methods_dict["learning"]["train"])
        num_round = param["num_round"] if "num_round" in param else 2
        self.model = xgb.train(param, dtrain, num_round)

    def predict(self, xs):
        xs = xgb.DMatrix(xs)
        return self.model.predict(xs)

    @staticmethod
    def parse_options(option):
        return MlModel.parse_options("gradient_boosting.toml", option)

    @staticmethod
    def save_current(conf):
        GradientBoostingModel._current_params.update(
            flatten_args(conf["general"]["parameters"])
        )
        xgb.set_config(**conf["general"]["global"])

    @classmethod
    def load_default(cls):
        cls._default_params = MlModel.load_default(
            "gradient_boosting.toml"
        )
