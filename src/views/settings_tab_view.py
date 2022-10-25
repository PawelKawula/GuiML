from gi.repository import Gtk

from views.arguments_view.arguments_view import ArgumentsView


class SettingsTabView(Gtk.Box):
    def __init__(self, dialog, model):
        super().__init__(orientation=Gtk.Orientation.VERTICAL)
        self.model = model
        self.set_border_width(10)
        button_box = Gtk.ButtonBox(
            layout_style=Gtk.ButtonBoxStyle.END,
            orientation=Gtk.Orientation.HORIZONTAL,
            halign=Gtk.Align.END,
            margin_top=10,
        )
        self.button_revert = Gtk.Button.new_from_stock("gtk-revert-to-saved")
        button_box.add(self.button_revert)
        self.button_save = Gtk.Button.new_from_stock("gtk-save")
        button_box.add(self.button_save)
        self.args_view = ArgumentsView(dialog, model.model_name, ["general"])
        scrolled_window = Gtk.ScrolledWindow()
        scrolled_window.add(self.args_view)
        self.pack_start(scrolled_window, True, True, 0)
        self.pack_start(button_box, False, False, 0)

    def register_listener(self, controller):
        self.button_revert.connect("clicked", controller.on_revert_clicked)
        self.button_save.connect("clicked", controller.on_save_clicked)
