from gi.repository import Gtk


class ArgumentSwitch(Gtk.Switch):
    def __init__(self, parent=None, data_type="bool", values=None):
        super().__init__(expand=False)
        self.default = None
        self.parent = parent
        if self.parent:
            self.connect("state-set", self.on_value_changed)
        self.data_type = data_type

    def get(self):
        return self.get_active()

    def get_widget(self):
        return self

    def set_default(self, default):
        self.default = default
        self.set_active(default)

    def on_value_changed(self, item, item2):
        if self.parent:
            self.parent.on_value_changed(self.get())
