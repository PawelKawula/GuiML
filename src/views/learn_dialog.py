#!/usr/bin/env python

from gi.repository import Gtk
from views import constants


class LearnDialog(Gtk.Dialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.method_combo_box = Gtk.ComboBoxText()
        self.method_combo_box.set_entry_text_column(0)
        self.method_combo_box.append_text("Deep Learning")
        self.method_combo_box.append_text("Decision Tree")
        self.get_content_area().add(self.method_combo_box)
        self.add_buttons(
            Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OK, Gtk.ResponseType.OK
        )
        self.show_all()

    def get_learn_kwargs(self, **kwargs):
        response = self.run()
        if response == Gtk.ResponseType.CANCEL:
            return None
        learn_kwargs = {"model": self.method_combo_box.get_active_text()}
        self.destroy()
        return learn_kwargs

    def add_method(self, method):
        self.method_combo_box.append(method)
