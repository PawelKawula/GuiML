from abc import ABC, abstractmethod

try:
    import tomllib as tomli
except ModuleNotFoundError:
    import tomli

from views.arguments_view.argument_entry import ArgumentEntry
from views.arguments_view.argument_combo import ArgumentCombo
from views.arguments_view.argument_switch import ArgumentSwitch
from views.arguments_view.argument_scale import ArgumentScale


class MlModel(ABC):
    """Base class for ML models"""

    @abstractmethod
    def predict(self, xs):
        """Gives us prediction for input"""
        pass

    @staticmethod
    def parse_options(fname, option):
        with open(fname, "rb") as f:
            conf = tomli.load(f)
            return conf[option] if option in conf else {}

    @staticmethod
    def parse_widget_type(widget_type):
        if widget_type == "entry":
            return ArgumentEntry
        elif widget_type == "combo":
            return ArgumentCombo
        elif widget_type == "switch":
            return ArgumentSwitch
        return ArgumentScale

    @staticmethod
    @abstractmethod
    def save_current(conf):
        pass

    @staticmethod
    def __load_dict_default(d, ret={}):
        for k, v in d.items():
            if isinstance(v, dict):
                if "default" in d[k]:
                    df = d[k]["default"]
                    if (
                        "can_none" in d[k]
                        and isinstance(df, str)
                        and df.lower() == "none"
                    ):
                        ret[k] = None
                    elif d[k]["widget_type"] == "combo":
                        ret[k] = d[k]["values"][df]
                    else:
                        ret[k] = df
                else:
                    ret[k] = {}
                    MlModel.__load_dict_default(d[k], ret[k])
        return ret

    @classmethod
    def load_default(cls, conf_file):
        with open(conf_file, "rb") as f:
            conf = MlModel.__load_dict_default(tomli.load(f))
        return conf.copy()

    @classmethod
    def get_default(cls):
        return cls._default_params
