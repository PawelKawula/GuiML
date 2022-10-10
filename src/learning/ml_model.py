from abc import ABC, abstractmethod

import tomli
from gi.repository import Gtk

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
    def parse_widget_type(widget_type):
        if widget_type == "entry":
            return ArgumentEntry
        elif widget_type == "combo":
            return ArgumentCombo
        elif widget_type == "switch":
            return ArgumentSwitch
        elif widget_type == "scale":
            return ArgumentScale
