from gi.repository import Gtk

from learning.defined_models import learn_models
from .learn_arguments_item import LearnArgumentsItem
from learning.ml_model import MlModel


class LearnArgumentsView:
    def __init__(self, view, ml_model_name=None):
        self.items, self.expanders, self.vboxes = [], [], []
        self.method_args = dict()
        self.view = view
        learn_arguments = learn_models[ml_model_name].parse_options("learning")
        self.ml_model_name = ml_model_name
        for method, arguments in learn_arguments.items():
            expander, vbox = Gtk.Expander(label=method), Gtk.VBox()
            self.method_args[method] = dict()
            for name, widget_info in arguments.items():
                widget_type = widget_info["widget_type"]
                data_type = widget_info["data_type"] if "data_type" in widget_info else None
                values = widget_info["values"] if "values" in widget_info else None
                widget_type = MlModel.parse_widget_type(widget_type)
                item = LearnArgumentsItem(name, widget_type, data_type, values)
                self.items.append(item)
                vbox.pack_end(item, True, True, 0)
                self.method_args[method][name] = item
            self.view.get_content_area().add(expander)
            expander.add(vbox)
            self.expanders.append(expander)
            self.vboxes.append(vbox)

    def get_arguments(self):
        res = {method: {name: item.get_value() for name, item  in args.items()} for method, args in self.method_args.items()}
        return res

    def destroy(self):
        for items in [self.items, self.vboxes, self.expanders]:
            for item in items:
                item.destroy()
