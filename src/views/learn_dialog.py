from gi.repository import Gtk
from views import constants, utils
from .arguments_view.arguments_view import ArgumentsView
from learning.defined_models import learn_models


class LearnDialog(Gtk.Dialog):
    def __init__(self, parent, main_model):
        super().__init__(parent)
        self.method_combo_box = Gtk.ComboBoxText(
            margin_left=20, margin_right=20, margin_top=10, margin_bottom=10
        )
        self.method_combo_box.connect("changed", self.on_method_combo_changed)
        self.method_combo_box.set_entry_text_column(0)
        for l in learn_models:
            self.method_combo_box.append_text(l)
        self.method_combo_box.set_active(0)
        self.get_content_area().add(self.method_combo_box)
        self.learn_arguments_view = ArgumentsView(
            self, self.get_active_model_text()
        )

        self.add_buttons(
            Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OK, Gtk.ResponseType.OK
        )
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