import xgboost as xgb
from gi.repository import Gtk

try:
    import tomllib as tomli
except ModuleNotFoundError:
    import tomli

from .ml_model import MlModel
from .utils import flatten_args


class GradientBoostingModel(MlModel):
    model_params = {}

    def __init__(self, tdf, **methods_dict):
        dtrain = xgb.DMatrix(tdf.train.xs, label=tdf.train.y)
        param = {"max_depth": 2, "eta": 1, "objective": "reg:squarederror"}
        param.update(GradientBoostingModel.model_params)
        param.update(methods_dict["learning"]["train"])
        num_round = param["num_round"] if "num_round" in param else 2
        self.model = xgb.train(param, dtrain, num_round)
        # for method, kwargs in methods_dict.items():
        #     getattr(self.model, method)(**kwargs)

    def predict(self, xs):
        xs = xgb.DMatrix(xs)
        return self.model.predict(xs)

    @staticmethod
    def parse_options(option):
        with open("learning/gradient_boosting.toml", "rb") as f:
            params = tomli.load(f)
            return params[option] if option in params else {}

    @staticmethod
    def save_config(conf):
        GradientBoostingModel.model_params.update(
            flatten_args(conf["general"]["parameters"])
        )
        xgb.set_config(**conf["general"]["global"])
