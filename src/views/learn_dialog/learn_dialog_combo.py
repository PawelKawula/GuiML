from gi.repository import Gtk

class LearnDialogCombo(Gtk.ComboBoxText):
    def __init__(self, entry_type=str, halign=Gtk.Align.END, valign=Gtk.Align.CENTER, values=[]):
        super().__init__(halign=halign, valign=valign)
        self.entry_type = entry_type
        self.set_entry_text_column(0)
        for v in values:
            self.append_text(str(v))

    def get(self):
        value = self.get_active_text()
        if self.entry_type is str:
            return value
        if self.entry_type is int:
            return int(value)
