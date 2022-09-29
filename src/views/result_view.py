#!/usr/bin/env python3

from gi.repository import Gtk

from views import constants, utils
from controllers import file_handler
from learning.decision_tree import DecisionTreeModel


class ResultView:
    def __init__(self, parent, main_model, **kwargs):
        self.parent = parent
        self.main_model = main_model
        self._builder = Gtk.Builder()
        self._builder.add_from_file(constants.RESULT_FILE)
        self._builder.connect_signals(self)

        self.dialog = self._builder.get_object("dialog")
        self.dialog.show()
        self.model = DecisionTreeModel(self.main_model.tdf)

        self.populate()

    def on_ok(self, button):
        self.dialog.destroy()

    def populate(self):
        split_kwargs = self.main_model.split_kwargs
        tdf = file_handler.get_values(
            self.main_model.tdf, valid=True, model=self.model, **split_kwargs
        )
        store = file_handler.get_store(tdf, valid=True, **split_kwargs)
        print(len(store))
        utils.view_trees(self._builder, store, **split_kwargs)
        print("VIEW TREES")

    def run(self):
        self.dialog.run()

    def destroy(self):
        self.dialog.destroy()
