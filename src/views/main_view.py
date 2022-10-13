from gi.repository import Gtk

from views import constants


class MainView:
    def __init__(self, model):
        self.model = model
        self._builder = Gtk.Builder()
        self._builder.add_from_file(constants.GLADE_FILE)

        self.window = self._builder.get_object("window")
        self.window.show()

    def register_listener(self, controller):
        self._builder.connect_signals(controller)
