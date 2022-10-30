from gi.repository import Gtk
import flatdict

from models.settings_tab_model import SettingsTabModel
from views import constants
from views.arguments_view.arguments_view import ArgumentsView
from views.settings_tab_view import SettingsTabView
from controllers.settings_tab_controller import SettingsTabController
from learning.defined_models import learn_models


class SettingsView:
    def __init__(self, model):
        self.model = model
        self._builder = Gtk.Builder()
        self._builder.add_from_file(constants.SETTINGS_FILE)

        self.dialog = self._builder.get_object("dialog")
        self.notebook = Gtk.Notebook(expand=True)
        self._builder.get_object("box").pack_start(self.notebook, True, True, 0)
        self.model_configs = {}

        for model_name in model.learn_models:
            model = SettingsTabModel(model_name)
            view = SettingsTabView(self.dialog, model, model_name)
            controller = SettingsTabController(self, model, view)
            view.register_listener(controller)
            self.model_configs[model_name] = view
            self.notebook.append_page(view, view.get_title_label())
        self.notebook.show_all()

    def register_listener(self, controller):
        self._builder.connect_signals(controller)

    def save_model_configs(self, model_name):
        conf = self.model_configs[model_name].args_view.get_arguments()
        self.notebook.get_nth_page(self.notebook.get_current_page()).save()
        learn_models[model_name].save_current(conf)

    def revert_model_configs(self, model_name):
        flat_items = flatdict.FlatDict(self.model_configs[model_name].args_view.items)
        flat_default = flatdict.FlatDict(learn_models[model_name].get_default())
        flat_changed = flatdict.FlatDict(
            self.model_configs[model_name].args_view.changed_values
        )
        for (key, item), value in zip(flat_items.items(), flat_default.values()):
            item.set_default(value)
            if key in flat_changed:
                item.set_changed()
        self.notebook.show_all()
