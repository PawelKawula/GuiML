from abc import ABC
import collections
from collections.abc import Sequence
from copy import deepcopy

from common.none_val import NoneVal

class DictWrapper(collections.Mapping):

    def __init__(self, data):
        self._data = data

    def __getitem__(self, key):
        return self._data[key]

    def __len__(self):
        return len(self._data)

    def __iter__(self):
        return iter(self._data)

class Config(ABC):
    def __init__(self,  config={}):
        self.__config = config

    def set_config(self, config):
        self.__config = config

    def _set_value(self, keys, value):
        self.__config[keys] = value

    def update(self, **kwargs):
        self.__config.update(kwargs)

    def __len__(self):
        return len(self.__config)

    def _get_dict(self):
        return self.__config

    def _get_value(self, key):
        if key in self.__config:
            return self.__config[key]
        return NoneVal


class ReadOnlyConfig(ABC):
    def __init__(self, config):
        self.__config = config

    def is_none(self):
        return not bool(len(self.__config))

    def _get_value(self, key):
        return self.__config._get_value(key)

    def dump_dict(self):
        return DictWrapper(self.__config._get_dict())

    def dump_dict_copy(self):
        return deepcopy(self.__config._get_dict())
