from abc import ABC, abstractmethod

import tomli
from gi.repository import Gtk

from views.learn_dialog.learn_dialog_entry import LearnDialogEntry
from views.learn_dialog.learn_dialog_combo import LearnDialogCombo
from views.learn_dialog.learn_dialog_switch import LearnDialogSwitch

class MlModel(ABC):
    """Base class for ML models"""
    @abstractmethod
    def predict(self, xs):
        """Gives us prediction for input"""
        pass

    @staticmethod
    def parse_widget_type(widget_type):
        if widget_type == "entry":
            return LearnDialogEntry
        elif widget_type == "combo":
            return LearnDialogCombo
        elif widget_type == "switch":
            return LearnDialogSwitch
