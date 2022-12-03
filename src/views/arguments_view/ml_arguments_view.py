import os

from gi.repository import Gtk
import flatdict
import toml

from learning.defined_models import learn_models
from learning.ml_model import MlModel
from .argument_item import ArgumentItem
from . import util


class MlArgumentsView(Gtk.VBox):
    def __init__(
        self,
        view,
        ml_model_name,
        options_to_parse=["learning"],
        save_file=None,
        parent=None,
    ):
        super().__init__()
        self.parent, self.save_file, self.view = parent, save_file, view
        self.ml_model_name, self.options_to_parse = ml_model_name, options_to_parse
        self.changed_values, self.items = {}, {}
        self.saved_settings = self.__load_save_file(save_file)
        for option in self.options_to_parse:
            widget_dict_for_cat = learn_models[ml_model_name].parse_options(option)
            self.__create_item_widgets_for_cat(widget_dict_for_cat, option)


    def __decorate_widget_group_in_frame(self, view):
        view = Gtk.Frame()
        self.add(view)

    def __create_item_widgets_for_cat(self, widget_dict_for_cat, option):
        self.items[option] = {}
        self.__parse_group_or_leaf_widgets_from_dict(widget_dict_for_cat, option)

    def __parse_group_or_leaf_widgets_from_dict(self, widget_dict_for_cat, option):
        for method, arguments in widget_dict_for_cat.items():
            view, expand = self, True
            if len(self.options_to_parse) != 1:
                expand = False
                self.__decorate_widget_group_in_frame(view)
            self.__add_widget_group(
                [option, method], arguments, view, 0, expand
            )


    def __load_save_file(self, save_file):
        if save_file and os.path.exists(save_file):
            with open(save_file) as f:
                return toml.load(f)
        return {}

    def __add_widget_group(self, method, arguments, view, margin, expand=False):
        expander, vbox = (
            Gtk.Expander(
                label=method[-1], margin_left=margin, valign=Gtk.Align.START
            ),
            Gtk.VBox(),
        )
        util.get_recursive_dict_item(self.items, method, 1)[method[-1]] = {}
        for name, widget_info in arguments.items():
            if "widget_type" in widget_info:
                self.__add_item(vbox, method + [name], name, widget_info)
            else:
                self.__add_widget_group(
                    method + [name], widget_info, vbox, margin + 10
                )
        expander.add(vbox)
        view.add(expander)
        expander.set_expanded(expand)

    def __add_item(self, vbox, method, name, widget_info):
        widget_type = widget_info["widget_type"]
        data_type = widget_info.get("data_type", None)
        values = widget_info.get("values", None)
        widget_type = MlModel.parse_widget_type(widget_type)
        parent, method_param = self, method
        item = ArgumentItem(
            name, widget_type, data_type, values, parent, method_param, True
        )
        dict_item = util.get_recursive_dict_item(self.items, method, 1)
        dict_item[method[-1]] = item
        self.__set_item_attribs(item, widget_info, method)
        vbox.pack_start(item, True, True, 0)

    def __set_item_attribs(self, item, widget_info, method):
        if "can_none" in widget_info:
            if widget_info["can_none"]:
                item.add_none_tickbox()
        if util.exists_recursive_dict_item(self.saved_settings, method):
            item.set_default(
                util.get_recursive_dict_item(self.saved_settings, method)
            )
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
