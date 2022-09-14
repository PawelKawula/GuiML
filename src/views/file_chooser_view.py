#!/usr/bin/env python3


from gi.repository import Gtk
from views import constants


class FileChooser(Gtk.FileChooserDialog):
    def __init__(self, parent):
        super().__init__(
            title="Please choose a file",
            parent=parent,
            action=Gtk.FileChooserAction.OPEN,
        )
        self.add_buttons(
            Gtk.STOCK_CANCEL,
            Gtk.ResponseType.CANCEL,
            Gtk.STOCK_OPEN,
            Gtk.ResponseType.OK,
        )
        self.add_filters()

    def get_csv(self):
        response = self.run()
        if response == Gtk.ResponseType.OK:
            print("Open clicked")
            print("File selected: " + self.get_filename())
        elif response == Gtk.ResponseType.CANCEL:
            print("Cancel clicked")
            self.destroy()
            return

        return self.get_filename()

    def add_filters(self):
        filter_text = Gtk.FileFilter()
        filter_text.set_name("Csv files")
        filter_text.add_mime_type("text/csv")
        self.add_filter(filter_text)

        filter_any = Gtk.FileFilter()
        filter_any.set_name("Any files")
        filter_any.add_pattern("*")
        self.add_filter(filter_any)
