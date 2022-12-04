from gi.repository import Gtk

from . import constants


class FileChooserView(Gtk.FileChooserDialog):
    def __init__(
        self, parent, filters={"Csv files": "text/csv", "Any files": "*"}
    ):
        super().__init__(
            title="Please choose a file",
            parent=parent,
            action=Gtk.FileChooserAction.OPEN,
        )
        self.filters = filters
        self.add_buttons(
            Gtk.STOCK_CANCEL,
            Gtk.ResponseType.CANCEL,
            Gtk.STOCK_OPEN,
            Gtk.ResponseType.OK,
        )
        self.add_filters()

    def add_filters(self):
        for name, mime_type in self.filters.items():
            ffilter = Gtk.FileFilter()
            ffilter.set_name(name)
            ffilter.add_mime_type(mime_type)
            self.add_filter(ffilter)

    def get_csv(self):
        response = self.run()
        filename = None
        if response == int(Gtk.ResponseType.OK):
            filename = self.get_filename()
        self.destroy()
        return filename
