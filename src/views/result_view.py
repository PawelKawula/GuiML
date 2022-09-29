#!/usr/bin/env python3

from gi.repository import Gtk

from views import constants, utils
from controllers import file_handler
from learning.decision_tree import DecisionTreeModel


class ResultView:
    def __init__(self, parent, model):
        self.parent = parent
        self._builder = Gtk.Builder()
        self._builder.add_from_file(constants.RESULT_FILE)
        self._builder.connect_signals(self)

        self.dialog = self._builder.get_object("dialog")
        self.dialog.show()
        self.model = DecisionTreeModel(self.parent.tdf)

        self.populate()

    def on_ok(self, button):
        self.dialog.destroy()

    def populate(self):
        in_values, out_values = file_handler.get_values(
            self.parent.tdf,
            self.parent.ins,
            self.parent.out,
            self.parent.pct,
            self.model,
        )
        input_store, output_store = file_handler.get_stores(
            in_values, out_values, len(self.parent.ins)
        )
        utils.view_trees(
            self._builder, input_store, output_store, self.parent.ins, self.parent.out
        )

    def run(self):
        self.dialog.run()

    def destroy(self):
        self.dialog.destroy()
