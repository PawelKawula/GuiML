from gi.repository import Gtk

from . import constants
from .template import Template
from .arguments_view.arguments_view import ArgumentsView
from common.configs.global_ml_config import ReadOnlyGlobalMlConfig


class ResultAddView(Gtk.Dialog):
    def __init__(self, parent, ml_config, splits_config):
        super().__init__(parent=parent, transient_for=parent, flags=0)
        self.set_default_size(800, 600)
        self.args_view = ArgumentsView(ml_config, splits_config)
        self.get_content_area().add(self.args_view)
        self.add_buttons(
            Gtk.STOCK_CANCEL,
            Gtk.ResponseType.CANCEL,
            Gtk.STOCK_OK,
            Gtk.ResponseType.OK,
        )

    def get_item(self):
        response = self.run()
        if response != int(Gtk.ResponseType.OK):
            return None
        return self.args_view.get_values()
