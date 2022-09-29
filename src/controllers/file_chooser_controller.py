#!/usr/bin/env python

from gi.repository import Gtk


class FileChooserController:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.add_filters()

    def add_filters(self):
        for name, mime_type in self.model.filters.items():
            ffilter = Gtk.FileFilter()
            ffilter.set_name(name)
            ffilter.add_mime_type(mime_type)
            self.view.add_filter(ffilter)

    def get_csv(self):
        response = self.view.run()
        filename = None
        if response == Gtk.ResponseType.OK:
            filename = self.view.get_filename()
            print("File selected: " + filename)
        elif response == Gtk.ResponseType.CANCEL:
            print("Cancel clicked")
            self.view.destroy()
        return filename
