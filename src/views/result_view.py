from gi.repository import Gtk
import pandas as pd

from . import constants, utils
from .result_add_view import ResultAddView
from .template import Template
from common import file_handler


@Template(filename=constants.RESULT_FILE)
class ResultView(Gtk.Dialog):
    __gtype_name__ = "result_dialog"

    def __init__(self, parent, ml_model, **learn_kwargs):
        super().__init__()
        self.parent = parent
        self.__initialize_configs()
        self.tdf = self.ml_config.get_tdf().new_empty()
        self.ml_model = ml_model(self.ml_config.get_tdf(), **learn_kwargs)
        self.populate()
        self.show()

    def __initialize_configs(self):
        self.ml_config = self.parent.get_ml_config()
        self.splits_config = self.parent.get_splits_config()

    @Gtk.Template.Callback()
    def on_ok_clicked(self, item):
        self.destroy()

    @Gtk.Template.Callback()
    def on_add_clicked(self, item):
        result_add = ResultAddView(self, self.ml_config, self.splits_config)
        item = result_add.get_item()
        series = {c: v for c, v in zip(self.splits_config.get_ins(), item)}
        self.tdf.items = self.tdf.items.append(series, ignore_index=True)
        self.tdf.process()
        prediction = self.ml_model.predict(
            self.tdf.xs.iloc[-1].array.reshape(1, -1)
        )
        self.store.append_added(item + [prediction.item()])
        result_add.destroy()

    def populate(self):
        tdf, split_kwargs = (
            self.ml_config.get_tdf(),
            self.splits_config.dump_dict_copy(),
        )
        tdf = file_handler.get_values(
            tdf, valid=True, ml_model=self.ml_model, **split_kwargs
        )
        self.store = file_handler.get_store(tdf, valid=True)
        utils.view_trees(
            self.items_view, self.store, expanded=True, **split_kwargs
        )
