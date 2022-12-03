import numpy as np
from gi.repository import Gtk

from .argument_combo import ArgumentCombo
from .argument_entry import ArgumentEntry
from .argument_switch import ArgumentSwitch
from .argument_scale import ArgumentScale
from .argument_calendar import ArgumentCalendar

class ArgumentsView(Gtk.VBox):
    def __init__(self, parent, **values):
        super().__init__()
        self.args = {}
        for v in values:
            self.args[v] = arg_widget_for_type(v)

    def get_values(self):
        return { w: w.get_value() for w in self.args }

def arg_widget_for_value(parent, v, values=["None"]):
    # astype(object)
    if np.issubdtype(v, np.number):
        return ArgumentEntry(parent, "int" if np.issubtype(v, np.integer) else "float")
    if np.issubdtype(v, np._bool):
        return ArgumentSwitch(parent)
    if np.issubdtype(v, np.character):
        return ArgumentCombo(parent, "str", values)
    if isinstance(v, pd.DatetimeIndex) or isinstance(v, pd.DatetimeTZDtype):
        return
