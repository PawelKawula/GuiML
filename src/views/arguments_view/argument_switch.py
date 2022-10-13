#!/usr/bin/env python

from gi.repository import Gtk


class ArgumentSwitch(Gtk.Switch):
    def __init__(self, data_type="bool", values=None):
        super().__init__(expand=False)
        self.data_type = data_type

    def get(self):
        return self.get_active()

    def get_widget(self):
        return self

    def set_default(self, default):
        self.set_active(default)
