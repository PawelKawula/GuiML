#!/usr/bin/env python

from models.split_model import SplitModel
from controllers import file_handler


class MainModel:
    def __init__(self):
        self.items_store = None
        self.df, self.tdf = None, None

    def set_dataframes(self, filename, **split_kwargs):
        self.df, self.tdf = file_handler.get_tabular_pandas(filename, **split_kwargs)

    def get_store(self, **split_kwargs):
        assert (
            self.df is not None and self.tdf is not None
        ), "Dataframes not initialized"
        values = file_handler.get_values(
            self.df, **split_kwargs
        )
        if values is None:
            return None
        return file_handler.get_store(values, **split_kwargs)
