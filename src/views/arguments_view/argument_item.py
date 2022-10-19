from gi.repository import Gtk

from views.constants import MARGINS
from .argument_entry import ArgumentEntry
from .argument_combo import ArgumentCombo


class ArgumentItem(Gtk.Box):
    def __init__(self, label, widget_type, data_type, values):
        super().__init__(**MARGINS)
        self.name = label
        self.values = values
        self.label = Gtk.Label(
            label=label, halign=Gtk.Align.START, valign=Gtk.Align.CENTER
        )
        self.pack_start(self.label, False, False, 0)
        # self.attach(self.label, 0, 0, 1, 1)
        self.type_widget = None
        self.learn_widget = widget_type(data_type, values)
        self.argument_grid = Gtk.Grid(halign=Gtk.Align.END)
        self.pack_end(self.argument_grid, True, True, 0)
        if data_type == "mixed":
            self.type_widget = Gtk.ComboBoxText()
            self.type_widget.set_entry_text_column(0)
            for t in ["str", "float", "int"]:
                self.type_widget.append_text(t)
            self.type_widget.connect("changed", self.on_type_widget_changed)
            self.argument_grid.attach(self.type_widget, 1, 0, 3, 1)
        # self.pack_end(self.learn_widget.get_widget(), False, False, 0)
        self.argument_grid.attach(self.learn_widget.get_widget(), 4, 0, 9, 1)
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
        self.can_none_check_button = Gtk.CheckButton()
        self.argument_grid.attach(self.can_none_check_button, 0, 0, 1, 1)

    def on_type_widget_changed(self, item):
        print("changed")
        choosen_type = self.type_widget.get_active_text()
        self.learn_widget.destroy()
        if choosen_type == "str":
            print("str")
            self.learn_widget = ArgumentCombo("str", self.values)
        else:
            self.learn_widget = ArgumentEntry(choosen_type)
        self.argument_grid.attach(self.learn_widget.get_widget(), 4, 0, 9, 1)
        self.argument_grid.show_all()
