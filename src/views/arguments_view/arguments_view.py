import os

from gi.repository import Gtk
import flatdict
import toml

from learning.defined_models import learn_models
from learning.ml_model import MlModel
from views.arguments_view.argument_item import ArgumentItem
from views.arguments_view import util


class ArgumentsView(Gtk.VBox):
    def __init__(
        self,
        view,
        ml_model_name,
        parse_options=["learning"],
        save_file=None,
        parent=None,
    ):
        super().__init__()
        self.parent = parent
        self.save_file = save_file
        self.changed_values, self.items = {}, {}
        self.view = view
        self.saved_settings = {}
        if self.save_file and os.path.exists(self.save_file):
            with open(self.save_file) as f:
                self.saved_settings = toml.load(f)
        for option in parse_options:
            arguments = learn_models[ml_model_name].parse_options(option)
            self.items[option] = {}
            for method, arguments in arguments.items():
                view, expand = self, True
                if len(parse_options) != 1:
                    view = Gtk.Frame()
                    self.add(view)
                    expand = False
                self.__add_sublists([option, method], arguments, view, 0, expand)

    def __add_sublists(self, method, arguments, view, margin, expand=False):
        expander, vbox = (
            Gtk.Expander(label=method[-1], margin_left=margin, valign=Gtk.Align.START),
            Gtk.VBox(),
        )
        util.get_recursive_dict_item(self.items, method, 1)[method[-1]] = {}
        for name, widget_info in arguments.items():
            if "widget_type" in widget_info:
                self.__add_item(vbox, method + [name], name, widget_info)
            else:
                self.__add_sublists(method + [name], widget_info, vbox, margin + 10)
        expander.add(vbox)
        view.add(expander)
        if expand:
            expander.set_expanded(True)

    def __add_item(self, vbox, method, name, widget_info):
        widget_type = widget_info["widget_type"]
        data_type = widget_info.get("data_type", None)
        values = widget_info.get("values", None)
        widget_type = MlModel.parse_widget_type(widget_type)
        parent = self if self.save_file else None
        method_param = method if self.save_file else None
        item = ArgumentItem(name, widget_type, data_type, values, parent, method_param)
        dict_item = util.get_recursive_dict_item(self.items, method, 1)
        dict_item[method[-1]] = item
        self.__set_item_attribs(item, widget_info, method)
        vbox.pack_start(item, True, True, 0)

    def __set_item_attribs(self, item, widget_info, method):
        if "can_none" in widget_info:
            if widget_info["can_none"]:
                item.add_none_tickbox()
        if util.exists_recursive_dict_item(self.saved_settings, method):
            item.set_default(util.get_recursive_dict_item(self.saved_settings, method))
        elif "default" in widget_info:
            item.set_default(widget_info["default"])
        item.set_saved()
        if "enabled_on" in widget_info:
            enabled_on = widget_info["enabled_on"]
            util.get_recursive_dict_item_from_toml(
                self.items, enabled_on["argument"]
            ).add_enabled_on((item, enabled_on["value"]))
            item.set_widget_sensitive(False)
        if "disabled_on" in widget_info:
            disabled_on = widget_info["disabled_on"]
            util.get_recursive_dict_item_from_toml(
                self.items, disabled_on["argument"]
            ).add_disabled_on((item, enabled_on["value"]))
            item.set_widget_sensitive(False)
        if "visible_on" in widget_info:
            visible_on = widget_info["visible_on"]
            util.get_recursive_dict_item_from_toml(
                self.items, visible_on["argument"]
            ).add_visible_on((item, visible_on["value"]))
            item.set_widget_visible(False)
        if "invisible_on" in widget_info:
            invisible_on = widget_info["invisible_on"]
            util.get_recursive_dict_item_from_toml(
                self.items, invisible_on["argument"]
            ).add_invisible_on((item, invisible_on["value"]))
            item.set_widget_visible(False)

    def get_arguments(self, items=None):
        items = self.items if items is None else items
        args = {}
        for level, item in items.items():
            if isinstance(item, dict):
                if len(item) != 0:
                    args.update({level: self.get_arguments(item)})
                else:
                    continue
            else:
                if item.is_visible() and item.get_widget_sensitive():
                    args.update({level: item.get_value()})
        # print(args)
        return args

    def on_value_changed(self, method, value):
        item = util.get_recursive_dict_item(self.items, method)
        if not item.get_visible():
            return
        if item.get_default() == value:
            util.delete_recursive_dict(self.changed_values, method)
            if util.check_empty_dict(self.changed_values):
                self.changed_values.clear()
        else:
            util.set_recursive_dict_item(self.changed_values, method, value)
        self.parent.set_edited(bool(len(self.changed_values)))

    def save(self):
        for item in flatdict.FlatDict(self.items).values():
            item.set_saved()
        if self.save_file:
            with open(self.save_file, "w") as f:
                toml.dump(self.changed_values, f)
        self.changed_values.clear()
