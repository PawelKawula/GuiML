from gi.repository import Gtk

from views import constants

class SettingsView():
    def __init__(self, model):
        self.model = model
        self._builder = Gtk.Builder()
        self._builder.add_from_file(constants.SETTINGS_FILE)

        self.dialog = self._builder.get_object("dialog")
        self.notebook = Gtk.Notebook(expand=True)
        self._builder.get_object("box").pack_start(self.notebook, True, True, 0)

        for i in range(2):
            page = Gtk.Box()
            page.set_border_width(10)
            page.add(Gtk.Label(label=f"page {i}"))
            self.notebook.append_page(page, Gtk.Label(label=f"page {i}"))
            print("page added")
        self.notebook.show_all()

        # self.notebook.append_page(Gtk.Label(label="page 1"), Gtk.Label(label="page 1"))
        # self.notebook.append_page(Gtk.Label(label="page 2"), Gtk.Label(label="page 2"))
        # self.notebook.append_page(Gtk.Label(label="page 3"), Gtk.Label(label="page 3"))

    def register_listener(self, controller):
        self._builder.connect_signals(controller)
