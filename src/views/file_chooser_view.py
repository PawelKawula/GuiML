from gi.repository import Gtk
from views import constants


class FileChooserView(Gtk.FileChooserDialog):
    def __init__(self, parent, model):
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
