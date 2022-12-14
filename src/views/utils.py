import csv
from copy import deepcopy

from gi.repository import Gtk


def view_trees(
    items_view, items_store, ins, out, expanded=False, **split_kwargs
):
    items_view.set_model(items_store)
    if expanded:
        items_view.expand_all()
    for col in items_view.get_columns():
        items_view.remove_column(col)

    renderer = Gtk.CellRendererText()
    columns = deepcopy(ins)
    columns.append(f"{out} (Out)")
    for i, column in enumerate(columns):
        items_view.append_column(Gtk.TreeViewColumn(column, renderer, text=i))


def is_none_in_dict(obj):
    if obj is None:
        return True
    if isinstance(obj, dict):
        for v in obj.values():
            if is_none_in_dict(v) and not v.get("can_none", False):
                return True
    return False
