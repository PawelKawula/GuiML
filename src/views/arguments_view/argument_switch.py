#!/usr/bin/env python

from gi.repository import Gtk


class ArgumentSwitch(Gtk.Switch):
    def __init__(self, data_type, values):
        super().__init__(expand=False)

    def get(self):
        return self.get_active()

    def get_widget(self):
        return self

    def set_default(self, default):
        self.set_active(default)
