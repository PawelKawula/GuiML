#!/usr/bin/env python3

from gi.repository import Gtk

from views import constants, utils
from controllers import file_handler
from learning.decision_tree import DecisionTreeModel


class ResultView:
    def __init__(self, parent, main_model, ml_model, **kwargs):
        self.parent = parent
        self.main_model = main_model
        self._builder = Gtk.Builder()
        self._builder.add_from_file(constants.RESULT_FILE)
        self._builder.connect_signals(self)

        self.dialog = self._builder.get_object("dialog")
        self.dialog.show()
        self.ml_model = ml_model(self.main_model.tdf, **kwargs)

        self.populate()

    def on_ok(self, button):
        self.dialog.destroy()

    def populate(self):
        split_kwargs = self.main_model.split_kwargs
        tdf = file_handler.get_values(
            self.main_model.tdf, valid=True, ml_model=self.ml_model, **split_kwargs
        )
        store = file_handler.get_store(tdf, valid=True, **split_kwargs)
        utils.view_trees(self._builder, store, **split_kwargs)

    def run(self):
        self.dialog.run()

    def destroy(self):
        self.dialog.destroy()
