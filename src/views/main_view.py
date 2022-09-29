#!/usr/bin/env python3

from gi.repository import Gtk

from views import constants
from controllers import file_handler
from controllers.main_controller import MainController


class MainView:
    def __init__(self, model):
        self.model = model
        self._builder = Gtk.Builder()
        self._builder.add_from_file(constants.GLADE_FILE)

        self.window = self._builder.get_object("window")
        self.window.show()

    def register_listener(self, controller):
        self._builder.connect_signals(controller)
