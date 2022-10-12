#!/usr/bin/env python

from gi.repository import Gtk

from .argument_entry import ArgumentEntry
from .argument_combo import ArgumentCombo
from views.constants import MARGINS


class ArgumentItem(Gtk.Box):
    def __init__(self, label, widget_type, data_type, values):
        super().__init__(**MARGINS)
        self.name = label
        self.label = Gtk.Label(
            label=label, halign=Gtk.Align.START, valign=Gtk.Align.CENTER
        )
        self.pack_start(self.label, False, False, 0)
        self.learn_widget = widget_type(data_type, values)
        self.pack_end(self.learn_widget.get_widget(), False, False, 0)

    def get_value(self):
        return self.learn_widget.get()

    def get_sensitive(self):
        return self.learn_widget.get_sensitive()

    def set_widget_sensitive(self, sensitive):
        self.learn_widget.set_sensitive(sensitive)

    def set_default(self, default):
        self.learn_widget.set_default(default)

    def get_widget_sensitive(self):
        return self.learn_widget.get_sensitive()

    def add_enabled_on(self, enabled_on):
        self.learn_widget.add_enabled_on(enabled_on)

    def add_visible_on(self, visible_on):
        self.learn_widget.add_visible_on(visible_on)

    def set_widget_visible(self, visible):
        self.set_visible(visible)
