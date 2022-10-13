from gi.repository import Gtk

from views import constants
from views.arguments_view.arguments_view import ArgumentsView
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

        for model_name in learn_models:
            page = Gtk.VBox()
            page.set_border_width(10)
            button_box = Gtk.ButtonBox(
                layout_style=Gtk.ButtonBoxStyle.END,
                orientation=Gtk.Orientation.VERTICAL,
                halign=Gtk.Align.END,
                margin_top=10,
            )
            button_save = Gtk.Button.new_from_stock("gtk-save")
            button_save.connect("clicked", self.on_save_clicked)
            button_box.add(button_save)
            args_view = ArgumentsView(self.dialog, model_name, ["general"])
            scrolled_window = Gtk.ScrolledWindow()
            scrolled_window.add(args_view)
            self.model_configs[model_name] = args_view
            page.pack_start(scrolled_window, True, True, 0)
            page.pack_start(button_box, False, False, 0)
            self.notebook.append_page(page, Gtk.Label(label=model_name))
        self.notebook.show_all()

    def register_listener(self, controller):
        self._builder.connect_signals(controller)

    def on_save_clicked(self, item):
        tab_label = self.notebook.get_tab_label_text(
            self.notebook.get_nth_page(self.notebook.get_current_page())
        )
        conf = self.model_configs[tab_label].get_arguments()
        learn_models[tab_label].save_config(conf)
