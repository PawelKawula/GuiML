from gi.repository import Gtk

from views.constants import MARGINS
from .argument_entry import ArgumentEntry
from .argument_combo import ArgumentCombo


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
        self.can_none_check_button = None

    def get_value(self):
        return (
            self.learn_widget.get()
            if not self.can_none_check_button
            or not self.can_none_check_button.get_active()
            else None
        )

    def get_widget_sensitive(self):
        return self.learn_widget.get_sensitive()

    def set_widget_sensitive(self, sensitive):
        self.learn_widget.set_sensitive(sensitive)

    def set_default(self, default):
        if not self.can_none_check_button or str(default).lower() != "none":
            self.learn_widget.set_default(default)

    def add_enabled_on(self, enabled_on):
        self.learn_widget.add_enabled_on(enabled_on)

    def add_disabled_on(self, disabled_on):
        self.learn_widget.add_disabled_on(disabled_on)

    def add_visible_on(self, visible_on):
        self.learn_widget.add_visible_on(visible_on)

    def add_invisible_on(self, invisible_on):
        self.learn_widget.add_invisible_on(invisible_on)

    def set_widget_visible(self, visible):
        self.set_visible(visible)

    def add_none_tickbox(self):
        print("ADDED")
        self.can_none_check_button = Gtk.CheckButton()
        self.pack_end(self.can_none_check_button, False, False, 0)
