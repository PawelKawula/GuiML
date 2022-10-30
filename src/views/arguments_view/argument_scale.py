from gi.repository import Gtk


class ArgumentScale:
    def __init__(self, parent=None, data_type=None, values=None):
        self.default = None
        values = [0, 1, 0.01] if values is None else values
        assert len(values) == 3, "values for scale must contain 3 numbers!"
        self.scale = Gtk.Scale.new_with_range(Gtk.Orientation.HORIZONTAL, *values)
        self.parent = parent
        if self.parent:
            self.scale.connect("value-changed", self.on_value_changed)
        self.data_type = data_type

    def get(self):
        value = self.scale.get_value()
        return int(value) if self.data_type == "int" else value

    def get_widget(self):
        return self.scale

    def set_default(self, default):
        self.default = default
        self.scale.set_value(default)

    def get_sensitive(self):
        return self.scale.get_sensitive()

    def set_sensitive(self, sensitive):
        self.scale.set_sensitive(sensitive)

    def destroy(self):
        self.scale.destroy()

    def on_value_changed(self, item):
        if self.parent:
            self.parent.on_value_changed()

    def get_default(self):
        return self.default
