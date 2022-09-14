#!/usr/bin/env python3

import csv

from gi.repository import Gtk

from views import constants
from controllers.file_handler import populate
from views.about_view import AboutDialog
from views.file_chooser_view import FileChooser
from views.output_view import OutputView


class Main:
    def __init__(self):
        self._builder = Gtk.Builder()
        self._builder.add_from_file(constants.GLADE_FILE)
        self._builder.connect_signals(self)

        self.window = self._builder.get_object("window")
        self.window.show()

        self.renderer = Gtk.CellRendererText()

    def on_destroy(self, *args):
        Gtk.main_quit()

    def on_quit_clicked(self, item):
        Gtk.main_quit()

    def on_file_activate(self, item):
        file_chooser = FileChooser(self.window)
        filename = file_chooser.get_csv()
        file_chooser.destroy()
        print(self._builder.get_object("input_store"))
        if filename:
            columns = self.get_columns(filename)
            print(f"type:{type(columns)}")
            output_chooser = OutputView(self, columns)
            ins, out = output_chooser.get_ins_out()
            output_chooser.destroy()
            if ins is None or out is None:
                return

            input_store, output_store = populate(filename, ins, out)
            input_view = self._builder.get_object("input_view")
            input_view.set_model(input_store)
            for col in input_view.get_columns():
                input_view.remove_column(col)
            output_view = self._builder.get_object("output_view")
            output_view.set_model(output_store)
            for col in output_view.get_columns():
                output_view.remove_column(col)

            for i, column in enumerate(ins):
                input_view.append_column(
                    Gtk.TreeViewColumn(column, self.renderer, text=i)
                )
            output_view.append_column(
                Gtk.TreeViewColumn(out, self.renderer, text=0)
            )

    def get_columns(self, filename):
        with open(filename) as f:
            reader = csv.reader(f)
            for row in reader:
                return row


    def on_about_activate(self, button):
        aboutDialog = AboutDialog(self.window)
        aboutDialog.run()
        aboutDialog.destroy()

    def on_cancel_clicked(self, button):
        self.destroy()
