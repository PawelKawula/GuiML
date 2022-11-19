from gi.repository import Gtk

from views import constants


class SplitsView:
    def __init__(self, model):
        self.model = model
        self._builder = constants.GTK_BUILDER
        self._builder.add_from_file(constants.SPLITS_FILE)

        self.window = self._builder.get_object("dialog")
        self.output_choose_combo = self._builder.get_object("output_choose_combo")
        for col in model.columns:
            self.output_choose_combo.append_text(col)
        self.first_split_method_button = self._builder.get_object(
            "split_method_combo_rand"
        )
        self.split_method_combo_time = self._builder.get_object(
            "split_method_combo_time"
        )
        self.validation_scale = self._builder.get_object("validation_scale")
        self.validation_scale.set_range(1, 99)
        self.validation_scale.set_value(75)
        self.excluded_radio = self._builder.get_object("excluded_radio")
        self.incl_excl_store = self._builder.get_object("incl_excl_store")
        self.incl_excl_tree = self._builder.get_object("incl_excl_tree")
        self.incl_excl_tree.get_selection().set_mode(Gtk.SelectionMode.MULTIPLE)
        self.incl_excl_tree.append_column(
            Gtk.TreeViewColumn("column name", Gtk.CellRendererText(), text=0)
        )

    def register_listener(self, controller):
        self._builder.connect_signals(controller)

    def get_builder(self):
        return self._builder

    def run(self):
        return self.window.run()

    def destroy(self):
        self.window.destroy()
