#!/usr/bin/env python

from gi.repository import Gtk

from views import utils
from views.split_view import SplitView
from views.learn_dialog import LearnDialog
from views.result_view import ResultView
from views.about_view import AboutDialog
from views.file_chooser_view import FileChooserView

from models.split_model import SplitModel
from models.file_chooser_model import FileChooserModel

from controllers.split_controller import SplitController
from controllers.file_chooser_controller import FileChooserController
from controllers import file_handler


class MainController:
    def __init__(self, model, view):
        self.model, self.view = model, view
        self.file_chooser_model = FileChooserModel()

    def get_ins_out(self):
        model = SplitModel(
            file_handler.get_columns_from_csv(self.file_chooser_model.filename)
        )
        view = SplitView(self.view.window, model)
        controller = SplitController(model, view)

        split_kwargs = controller.get_ins_out()
        view.destroy()
        return split_kwargs

    def on_destroy(self, *args):
        Gtk.main_quit()

    def on_quit_clicked(self, item):
        Gtk.main_quit()

    def on_file_activate(self, item):
        view = FileChooserView(self.view.window, self.file_chooser_model)
        file_chooser = FileChooserController(self.file_chooser_model, view)

        self.file_chooser_model.set_filename(file_chooser.get_csv())
        view.destroy()
        if not self.file_chooser_model.filename:
            return

        split_kwargs = self.get_ins_out()
        if split_kwargs["ins"] is None or split_kwargs["out"] is None:
            return

        self.model.set_dataframe(self.file_chooser_model.filename, **split_kwargs)
        store = self.model.get_store(**split_kwargs)
        utils.view_trees(self.view._builder, store, **split_kwargs)

    def on_about_activate(self, button):
        about_dialog = AboutDialog(self.view.window)
        about_dialog.run()
        about_dialog.destroy()

    def on_cancel_clicked(self, button):
        self.view.destroy()

    def on_learn_clicked(self, button):
        if self.model.tdf is None:
            return
        learn_dialog = LearnDialog(self.view)
        kwargs = learn_dialog.get_learn_kwargs()
        result_dialog = ResultView(self, **kwargs)
        result_dialog.run()
        result_dialog.destroy()
