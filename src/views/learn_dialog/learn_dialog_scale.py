from gi.repository import Gtk


class LearnDialogScale:
    def __init__(self, data_type=None, values=[]):
        self.scale = Gtk.Scale.new_with_range(Gtk.Orientation.HORIZONTAL, 0, 1, 0.01)
        self.data_type = data_type

    def get(self):
        self.scale.get_value()

    def get_widget(self):
        return self.scale

    def set_default(self, default):
        self.scale.set_value(default)

    def destroy(self):
        self.scale.destroy()
