from gi.repository import Gtk


class SplitsController:
    def __init__(self, model, view):
        self.model, self.view = model, view
        self.prev_out = None

    def get_ins_out(self):
        response = self.view.run()
        if response == Gtk.ResponseType.CANCEL:
            return None
        split_kwargs = {}
        split_kwargs["validation_split_method"] = next(
            (
                radio.get_label().lower()
                for radio in self.view.first_split_method_button.get_group()
                if radio.get_active()
            )
        )
        split_kwargs["pct"] = self.view.validation_scale.get_value()
        selection = self.view.output_choose_combo.get_active_text()
        selected_cols = self.get_included_excluded_columns()
        excluded_ticked = self.view.excluded_radio.get_active()
        in_columns = self.model.columns.copy()
        in_columns.remove(selection)
        split_kwargs["ins"] = (
            [col for col in in_columns if col not in selected_cols]
            if excluded_ticked is True
            else [col for col in in_columns if col in selected_cols]
        )
        split_kwargs["out"] = selection
        return split_kwargs

    def get_included_excluded_columns(self):
        cols = []
        model, pathlist = self.view.incl_excl_tree.get_selection().get_selected_rows()
        for path in pathlist:
            tree_iter = model.get_iter(path)
            value = model.get_value(tree_iter, 0)
            cols.append(value)
        return cols

    # TODO: only replace not clear and populate
    def on_output_choose_combo_changed(self, item):
        self.view.incl_excl_store.clear()
        for col in self.model.columns:
            if col != self.view.output_choose_combo.get_active_text():
                self.view.incl_excl_store.append([col])


if __name__ == "__main__":
    # from views.splits_view import SplitsView
    # from views.splits_model import SplitsModel
    model = SplitsModel(["inp col1", "inp col2", "inp col3", "out col"])
    view = SplitsView(model)
    controller = SplitsController(model, view)
    view.register_listener(controller)
    print(controller.get_ins_out())
