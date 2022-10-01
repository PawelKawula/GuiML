#!/usr/bin/env python

from abc import ABC, abstractmethod


class MlModel(ABC):
    """Base class for ML models
    """
    @abstractmethod
    def predict(self, xs):
        """Gives us prediction for input
        """
        pass

    @abstractmethod
    def setup_view(view):
        """Returns dict containing widget name, class and kwargs for __init__
        """
        return {}
