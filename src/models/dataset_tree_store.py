#!/usr/bin/env python

from gi.repository import Gtk


class DatasetTreeStore(Gtk.TreeStore):
    def __init__(self, valid, *columns):
        super().__init__(*columns)
        empty_strs = (len(columns) - 1) * [""]
        self.valid = valid
        if not valid:
            super().append(None, ["Training"] + empty_strs)
            super().append(None, ["Validation"] + empty_strs)
            self.training_iter = self.get_iter(Gtk.TreePath([0]))
            self.validation_iter = self.get_iter(Gtk.TreePath([1]))

    def append_training(self, values):
        assert not self.valid
        for row in values:
            super().append(self.training_iter, row)

    def append_validation(self, values):
        assert not self.valid
        for row in values:
            super().append(self.validation_iter, row)

    def append_results(self, values):
        assert self.valid
        for row in values:
            super().append(None, row)
