import logging
from inspect import getframeinfo, stack

from .none_val import NoneVal


class ProgramArgumentsMeta(type):
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class ProgramArguments(metaclass=ProgramArgumentsMeta):
    def __init__(self, **kwargs):
        self.__arguments = kwargs

    def get_argument(self, key):
        if key in self.__arguments:
            return self.__arguments[key]
        caller = getframeinfo(stack()[1][0])
        logging.warning(
            'Tried to get nonexistent argument "%s" in %s:%s'
            % (key, caller.filename, caller.lineno)
        )
        return NoneVal
