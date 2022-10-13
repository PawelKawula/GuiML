from gi.repository import Gtk

from learning.defined_models import learn_models
from learning.ml_model import MlModel
from .argument_item import ArgumentItem
from .util import get_recursive_dict_item, get_recursive_dict_item_from_toml


class ArgumentsView(Gtk.VBox):
    def __init__(self, view, ml_model_name, parse_options=["learning"]):
        super().__init__()
        self.items = {}
        self.view = view
        for option in parse_options:
            arguments = learn_models[ml_model_name].parse_options(option)
            self.items[option] = {}
            for method, arguments in arguments.items():
                view, expand = self, True
                if len(parse_options) != 1:
                    view = Gtk.Frame()
                    self.add(view)
                    expand = False
                self.add_sublists([option, method], arguments, view, 0, expand)

    def add_sublists(self, method, arguments, view, margin, expand=False):
        expander, vbox = (
            Gtk.Expander(label=method[-1], margin_left=margin, valign=Gtk.Align.START),
            Gtk.VBox(),
        )
        get_recursive_dict_item(self.items, method, 1)[method[-1]] = {}
        for name, widget_info in arguments.items():
            if "widget_type" in widget_info:
                self.add_item(vbox, method + [name], name, widget_info)
            else:
                self.add_sublists(method + [name], widget_info, vbox, margin + 10)
        expander.add(vbox)
        view.add(expander)
        if expand:
            expander.set_expanded(True)

    def add_item(self, vbox, method, name, widget_info):
        widget_type = widget_info["widget_type"]
        data_type = widget_info.get("data_type", None)
        values = widget_info.get("values", None)
        widget_type = MlModel.parse_widget_type(widget_type)
        item = ArgumentItem(name, widget_type, data_type, values)
        dict_item = get_recursive_dict_item(self.items, method, 1)
        dict_item[method[-1]] = item
        self.set_item_attribs(item, widget_info)
        vbox.pack_start(item, True, True, 0)

    def set_item_attribs(self, item, widget_info):
        if "default" in widget_info:
            item.set_default(widget_info["default"])
        if "enabled_on" in widget_info:
            enabled_on = widget_info["enabled_on"]
            get_recursive_dict_item_from_toml(
                self.items, enabled_on["argument"]
            ).add_enabled_on((item, enabled_on["value"]))
            item.set_widget_sensitive(False)
        if "disabled_on" in widget_info:
            disabled_on = widget_info["disabled_on"]
            get_recursive_dict_item_from_toml(
                self.items, disabled_on["argument"]
            ).add_disabled_on((item, enabled_on["value"]))
            item.set_widget_sensitive(False)
        if "visible_on" in widget_info:
            visible_on = widget_info["visible_on"]
            get_recursive_dict_item_from_toml(
                self.items, visible_on["argument"]
            ).add_visible_on((item, visible_on["value"]))
            item.set_widget_visible(False)
        if "invisible_on" in widget_info:
            invisible_on = widget_info["invisible_on"]
            get_recursive_dict_item_from_toml(
                self.items, invisible_on["argument"]
            ).add_invisible_on((item, invisible_on["value"]))
            item.set_widget_visible(False)

    def get_arguments(self, items=None):
        items = self.items if items is None else items
        args = {}
        for level, item in items.items():
            if isinstance(item, dict) and len(item) != 0:
                args.update({level: self.get_arguments(item)})
            else:
                if item.is_visible() and item.get_widget_sensitive():
                    args.update({level: item.get_value()})
        return args
