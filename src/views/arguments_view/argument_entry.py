from gi.repository import Gtk


class ArgumentEntry(Gtk.Entry):
    def __init__(self, data_type=None, values=None):
        super().__init__(halign=Gtk.Align.END, valign=Gtk.Align.CENTER)
        self.data_type = data_type

    def get(self):
        text = self.get_text()
        if self.data_type == "int":
            return int(text)
        if self.data_type == "float":
            return float(text)
        return text

    def get_widget(self):
        return self

    def set_default(self, default):
        self.set_text(str(default))
