from copy import deepcopy

from gi.repository import Gtk

from views import constants, utils
from views.template import Template
from views.splits_view import SplitsView
from views.learn_dialog import LearnDialog
from views.result_view import ResultView
from views.about_view import AboutDialog
from views.file_chooser_view import FileChooserView
from views.settings_view import SettingsView
from common import file_handler
from common.configs.global_ml_config import GlobalMlConfig, ReadOnlyGlobalMlConfig
from common.configs.splits_config import SplitsConfig, ReadOnlySplitsConfig
from common.none_val import NoneVal


@Template(filename=constants.GLADE_FILE)
class MainView(Gtk.Window):
    __gtype_name__ = "window"
    def __init__(self):
        super().__init__()
        self.splits_config = SplitsConfig()
        self.ro_splits_config = ReadOnlySplitsConfig(self.splits_config)
        self.ml_config = GlobalMlConfig()
        self.ro_ml_config = ReadOnlyGlobalMlConfig(self.ml_config)

    def __get_ins_out(self, filename):
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
        file_chooser.destroy()
        self.ml_config.set_filename(filename if filename else NoneVal)
        self.__populate_tree(filename)

    def __populate_tree(self, filename):
        if filename == NoneVal:
            return
        self.__get_ins_out(filename)
        if not self.__is_splits_config_correct():
            return

        self.ml_config.set_tdf(file_handler.get_tabular_pandas(**self.ro_splits_config.dump_dict_copy()))
        store = self.__get_store(**self.ro_splits_config.dump_dict_copy())
        utils.view_trees(self.items_view, store, **self.ro_splits_config.dump_dict_copy())

    def __is_splits_config_correct(self):
        return not(self.ro_splits_config.is_none()
            or self.ro_splits_config.get_ins() is NoneVal
            or self.ro_splits_config.get_out() is NoneVal)

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
        # learn_dialog.destroy()
        if kwargs is None:
            return
        result_dialog = ResultView(self, ml_model, **kwargs)
        # result_dialog.run()
        # result_dialog.destroy()
    def get_splits_config(self):
        return self.ro_splits_config

    def get_ml_config(self):
        return self.ro_ml_config
