import numpy as np
import pandas as pd
from gi.repository import Gtk

from learning.ml_model import MlModel
from .argument_combo import ArgumentCombo
from .argument_entry import ArgumentEntry
from .argument_switch import ArgumentSwitch
from .argument_scale import ArgumentScale
from .argument_calendar import ArgumentCalendar
from .argument_item import ArgumentItem


class ArgumentsView(Gtk.ScrolledWindow):
    def __init__(self, ml_config, splits_config):
        super().__init__(expand=True)
        self.box = Gtk.VBox()
        self.add(self.box)
        self.ml_config, self.splits_config, self.args = (
            ml_config,
            splits_config,
            {},
        )
        for col in splits_config.get_ins():
            self.args[col] = arg_widget_for_col(ml_config, col)
            print(self.args[col])
            self.box.pack_start(self.args[col], True, True, 0)
        self.show_all()

    def get_values(self):
        return [v.get_value() for v in self.args.values()]


def arg_widget_for_col(ml_config, col):
    is_cat = ml_config.is_column_categorical(col)
    categories = ["None"]
    value = ml_config.get_item_from_tdf(0, col)
    if is_cat:
        categories = ml_config.get_column_categories(col)
    data_type = get_data_type_for_pandas_value(value)
    widget_type = get_widget_for_type(value, data_type, is_cat)
    widget_type = MlModel.parse_widget_type(widget_type)
    return ArgumentItem(col, widget_type, data_type, categories)


def get_widget_for_type(value, data_type, is_cat):
    if data_type == "bool":
        return "switch"
    return "combo" if is_cat else "entry"


def get_data_type_for_pandas_value(value):
    print(type(value))
    if isinstance(value, str):
        return "str"
    if isinstance(value, bool):
        return "bool"
    if np.issubdtype(value, np.number):
        return "int" if np.issubdtype(value, np.integer) else "float"
    if isinstance(value, (pd.DatetimeIndex, pd.DatetimeTZDtype)):
        return "datetime"
    print("nuthin")
