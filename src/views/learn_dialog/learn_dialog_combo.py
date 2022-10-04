from gi.repository import Gtk


class LearnDialogCombo(Gtk.ComboBoxText):
    def __init__(self, data_type=None, values=["None"]):
        super().__init__(halign=Gtk.Align.END, valign=Gtk.Align.CENTER)
        self.data_type = data_type
        self.set_entry_text_column(0)
        for v in values:
            self.append_text(str(v))

    def get(self):
        value = self.get_active_text()
        if self.data_type == "float":
            return float(value)
        if self.data_type == "int":
            return int(value)
        return value
