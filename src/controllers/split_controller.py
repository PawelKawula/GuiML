#!/usr/bin/env python

from gi.repository import Gtk


class SplitController:
    def __init__(self, model, view):
        self.model, self.view = model, view

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
        split_kwargs["ins"] = [x for x in self.model.columns if x != selection]
        split_kwargs["out"] = selection
        return split_kwargs
