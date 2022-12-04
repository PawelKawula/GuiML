from gi.repository import Gtk

from views.constants import MARGINS
from .argument_entry import ArgumentEntry
from .argument_combo import ArgumentCombo


class ArgumentItem(Gtk.Box):
    def __init__(
        self,
        name,
        widget_type,
        data_type,
        values,
        parent=None,
        method=None,
        propagate_change_to_parent=False,
    ):
        super().__init__(**MARGINS)
        self.propagate_change_to_parent = propagate_change_to_parent
        self.parent, self.method = parent, method
        self.name, self.values = name, values
        self.label = Gtk.Label(
            label=name, halign=Gtk.Align.START, valign=Gtk.Align.CENTER
        )
        self.pack_start(self.label, False, False, 0)
        self.type_widget = None
        self.widget_type = widget_type
        self.learn_widget = widget_type(
            self if parent else None, data_type, values
        )
        self.argument_grid = Gtk.Grid(halign=Gtk.Align.END)
        self.pack_end(self.argument_grid, True, True, 0)
        self.data_type = data_type
        if data_type == "mixed":
            self.type_widget = Gtk.ComboBoxText()
            self.type_widget.set_entry_text_column(0)
            for t in ["str", "float", "int"]:
                self.type_widget.append_text(t)
            self.type_widget.connect("changed", self.on_type_widget_changed)
            self.argument_grid.attach(self.type_widget, 1, 0, 3, 1)
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
        self.default = default
        if self.data_type == "mixed":
            if isinstance(default, str):
                self.type_widget.set_active(0)
            if isinstance(default, float):
                self.type_widget.set_active(1)
            if isinstance(default, int):
                self.type_widget.set_active(2)
        if str(default).lower() != "none":
            self.learn_widget.set_default(default)
        elif self.can_none_check_button:
            self.can_none_check_button.set_active(True)

    def get_default(self):
        if self.data_type == "mixed":
            return self.default
        return self.learn_widget.get_default()

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
        self.can_none_check_button.connect(
            "toggled", self.on_can_none_tickbox_toggled
        )
        self.argument_grid.attach(self.can_none_check_button, 0, 0, 1, 1)

    def on_can_none_tickbox_toggled(self, item):
        sensitive = not self.can_none_check_button.get_active()
        self.learn_widget.set_sensitive(sensitive)
        if self.type_widget:
            self.type_widget.set_sensitive(sensitive)
        self.on_value_changed()

    # TODO: on_value_changed for mixed type
    def on_type_widget_changed(self, item):
        choosen_type = self.type_widget.get_active_text()
        self.learn_widget.destroy()
        parent = self if self.parent else None
        if choosen_type == "str":
            self.learn_widget = ArgumentCombo(parent, "str", self.values)
            if isinstance(self.default, str):
                self.learn_widget.set_default(self.default)
        else:
            self.learn_widget = ArgumentEntry(parent, choosen_type)
            if choosen_type == "float" and isinstance(self.default, float):
                self.learn_widget.set_default(self.default)
            if choosen_type == "int" and isinstance(self.default, int):
                self.learn_widget.set_default(self.default)
        self.argument_grid.attach(self.learn_widget.get_widget(), 4, 0, 9, 1)
        self.on_value_changed()

    def on_value_changed(self):
        value = self.get_value()
        label = f"* {self.name}" if self.get_default() != value else self.name
        if not self.propagate_change_to_parent:
            return
        self.label.set_label(label)
        self.parent.on_value_changed(self.method, value)

    def get_default(self):
        return self.learn_widget.get_default()

    def set_saved(self):
        self.label.set_label(self.name)

    def set_changed(self):
        self.label.set_label(f"* {self.name}")
