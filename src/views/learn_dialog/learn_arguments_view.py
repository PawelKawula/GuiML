from gi.repository import Gtk

from learning.defined_models import learn_models
from .learn_arguments_item import LearnArgumentsItem

class LearnArgumentsView():
    def __init__(self, view, ml_model_name=None):
        self.items = []
        self.view = view
        learn_arguments = learn_models[ml_model_name].setup_view()
        self.ml_model_name = ml_model_name
        for name, widget_info in learn_arguments.items():
            widget_type, widget_kwargs = widget_info
            item = LearnArgumentsItem(name, widget_type, widget_kwargs)
            self.items.append(item)
            self.view.get_content_area().add(item)

    def get_arguments(self):
        res = {arg.name: arg.get_value() for arg in self.items}
        return res

    def destroy(self):
        for item in self.items:
            item.destroy()
