from copy import deepcopy

from gi.repository import Gtk
import pandas as pd

from . import constants, utils
from .template import Template
from .splits_view import SplitsView
from .learn_dialog import LearnDialog
from .result_view import ResultView
from .about_view import AboutDialog
from .file_chooser_view import FileChooserView
from .settings_view import SettingsView
from common import file_handler
from common.configs.global_ml_config import (
    GlobalMlConfig,
    ReadOnlyGlobalMlConfig,
)
from common.configs.splits_config import SplitsConfig, ReadOnlySplitsConfig
from common.none_val import NoneVal
from models.dataset_tree_store import DatasetTreeStore


@Template(filename=constants.GLADE_FILE)
class MainView(Gtk.Window):
    __gtype_name__ = "window"

    def __init__(self):
        super().__init__()
        self.splits_config = SplitsConfig()
        self.ro_splits_config = ReadOnlySplitsConfig(self.splits_config)
        self.ml_config = GlobalMlConfig()
        self.ro_ml_config = ReadOnlyGlobalMlConfig(self.ml_config)
        self.store = Gtk.TreeStore()

    def __set_ins_out(self, filename):
        splits = SplitsView(self)
        self.splits_config.update(**splits.get_ins_out())
        splits.destroy()

    @Gtk.Template.Callback()
    def on_destroy(self, arg):
        Gtk.main_quit()

    @Gtk.Template.Callback()
    def on_settings_activate(self, item):
        settings = SettingsView(self)
        settings.run()
        settings.destroy()

    @Gtk.Template.Callback()
    def on_quit_activate(self, item):
        Gtk.main_quit()

    @Gtk.Template.Callback()
    def on_file_activate(self, item):
        file_chooser = FileChooserView(self)
        filename = file_chooser.get_csv()
        self.ml_config.set_filename(filename)
        self.__populate_tree(filename)

    def __populate_tree(self, filename):
        if filename == None:
            return
        self.__set_ins_out(filename)
        if not self.__is_splits_config_correct():
            return
        cols = self.ro_splits_config.get_ins() + [
            self.ro_splits_config.get_out()
        ]
        df = pd.read_csv(filename)[cols]
        self.ml_config.set_df(df)

        self.ml_config.set_tdf(
            file_handler.get_tabular_pandas(
                df.copy(), **self.ro_splits_config.dump_dict_copy()
            )
        )
        if self.ro_splits_config.get_render():
            self.store = self.__get_store(**self.ro_splits_config.dump_dict_copy())
        else:
            self.store.clear()

        utils.view_trees(
            self.items_view, self.store, **self.ro_splits_config.dump_dict_copy()
        )

    def __is_splits_config_correct(self):
        return not (
            self.ro_splits_config.is_none()
            or self.ro_splits_config.get_ins() is NoneVal
            or self.ro_splits_config.get_out() is NoneVal
        )

    def __get_store(self, **split_kwargs):
        tdf = self.ro_ml_config.get_tdf()
        assert tdf is not None, "Dataframe not initialized"
        tdf = file_handler.get_values(tdf, **split_kwargs)
        if tdf is None:
            return None
        return file_handler.get_store(tdf)

    @Gtk.Template.Callback()
    def on_about_activate(self, button):
        about_dialog = AboutDialog(self)
        about_dialog.run()
        about_dialog.destroy()

    @Gtk.Template.Callback()
    def on_learn_clicked(self, button):
        tdf = self.ro_ml_config.get_tdf()
        if tdf is None:
            return
        learn_dialog = LearnDialog(self)
        ml_model, kwargs = learn_dialog.get_learn_kwargs()
        if kwargs is None:
            return
        result_dialog = ResultView(self, ml_model, **kwargs)

    def get_splits_config(self):
        return self.ro_splits_config

    def get_ml_config(self):
        return self.ro_ml_config
