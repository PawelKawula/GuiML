from collections.abc import Sequence

from gi.repository import Gtk


class ArgumentCombo(Gtk.ComboBoxText):
    def __init__(self, parent=None, data_type=None, values=["None"]):
        super().__init__(halign=Gtk.Align.END, valign=Gtk.Align.CENTER)
        self.default = None
        self.parent = parent
        if self.parent:
            self.connect("changed", self.on_value_changed)
        self.data_type = data_type
        self.set_entry_text_column(0)
        self.values = values
        for v in values:
            self.append_text(str(v))
        self.invisible_on, self.visible_on = [], []
        self.enabled_on, self.disabled_on = [], []

        self.connect("changed", self.on_changed)

    def get(self):
        value = self.get_active_text()
        if not value:
            return None
        if self.data_type == "float":
            return float(value)
        if self.data_type == "int":
            return int(value)
        return value

    def get_widget(self):
        return self

    def set_default(self, default):
        self.default = self.values[default] if isinstance(default, int) else default
        self.set_active(default)

    def add_enabled_on(self, sensitives):
        self.enabled_on.append(sensitives)

    def add_disabled_on(self, sensitives):
        self.disabled_on.append(sensitives)

    def add_visible_on(self, sensitives):
        self.visible_on.append(sensitives)

    def add_invisible_on(self, sensitives):
        self.invisible_on.append(sensitives)

    def on_changed(self, combo):
        for sen_item, value in self.enabled_on:
            condition = (
                self.get() in value
                if isinstance(value, Sequence)
                else value == self.get()
            )
            sen_item.set_widget_sensitive(condition)
        for sen_item, value in self.disabled_on:
            condition = (
                self.get() not in value
                if isinstance(value, Sequence)
                else value != self.get()
            )
            sen_item.set_widget_sensitive(condition)
        for sen_item, value in self.visible_on:
            condition = (
                self.get() in value
                if isinstance(value, Sequence)
                else value == self.get()
            )
            sen_item.set_widget_visible(condition)
        for sen_item, value in self.invisible_on:
            condition = (
                self.get() not in value
                if isinstance(value, Sequence)
                else value != self.get()
            )
            sen_item.set_widget_visible(condition)

    def on_value_changed(self, item):
        if self.parent:
            self.parent.on_value_changed(self.get())
