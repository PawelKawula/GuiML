from gi.repository import Gtk

from . import constants
from .template import Template
from common.configs.global_ml_config import ReadOnlyGlobalMlConfig
from common.configs.splits_config import SplitsConfig
from common import file_handler


@Template(filename=constants.SPLITS_FILE)
class SplitsView(Gtk.Dialog):
    __gtype_name__ = "splits_dialog"

    def __init__(self, parent):
        super().__init__(parent)
        self.ml_config = parent.get_ml_config()
        self.columns = file_handler.get_columns_from_csv(
            self.ml_config.get_filename()
        )

        for col in self.columns:
            self.output_choose_combo.append_text(col)
        self.validation_scale.set_range(1, 99)
        self.validation_scale.set_value(75)
        self.incl_excl_store = Gtk.ListStore(str)
        self.incl_excl_tree.set_model(self.incl_excl_store)
        self.incl_excl_tree.get_selection().set_mode(Gtk.SelectionMode.MULTIPLE)
        self.incl_excl_tree.append_column(
            Gtk.TreeViewColumn("column name", Gtk.CellRendererText(), text=0)
        )

    def get_ins_out(self):
        response = self.run()
        if response != int(Gtk.ResponseType.OK):
            return None
        split_kwargs = {}
        split_kwargs["validation_split_method"] = next(
            (
                radio.get_label().lower()
                for radio in self.split_method_combo_time.get_group()
                if radio.get_active()
            )
        )
        split_kwargs["pct"] = self.validation_scale.get_value()
        selection = self.output_choose_combo.get_active_text()
        selected_cols = self.get_included_excluded_columns()
        excluded_ticked = self.excluded_radio.get_active()
        in_columns = self.columns.copy()
        in_columns.remove(selection)
        split_kwargs["ins"] = (
            [col for col in in_columns if col not in selected_cols]
            if excluded_ticked is True
            else [col for col in in_columns if col in selected_cols]
        )
        split_kwargs["out"] = selection
        split_kwargs["render"] = self.render_checkbox.get_active()
        return split_kwargs

    def get_included_excluded_columns(self):
        cols = []
        (
            model,
            pathlist,
        ) = self.incl_excl_tree.get_selection().get_selected_rows()
        for path in pathlist:
            tree_iter = model.get_iter(path)
            value = model.get_value(tree_iter, 0)
            cols.append(value)
        return cols

    # TODO: only replace not clear and populate
    @Gtk.Template.Callback()
    def on_output_choose_combo_changed(self, item):
        self.incl_excl_store.clear()
        for col in self.columns:
            if col != self.output_choose_combo.get_active_text():
                self.incl_excl_store.append([col])
