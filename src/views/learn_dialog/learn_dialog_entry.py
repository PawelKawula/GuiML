#!/usr/bin/env python

from abc import abstractmethod

from gi.repository import Gtk


class LearnDialogEntry(Gtk.Entry):
    def __init__(self, text, entry_type, halign=Gtk.Align.END, valign=Gtk.Align.CENTER):
        super().__init__(halign=halign, valign=valign)
        self.set_text(text)
        self.entry_type = entry_type

    def get(self):
        if self.entry_type is int:
            return int(self.get_text())
        if self.entry_type is float:
            return float(self.get_text())
