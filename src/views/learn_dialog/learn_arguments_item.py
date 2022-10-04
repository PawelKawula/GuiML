#!/usr/bin/env python

from gi.repository import Gtk

from .learn_dialog_entry import LearnDialogEntry
from .learn_dialog_combo import LearnDialogCombo


class LearnArgumentsItem(Gtk.Paned):
    def __init__(self, label, widget_type, data_type, values):
        super().__init__()
        self.name = label
        self.label = Gtk.Label(
            label=label, halign=Gtk.Align.START, valign=Gtk.Align.CENTER
        )
        self.add1(self.label)
        self.learn_widget = widget_type(data_type, values)
        self.add2(self.learn_widget.get_widget())

    def get_value(self):
        return self.learn_widget.get()

    def set_default(self, default):
        self.learn_widget.set_default(default)
