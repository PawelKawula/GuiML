#!/usr/bin/env python

from gi.repository import Gtk


class DatasetTreeStore(Gtk.TreeStore):
    def __init__(self, *columns):
        super().__init__(*columns)
        empty_strs = (len(columns) - 1) * [""]
        self.append(None, ["Training"] + empty_strs)
        self.append(None, ["Validation"] + empty_strs)
        self.training_iter = self.get_iter(Gtk.TreePath([0]))
        self.validation_iter = self.get_iter(Gtk.TreePath([1]))

    def append_training(self, values):
        print(values[0])
        for row in values:
            self.append(self.training_iter, row)

    def append_validation(self, values):
        for row in values:
            self.append(self.validation_iter, row)
