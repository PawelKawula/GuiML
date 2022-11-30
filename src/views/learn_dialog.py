from gi.repository import Gtk
from views import constants, utils
from views.template import Template
from .arguments_view.arguments_view import ArgumentsView
from learning.defined_models import learn_models


@Template(filename=constants.LEARN_DIALOG_FILE)
class LearnDialog(Gtk.Dialog):
    __gtype_name__ = "learn_dialog"
    def __init__(self, parent):
        super().__init__(parent)
        for l in learn_models:
            self.method_combo_box.append_text(l)
        self.method_combo_box.set_active(0)
        self.learn_arguments_view = ArgumentsView(self, self.get_active_model_text())
        self.get_content_area().add(self.learn_arguments_view)
        self.show_all()

    def get_learn_kwargs(self, **kwargs):
        while True:
            response = self.run()
            if response != Gtk.ResponseType.OK:
                return None, None
            learn_kwargs = self.learn_arguments_view.get_arguments()
            if not utils.is_none_in_dict(learn_kwargs):
                break
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
            self.learn_arguments_view.destroy()
            self.learn_arguments_view = ArgumentsView(
                self, self.get_active_model_text()
            )
            self.get_content_area().add(self.learn_arguments_view)
