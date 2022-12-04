from gi.repository import Gtk

from . import constants, utils
from .template import Template
from .arguments_view.ml_arguments_view import MlArgumentsView
from learning.defined_models import learn_models


@Template(filename=constants.LEARN_DIALOG_FILE)
class LearnDialog(Gtk.Dialog):
    __gtype_name__ = "learn_dialog"

    def __init__(self, parent):
        super().__init__(parent=parent, transient_for=parent, flags=0)
        for l in learn_models:
            self.method_combo_box.append_text(l)
        self.method_combo_box.set_active(0)
        self.learn_arguments_view = MlArgumentsView(
            self, self.get_active_model_text()
        )
        self.box.pack_start(self.learn_arguments_view, True, True, 0)
        self.arg_views = {}
        self.add_buttons(
            Gtk.STOCK_CANCEL,
            Gtk.ResponseType.CANCEL,
            Gtk.STOCK_OK,
            Gtk.ResponseType.OK,
        )
        # self.show_all()

    def get_learn_kwargs(self, **kwargs):
        response = self.run()
        if response != int(Gtk.ResponseType.OK):
            self.destroy()
            return None, None
        learn_kwargs = self.learn_arguments_view.get_arguments()
        ml_model = self.get_active_model()
        self.destroy()
        return ml_model, learn_kwargs

    @Gtk.Template.Callback()
    def on_method_combo_changed(self, combo):
        self.reset_view()
        self.show_all()

    def get_active_model(self):
        return learn_models[self.method_combo_box.get_active_text()]

    def get_active_model_text(self):
        return self.method_combo_box.get_active_text()

    def reset_view(self):
        if hasattr(self, "learn_arguments_view"):
            active_model_text = self.get_active_model_text()
            # self.learn_arguments_view.destroy()
            self.box.remove(self.learn_arguments_view)
            if active_model_text in self.arg_views:
                self.learn_arguments_view = self.arg_views[active_model_text]
            else:
                self.learn_arguments_view = ArgumentsView(
                    self, self.get_active_model_text()
                )
            self.box.pack_start(self.learn_arguments_view, True, True, 0)
            self.resize(1, 1)
