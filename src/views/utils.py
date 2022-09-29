#!/usr/bin/env python3

import csv
from copy import deepcopy

from gi.repository import Gtk


def view_trees(builder, items_store, ins, out, **split_kwargs):
    items_view = builder.get_object("items_view")
    items_view.set_model(items_store)
    for col in items_view.get_columns():
        items_view.remove_column(col)

    """
    output_view = builder.get_object("output_view")
    output_view.set_model(output_store)
    for col in output_view.get_columns():
        output_view.remove_column(col)
    """
    renderer = Gtk.CellRendererText()
    columns = deepcopy(ins)
    columns.append(f"{out} (Out)")
    for i, column in enumerate(columns):
        items_view.append_column(Gtk.TreeViewColumn(column, renderer, text=i))
