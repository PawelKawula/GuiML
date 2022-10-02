#!/usr/bin/env python

from gi.repository import Gtk
from views import constants
from .learn_arguments_view import LearnArgumentsView
from learning.defined_models import learn_models


class LearnDialog(Gtk.Dialog):
    def __init__(self, parent, main_model):
        super().__init__(parent)
        self.method_combo_box = Gtk.ComboBoxText()
        self.method_combo_box.connect("changed", self.on_method_combo_changed)
        self.method_combo_box.set_entry_text_column(0)
        for l in learn_models:
            self.method_combo_box.append_text(l)
        self.get_content_area().add(self.method_combo_box)

        self.add_buttons(
            Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OK, Gtk.ResponseType.OK
        )
        self.learn_arguments_view = LearnArgumentsView(self)
        self.show_all()

    def get_learn_kwargs(self, **kwargs):
        response = self.run()
        if response == Gtk.ResponseType.CANCEL:
            return None
        learn_kwargs = self.learn_arguments_view.get_arguments()
        self.destroy()
        return learn_kwargs

    def on_method_combo_changed(self, combo):
        self.reset_view()
        self.show_all()

    """
    def update_view(self, learn_args):
        for name, value in learn_args.items():
            widget, widget_kwargs = value
            box = Gtk.Box(spacing=6)
            box.pack_start(Gtk.Label(name), True, True, 0)
            box.pack_start(widget(**widget_kwargs), True, True, 0)
            self.learn_widgets.append(box)
            self.get_content_area().add(box)
        self.show_all()
    """

    """
    def reset_view(self):
        for child in self.learn_widgets:
            self.get_content_area().remove(child)
    """

    def get_active_model(self):
        return learn_models[self.method_combo_box.get_active_text()]

    def get_active_model_text(self):
        return self.method_combo_box.get_active_text()

    def reset_view(self):
        #self.learn_arguments_view.reset()
        self.learn_arguments_view.destroy()
        self.learn_arguments_view = LearnArgumentsView(self, self.get_active_model_text())
