from gi.repository import Gtk
import flatdict

from views import constants
from .template import Template
from .arguments_view.arguments_view import ArgumentsView
from .settings_tab_view import SettingsTabView

from learning.defined_models import learn_models
from common.configs.global_ml_config import GlobalMlConfig


@Template(filename=constants.SETTINGS_FILE)
class SettingsView(Gtk.Dialog):
    __gtype_name__ = "settings_dialog"

    def __init__(self, parent):
        super().__init__(parent)
        self.model_configs = {}

        for model_name in parent.get_ml_config().get_learn_models():
            stv = SettingsTabView(self, model_name)
            self.model_configs[model_name] = stv
            self.notebook.append_page(stv, stv.get_title_label())
        self.notebook.show_all()

    def save_model_configs(self, model_name):
        conf = self.model_configs[model_name].args_view.get_arguments()
        self.notebook.get_nth_page(self.notebook.get_current_page()).save()
        learn_models[model_name].save_current(conf)

    def revert_model_configs(self, model_name):
        flat_items = flatdict.FlatDict(
            self.model_configs[model_name].args_view.items
        )
        flat_default = flatdict.FlatDict(learn_models[model_name].get_default())
        flat_changed = flatdict.FlatDict(
            self.model_configs[model_name].args_view.changed_values
        )
        for (key, item), value in zip(
            flat_items.items(), flat_default.values()
        ):
            item.set_default(value)
            if key in flat_changed:
                item.set_changed()
        self.notebook.show_all()
