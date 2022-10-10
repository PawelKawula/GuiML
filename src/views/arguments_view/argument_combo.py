from gi.repository import Gtk


class ArgumentCombo(Gtk.ComboBoxText):
    def __init__(self, data_type=None, values=["None"]):
        super().__init__(halign=Gtk.Align.END, valign=Gtk.Align.CENTER)
        self.data_type = data_type
        self.set_entry_text_column(0)
        for v in values:
            self.append_text(str(v))
        self.enabled_on, self.disabled_on = [], []
        self.connect("changed", self.on_changed)

    def get(self):
        value = self.get_active_text()
        if self.data_type == "float":
            return float(value)
        if self.data_type == "int":
            return int(value)
        return value

    def get_widget(self):
        return self

    def set_default(self, default):
        self.set_active(default)

    def add_enabled_on(self, sensitives):
        self.enabled_on.append(sensitives)

    def add_disabled_on(self, sensitives):
        self.disabled_on.append(sensitives)

    def on_changed(self, combo):
        for sen_item, value in self.enabled_on:
            sen_item.set_widget_sensitive(value == self.get())
        for sen_item, value in self.disabled_on:
            sen_item.set_widget_sensitive(value != self.get())
