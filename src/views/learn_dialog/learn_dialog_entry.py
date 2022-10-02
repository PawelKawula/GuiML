#!/usr/bin/env python

from abc import abstractmethod

from gi.repository import Gtk


class LearnDialogEntry(Gtk.Entry):
    entry_types = [float, int]

    def __init__(self, text, entry_type):
        super().__init__()
        self.set_text(text)
        self.entry_type = entry_type
        assert (
            type(entry_type) in LearnDialogEntry.entry_types
        ), "Incorrect value type for widget!"

    def get(self):
        if self.entry_type is int:
            return int(self.get_text())
        if self.entry_type is float:
            return float(self.get_text())
