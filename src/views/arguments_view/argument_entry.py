from gi.repository import Gtk


class ArgumentEntry(Gtk.Entry):
    def __init__(self, parent=None, data_type=None, values=None):
        super().__init__(halign=Gtk.Align.END, valign=Gtk.Align.CENTER)
        self.parent = parent
        if self.parent:
            self.connect("changed", self.on_value_changed)
        self.default = None
        self.data_type = data_type
        self.values = values

    def get(self):
        value = self.get_text().lower()
        # TODO: SHOULD IT REALLY RETURN NONE OR SHOULD IT BE SMTH ELSE
        if value == "":
            return None
        if self.data_type == "int":
            return int(value)
        if self.data_type == "float":
            return float(value) if value.find(".") != -1 else int(value)
        return value

    def get_widget(self):
        return self

    def set_default(self, default):
        self.default = default
        self.set_text(str(default))

    def on_value_changed(self, item):
        if self.parent:
            self.parent.on_value_changed(self.get())
