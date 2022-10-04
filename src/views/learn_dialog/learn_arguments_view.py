from gi.repository import Gtk

from learning.defined_models import learn_models
from .learn_arguments_item import LearnArgumentsItem
from learning.ml_model import MlModel


class LearnArgumentsView:
    def __init__(self, view, ml_model_name=None):
        self.items, self.expanders, self.vboxes = [], [], []
        self.method_args = {}
        self.view = view
        learn_arguments = learn_models[ml_model_name].parse_options("learning")
        self.ml_model_name = ml_model_name
        for method, arguments in learn_arguments.items():
            expander, vbox = Gtk.Expander(label=method), Gtk.VBox()
            self.method_args[method] = {}
            for name, widget_info in arguments.items():
                self.add_item(vbox, method, name, widget_info)
            self.view.get_content_area().add(expander)
            expander.add(vbox)
            self.expanders.append(expander)
            self.vboxes.append(vbox)

    def add_item(self, vbox, method, name, widget_info):
        widget_type = widget_info["widget_type"]
        data_type = widget_info.get("data_type", None)
        values = widget_info.get("values", None)
        widget_type = MlModel.parse_widget_type(widget_type)
        item = LearnArgumentsItem(name, widget_type, data_type, values)
        if "default" in widget_info:
            item.set_default(widget_info["default"])
        self.items.append(item)
        vbox.pack_start(item, True, True, 0)
        self.method_args[method][name] = item

    def get_arguments(self):
        return {
            method: {name: item.get_value() for name, item in args.items()}
            for method, args in self.method_args.items()
        }

    def destroy(self):
        for items in [self.items, self.vboxes, self.expanders]:
            for item in items:
                item.destroy()
