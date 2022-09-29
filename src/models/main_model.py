#!/usr/bin/env python

from models.split_model import SplitModel
from controllers import file_handler


class MainModel:
    def __init__(self):
        self.items_store = None
        self.tdf = None, None

    def set_dataframe(self, filename, **split_kwargs):
        self.tdf = file_handler.get_tabular_pandas(filename, **split_kwargs)

    def get_store(self, **split_kwargs):
        assert self.tdf is not None, "Dataframe not initialized"
        tdf = file_handler.get_values(self.tdf, **split_kwargs)
        if tdf is None:
            return None
        return file_handler.get_store(tdf, **split_kwargs)
