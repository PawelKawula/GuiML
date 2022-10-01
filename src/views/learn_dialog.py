#!/usr/bin/env python

from gi.repository import Gtk
from views import constants
from learning.decision_tree import DecisionTreeModel
from learning.deep_learning import DeepLearningModel
from learning.gradient_boosting_model import GradientBoostingModel


class LearnDialog(Gtk.Dialog):
    learn_models = {
        "Decision Tree": DecisionTreeModel,
        "Deep Learning": DeepLearningModel,
        "Gradient Boosting": GradientBoostingModel
    }

    def __init__(self, parent, main_model):
        super().__init__(parent)
        self.method_combo_box = Gtk.ComboBoxText()
        self.method_combo_box.connect("changed", self.on_method_combo_changed)
        self.method_combo_box.set_entry_text_column(0)
        for l in LearnDialog.learn_models:
            self.method_combo_box.append_text(l)
        self.get_content_area().add(self.method_combo_box)

        self.add_buttons(
            Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OK, Gtk.ResponseType.OK
        )
        self.learn_kwargs = dict()
        self.learn_widgets = []
        self.show_all()

    def get_learn_kwargs(self, **kwargs):
        response = self.run()
        if response == Gtk.ResponseType.CANCEL:
            return None
        self.destroy()
        return self.learn_kwargs

    def on_method_combo_changed(self, combo):
        self.learn_kwargs.clear()
        model_class = LearnDialog.learn_models[self.method_combo_box.get_active_text()]
        self.reset_view()
        learn_args = model_class.setup_view(self)
        self.update_view(learn_args)
        self.learn_kwargs = {"ml_model": model_class}
        self.learn_kwargs.update(learn_args)
        self.show_all()

    def update_view(self, learn_args):
        for name, value in learn_args.items():
            widget, widget_kwargs = value
            box = Gtk.Box(spacing=6)
            box.pack_start(Gtk.Label(name), True, True, 0)
            box.pack_start(widget(**widget_kwargs), True, True, 0)
            self.learn_widgets.append(box)
            self.get_content_area().add(box)
        self.show_all()

    def reset_view(self):
        for child in self.learn_widgets:
            self.get_content_area().remove(child)
