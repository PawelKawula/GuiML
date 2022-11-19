from abc import ABC, abstractmethod


from .ml_model import MlModel
from .utils import dict_get_recursive_arg


class DecisionTreeAbstractModel(MlModel, ABC):
    def __init__(self, tdf, **parameters_dict):
        self.tdf = tdf
        self.init = dict_get_recursive_arg(parameters_dict, "general", "init")
        self.fit = dict_get_recursive_arg(parameters_dict, "general", "fit")

    @staticmethod
    @abstractmethod
    def load_default():
        pass
