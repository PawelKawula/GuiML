#!/usr/bin/env python

from gi.repository import Gtk

from .learn_dialog_entry import LearnDialogEntry


class LearnArgumentsItem(Gtk.Paned):
    def __init__(self, label, widget_type, widget_kwargs):
        super().__init__()
        self.name = label
        self.label = Gtk.Label(label=label, halign=Gtk.Align.START, valign=Gtk.Align.CENTER)
        self.add1(self.label)
        self.learn_widget = widget_type(**widget_kwargs, halign=Gtk.Align.END, valign=Gtk.Align.CENTER)
        self.add2(self.learn_widget)

    def get_value(self):
        if isinstance(self.learn_widget, Gtk.ComboBoxText):
            return self.learn_widget.get_active_text()
        if isinstance(self.learn_widget, Gtk.Switch) or isinstance(
            self.learn_widget, Gtk.ToggleButton
        ):
            return self.learn_widget.get_active()
        if isinstance(self.learn_widget, LearnDialogEntry):
            return self.learn_widget.get()
