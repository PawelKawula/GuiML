#!/usr/bin/env python

from abc import abstractmethod

from gi.repository import Gtk


class LearnDialogEntry(Gtk.Entry):
    def __init__(self, data_type=None, values=None):
        super().__init__(halign=Gtk.Align.END, valign=Gtk.Align.CENTER)
        self.data_type = data_type

    def get(self):
        text = self.get_text()
        if self.data_type == "int":
            return int(text)
        if self.data_type == "float":
            return float(text)
        return text
