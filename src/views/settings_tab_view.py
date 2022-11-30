from gi.repository import Gtk

from views import constants

from views.arguments_view.arguments_view import ArgumentsView
from views.template import Template


@Template(filename=constants.SETTINGS_TAB_FILE)
class SettingsTabView(Gtk.Box):
    __gtype_name__ = "settings_tab_box"

    def __init__(self, parent, title):
        super().__init__(orientation=Gtk.Orientation.VERTICAL)
        self.title, self.parent = title, parent
        self.title_label = Gtk.Label(label=title)
        self.args_view = ArgumentsView(
            parent,
            self.title_label.get_text(),
            ["general"],
            save_file=f"{title}.toml",
            parent=self,
        )
        self.scrolled_window.add(self.args_view)

    def set_edited(self, edited):
        self.title_label.set_label(f"* {self.title}" if edited else self.title)

    def get_title_label(self):
        return self.title_label

    def save(self):
        self.title_label.set_label(self.title)
        self.args_view.save()

    @Gtk.Template.Callback()
    def on_save_clicked(self, item):
        self.parent.save_model_configs(self.title)

    @Gtk.Template.Callback()
    def on_revert_clicked(self, item):
        self.parent.revert_model_configs(self.title)
